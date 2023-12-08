import numpy as np
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
                    "elapsed [s]",
                    "x [m]",
                    "y [m]",
                    "z [m]",
                    "roll [deg]",
                    "pitch [deg]",
                    "yaw [deg]",
                    "broadcasted 1=yes",
                ]
            )
            file.close()

    def log(self, msg, broadcasted=False):
        if len(msg) < 7:
            return
        stamp_s, x, y, z, roll, pitch, yaw = msg
        # -- Log the detection of the tag
        with self.fname.open("a", newline="") as file:
            writer = csv.writer(file)
            roll_deg = np.degrees(roll)
            pitch_deg = np.degrees(pitch)
            yaw_deg = np.degrees(yaw)
            broadcasted_0_1 = int(broadcasted)
            writer.writerow(
                [
                    stamp_s,
                    stamp_s,
                    x,
                    y,
                    z,
                    roll_deg,
                    pitch_deg,
                    yaw_deg,
                    broadcasted_0_1,
                ]
            )
            file.close()
        # print("[", stamp_s, "]", x, y, z, roll, pitch, yaw)
