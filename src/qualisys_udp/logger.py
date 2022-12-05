import csv
from pathlib import Path
from datetime import datetime


class Logger:
    def __init__(self, name, marker_id, log_dir):
        self.marker_id = marker_id

        # -- Create the log directory if it does not exist
        Path(log_dir).mkdir(parents=True, exist_ok=True)

        # -- Create the log file with YYYYMMDD_HHMMSS.csv
        self.fname = (
            Path(log_dir) / f"{datetime.now():%Y%m%d_%H%M%S}_{marker_id}_{name}.csv"
        )

        # -- Write the header
        with self.fname.open("w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "epoch [s]",
                    "x [m]",
                    "y [m]",
                    "z [m]",
                    "roll [rad]",
                    "pitch [rad]",
                    "yaw [rad]",
                ]
            )
            file.close()

    def log(self, msg):
        if len(msg) < 7:
            return
        stamp_s, x, y, z, roll, pitch, yaw = msg
        # -- Log the detection of the tag
        with self.fname.open("a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([stamp_s, x, y, z, roll, pitch, yaw])
            file.close()
        # print("[", stamp_s, "]", x, y, z, roll, pitch, yaw)
