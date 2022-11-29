import json
import socket
from threading import Thread
import argparse


class UDPClient:
    def __init__(self, port):
        # -- UDP
        self.client = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        )

        # -- Enable port reusage
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # -- Enable broadcasting mode
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # self.client.settimeout(params["timeout"])
        self.client.bind(("", port))
        self.th = Thread(target=self.loop, daemon=True)
        self.th.start()

    def loop(self):
        while True:
            print("waiting for data...")
            try:
                broadcast_data, _ = self.client.recvfrom(4096)
                result = json.loads(broadcast_data)
                print("Received:", result)

            except Exception as e:
                print("Got exception trying to recv %s" % e)

    def __del__(self):
        self.client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=50000)
    args = parser.parse_args()
    client = UDPClient(args.port)

    while True:
        pass
