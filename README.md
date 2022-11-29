# Qualisys UDP server

UDP server with variable rate and added noise.

## Usage

```bash
qualisys_udp [-h] [--qualisys_ip QUALISYS_IP] [--body-id BODY_ID] [--marker_id MARKER_ID] [--port PORT] [--rate RATE]
             [--noise-position NOISE_POSITION] [--noise-orientation NOISE_ORIENTATION] [--log-dir LOG_DIR]
             [--position-only | --orientation-only]

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
                        Add noise to the broadcasted position (default: 0.03)
  --noise-orientation NOISE_ORIENTATION
                        Add noise to the broadcasted orientation (default: 0.01)
  --log-dir LOG_DIR     Log directory (default: ./logs)
  --position-only       Broadcast position only (default: False)
  --orientation-only    Broadcast orientation only (default: False)

```

## How to use in your own projects

In the examples folders you will find a python example to create a UDP client to read
the data broadcasted by this software.

## How to install

Install it using pip:

```bash
pip install git+https://github.com/ocean-perception/qualisys_udp.git
```