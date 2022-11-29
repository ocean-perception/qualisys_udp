import argparse
import numpy as np

from .qualisys import Qualisys
from .udp_broadcast_server import UDPBroadcastServer
from .rate import Rate

__all__ = ["Qualisys", "UdpBroadcastServer"]


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--qualisys_ip",
        type=str,
        default="192.168.0.71",
        help="Qualisys IP address",
    )
    parser.add_argument(
        "--body-id",
        type=int,
        default=1,
        help="Qualisys body ID",
    )
    parser.add_argument(
        "--marker_id",
        type=int,
        default=1,
        help="Marker ID to broadcast",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=50000,
        help="UDP port to broadcast",
    )
    parser.add_argument(
        "--rate",
        type=float,
        default=1.0,
        help="Broadcast rate in Hz",
    )
    parser.add_argument(
        "--noise-position",
        type=float,
        default=0.05,
        help="Add noise to the broadcasted position",
    )
    parser.add_argument(
        "--noise-orientation",
        type=float,
        default=0.01,
        help="Add noise to the broadcasted orientation",
    )
    args = parser.parse_args()

    print("\nStarting Qualisys UDP broadcast server")
    print("  * Qualisys IP: " + str(args.qualisys_ip))
    print("  * Body ID: " + str(args.body_id))
    print("  * Marker ID: " + str(args.marker_id))
    print("  * UDP port: " + str(args.port))
    print("  * Broadcast rate: " + str(args.rate))
    print("  * Position noise: " + str(args.noise_position))
    print("  * Orientation noise: " + str(args.noise_orientation), end="\n\n")

    qualisys = Qualisys(args.qualisys_ip, args.body_id)
    udp_server = UDPBroadcastServer("255.255.255.255", args.port)

    rate = Rate(args.rate)

    while True:
        if qualisys.is_connected:
            # Get the last message from the Qualisys server
            msg = qualisys.read()
            if len(msg) > 0:
                stamp_s, x_m, y_m, z_m, roll, pitch, yaw = msg

                # Add noise to the position
                x_m += np.random.normal(0, args.noise_position)
                y_m += np.random.normal(0, args.noise_position)
                z_m += np.random.normal(0, args.noise_position)
                # Add noise to the orientation
                roll += np.random.normal(0, args.noise_orientation)
                pitch += np.random.normal(0, args.noise_orientation)
                yaw += np.random.normal(0, args.noise_orientation)

                # Send the message
                msg = {}
                msg[args.marker_id] = [
                    stamp_s,
                    stamp_s,
                    x_m,
                    y_m,
                    z_m,
                    roll,
                    pitch,
                    yaw,
                ]
                udp_server.broadcast(msg)
        else:
            print("Qualisys not connected")

        rate.sleep()


if __name__ == "__main__":
    main()