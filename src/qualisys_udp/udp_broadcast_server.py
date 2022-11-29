import json
import socket


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


class UDPBroadcastServer:
    def __init__(self, ip, port):
        # -- Enable port reusage
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        )
        # -- Enable broadcasting mode
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # -- Enable broadcasting mode
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.settimeout(None)
        self.ip = ip
        self.port = port

        current_ip = get_ip_address()
        if self.ip != current_ip:
            self.ip = current_ip

    def broadcast(self, message):
        # -- Broadcast the dictionary as a bytes-like object (string-like info) and empties
        broadcast_string = json.dumps(message, indent=3)

        self.socket.sendto(
            broadcast_string.encode("utf-8"),
            (self.ip, self.port),
        )
