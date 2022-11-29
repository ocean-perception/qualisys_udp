# Qualisys UDP server

UDP server with variable rate and added noise.

## Usage

```bash
qualisys_udp [-h] [--qualisys_ip QUALISYS_IP] [--body-id BODY_ID] [--marker_id MARKER_ID] [--port PORT] [--rate RATE]
             [--noise-position NOISE_POSITION] [--noise-orientation NOISE_ORIENTATION]

options:
  -h, --help            show this help message and exit
  --qualisys_ip QUALISYS_IP
                        Qualisys IP address (default: 192.168.0.71)
  --body-id BODY_ID     Qualisys body ID (default: 1)
  --marker_id MARKER_ID
                        Marker ID to broadcast (default: 1)
  --port PORT           UDP port to broadcast (default: 50000)
  --rate RATE           Broadcast rate in Hz (default: 1.0)
  --noise-position NOISE_POSITION
                        Add noise to the broadcasted position (default: 0.05 m)
  --noise-orientation NOISE_ORIENTATION
                        Add noise to the broadcasted orientation (default: 0.01 rad)

```

## How to install

Install it using pip:

```bash
pip install git+https://github.com/ocean-perception/qualisys_udp.git
```