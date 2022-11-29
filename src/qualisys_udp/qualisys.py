import asyncio
import importlib
import math
import weakref
from datetime import datetime
from threading import Thread


qtm_spec = importlib.util.find_spec("qtm")
if qtm_spec is None:
    print("------------------------------------")
    print("   WARNING: qtm module not found")
    print("------------------------------------")
    print("  * Please install the qtm module with:")
    print("        pip install qtm")
else:
    import qtm


def is_valid(x):
    return (not math.isnan(x)) and type(x) == float


class Qualisys:
    def __init__(self, qualisys_ip, marker_id, parent=None):
        if parent is not None:
            self._parent = weakref.ref(parent)
        self.marker_id = marker_id
        self.qualisys_ip = qualisys_ip

        # total elapsed simulation time
        self.elapsed_time = 0.0
        self.thread = None
        self.is_connected = False
        self.last_msg = None

        if qtm_spec is not None:
            self.client = asyncio.new_event_loop()
            self.thread = Thread(target=self.start_background_loop)
            self.thread.daemon = True  # Daemonize thread
            self.thread.start()

    def start_background_loop(self):
        asyncio.set_event_loop(self.client)
        asyncio.ensure_future(self.loop())
        self.client.run_forever()

    async def loop(self):
        """Main function"""
        print("Trying to connect to Qualisys server in: " + str(self.qualisys_ip))
        connection = await qtm.connect(self.qualisys_ip)

        if connection is None:
            # TODO: Here we can try to connect to the fake server,
            # that must meet the same qtm data structure
            print("No active server found in:" + str(self.qualisys_ip))
            self.is_connected = False
            return
        try:
            self.is_connected = True
            _ = await connection.get_state()
            await connection.stream_frames(
                frames="frequency:5",
                components=["6dEuler"],
                on_packet=self.on_packet,
            )
        except asyncio.TimeoutError:
            self.is_connected = False
            return

    def on_packet(self, packet):
        """Callback function that is run when stream-data is triggered by QTM"""
        _, bodies = packet.get_6d_euler()
        stamp = datetime.utcnow()
        stamp = datetime.timestamp(stamp)
        if len(bodies) > self.marker_id:
            self.last_msg = (stamp, bodies[self.body_number])

    def read(self) -> list[float]:
        if self.last_msg is None:
            return []

        stamp, body = self.last_msg
        x_mm = body[0][0]  # These are floats
        y_mm = body[0][1]
        z_mm = body[0][2]
        roll_deg = body[1][0]
        pitch_deg = body[1][1]
        yaw_deg = body[1][2]

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
            return stamp_s, x, y, z, roll, pitch, yaw
        return []

    def __del__(self):
        if self.client.is_running:
            self.client.stop()
        if not self.client.is_closed:
            self.client.close()
