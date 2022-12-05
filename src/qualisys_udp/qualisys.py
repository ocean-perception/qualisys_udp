import asyncio
import importlib
import math
import weakref
from datetime import datetime
from threading import Thread
import xml.etree.ElementTree as ET


qtm_spec = importlib.util.find_spec("qtm")
if qtm_spec is None:
    print("------------------------------------")
    print("   WARNING: qtm module not found")
    print("------------------------------------")
    print("  * Please install the qtm module with:")
    print("        pip install qtm")
else:
    import qtm


def body_enabled_count(xml_string):
    xml = ET.fromstring(xml_string)
    return sum(enabled.text == "true" for enabled in xml.findall("*/Body/Enabled"))


def create_body_index(xml_string):
    """Extract a name to index dictionary from 6dof settings xml"""
    xml = ET.fromstring(xml_string)
    body_to_index = {}
    for index, body in enumerate(xml.findall("*/Body/Name")):
        body_to_index[body.text.strip()] = index

    return body_to_index


def is_valid(x):
    valid = (not math.isnan(x)) and type(x) == float
    return valid


def start_background_loop(event_loop, cls) -> None:
    asyncio.set_event_loop(event_loop)
    asyncio.ensure_future(cls.loop())
    event_loop.run_forever()


class Qualisys:
    def __init__(self, qualisys_ip, body_name="MrBuild", parent=None):
        super(Qualisys, self).__init__()
        if parent is not None:
            self._parent = weakref.ref(parent)

        self.qualisys_ip = qualisys_ip
        self.body_name = body_name

        # total elapsed simulation time
        self.elapsed_time = 0.0
        self.thread = None
        self.is_connected = False
        self.last_msg = None

        if qtm_spec is not None:
            self.event_loop = asyncio.new_event_loop()
            self.thread = Thread(
                target=start_background_loop, args=(self.event_loop, self), daemon=True
            )
            self.thread.start()

    async def setup(self):
        connection = await qtm.connect("192.168.60.71")
        if connection is None:
            return
        await connection.stream_frames(
            frames="frequency:1", components=["6dEuler"], on_packet=self.on_packet
        )

    async def loop(self):
        """Main function"""
        print("Trying to connect to Qualisys server in: " + str(self.qualisys_ip))
        connection = await qtm.connect(self.qualisys_ip)  # , version=1.20)

        if connection is None:
            # TODO: Here we can try to connect to the fake server,
            # that must meet the same qtm data structure
            print("No active server found in:" + str(self.qualisys_ip))
            self.is_connected = False
            return
        try:
            self.is_connected = True
            _ = await connection.get_state()

            # Get 6dof settings from qtm
            xml_string = await connection.get_parameters(parameters=["6d"])
            self.body_index = create_body_index(xml_string)

            print(
                "{} of {} 6DoF bodies enabled".format(
                    body_enabled_count(xml_string), len(self.body_index)
                )
            )

            self.body_idx = self.body_index.get(self.body_name)
            if self.body_idx is None:
                print("Body name {} not found".format(self.body_name))
                return
            print("Body index for {}: {}".format(self.body_name, self.body_idx))

            await connection.stream_frames(
                components=["6dEuler"],
                on_packet=self.on_packet,
            )
        except asyncio.TimeoutError:
            self.is_connected = False
            return

    def on_packet(self, packet):
        # Callback function that is run when stream-data is triggered by QTM
        stamp = datetime.utcnow()
        stamp = datetime.timestamp(stamp)
        _, bodies = packet.get_6d_euler()
        if len(bodies) > self.body_idx:
            position, rotation = bodies[self.body_idx]
            self.last_msg = (stamp, position, rotation)

            return

    def read(self) -> list[float]:
        if self.last_msg is None:
            return []

        stamp, position, rotation = self.last_msg
        x_mm = position.x  # These are floats
        y_mm = position.y
        z_mm = position.z
        roll_deg = rotation.a1
        pitch_deg = rotation.a2
        yaw_deg = rotation.a3

        # Check if qualisys has valid data
        if is_valid(x_mm) and is_valid(y_mm) and is_valid(z_mm):
            stamp_s = stamp
            x = x_mm / 1000.0
            y = y_mm / 1000.0
            z = z_mm / 1000.0
            roll = roll_deg * math.pi / 180.0
            pitch = pitch_deg * math.pi / 180.0
            yaw = yaw_deg * math.pi / 180.0
            self.last_msg = None

            output_prefix = "Qualisys"
            print(
                "{} x_m: {:.3f}, y_m: {:.3f}, yaw_deg: {:.3f}, timestamp: {:.3f}".format(
                    output_prefix, x, y, yaw_deg, stamp_s
                )
            )

            return stamp_s, x, y, z, roll, pitch, yaw
        return []
