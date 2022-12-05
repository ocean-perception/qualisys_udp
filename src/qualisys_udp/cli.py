import argparse
import numpy as np
import threading


from .qualisys import Qualisys
from .udp_broadcast_server import UDPBroadcastServer
from .rate import Rate
from .logger import Logger


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--qualisys_ip",
        type=str,
        default="192.168.60.71",
        help="Qualisys IP address",
    )
    parser.add_argument(
        "--body-name",
        type=str,
        default="MrBuild",
        help="Qualisys body name",
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
        default=0.03,
        help="Add noise to the broadcasted position",
    )
    parser.add_argument(
        "--noise-orientation",
        type=float,
        default=0.01,
        help="Add noise to the broadcasted orientation",
    )
    parser.add_argument(
        "--log-dir",
        type=str,
        default="./logs",
        help="Log directory",
    )

    # Position only and orientation only are mutually exclusive
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--position-only",
        action="store_true",
        help="Broadcast position only",
    )
    group.add_argument(
        "--orientation-only",
        action="store_true",
        help="Broadcast orientation only",
    )

    args = parser.parse_args()

    print("\nStarting Qualisys UDP broadcast server")
    print("  * Qualisys IP: " + str(args.qualisys_ip))
    print("  * Body name: " + str(args.body_name))
    print("  * Marker ID: " + str(args.marker_id))
    print("  * UDP port: " + str(args.port))
    print("  * Broadcast rate: " + str(args.rate))
    print("  * Position noise: " + str(args.noise_position))
    print("  * Orientation noise: " + str(args.noise_orientation), end="\n\n")

    qualisys = Qualisys(args.qualisys_ip, args.body_name)
    udp_server = UDPBroadcastServer("255.255.255.255", args.port)
    logger_groundtruth = Logger("groundtruth", args.marker_id, args.log_dir)
    logger_broadcasted = Logger("broadcasted", args.marker_id, args.log_dir)
    rate = Rate(args.rate)
    fixed_rate = Rate(100.0)

    while True:
        if qualisys.is_connected:
            # Get the last message from the Qualisys server
            msg = qualisys.read()
            logger_groundtruth.log(msg)
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
                if args.position_only:
                    msg[args.marker_id] = [
                        stamp_s,
                        stamp_s,
                        x_m,
                        y_m,
                        z_m,
                        None,
                        None,
                        None,
                    ]
                elif args.orientation_only:
                    msg[args.marker_id] = [
                        stamp_s,
                        stamp_s,
                        None,
                        None,
                        None,
                        roll,
                        pitch,
                        yaw,
                    ]
                else:
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
                remaining_time_s = rate.remaining()
                # print(remaining_time_s)
                if remaining_time_s <= 0:
                    udp_server.broadcast(msg)
                    logger_broadcasted.log([stamp_s, x_m, y_m, z_m, roll, pitch, yaw])
                    rate.reset()
        else:
            print("Qualisys not connected")
        fixed_rate.sleep()


if __name__ == "__main__":
    main()
