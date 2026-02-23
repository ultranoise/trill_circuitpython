"""
Example of using Trill Craft sensor with CircuitPython on ESP32-S2 mini,
including configuration of prescaler, noise threshold, and scan settings.
"""

import time
import board
import busio

from trill_circuitpython import Craft, Touches1D
from trill_circuitpython import MODE_CENTROID, MODE_RAW

# --- I2C SETUP (ESP32-S2 mini) ---------------------------------------------

i2c = busio.I2C(board.SCL, board.SDA)

# Wait for I2C lock (sometimes needed on ESP32-S2)
while not i2c.try_lock():
    pass
i2c.unlock()

# --- TRILL CRAFT INITIALISATION --------------------------------------------

# Default address is 0x30, default mode is MODE_CENTROID
craft = Craft(i2c, address=0x30, mode=MODE_CENTROID)

print("Trill Craft on ESP32-S2 mini")
print("Type:", craft.get_type())
print("Firmware:", craft.get_firmware_version())
print("Size:", craft.get_size())
print("Channels:", craft.get_num_channels())
print("-" * 40)

# --- CONFIGURATION EXAMPLES -------------------------------------------------
# You can tweak these three knobs depending on your application:

# 1) Scan settings: speed & resolution (number of bits)
#    speed: 0–3  (0 = slowest / highest quality, 3 = fastest / noisier)
#    resolution: 9–16 bits (higher = finer, but noisier & slower)
craft.set_scan_settings(speed=1, resolution=12)

# 2) Prescaler: 1–8
#    Lower prescaler  = faster / more sensitive, but more noise
#    Higher prescaler = slower / less sensitive, but more stable
craft.set_prescaler(prescaler=4)

# 3) Noise threshold: 0–255
#    Values below this threshold are ignored in centroid/diff modes.
craft.set_noise_threshold(threshold=30)

# Optionally, update baseline after configuration, with no touches on the sensor
print("Updating baseline… (remove all fingers from Craft)")
time.sleep(0.5)
craft.update_baseline()
print("Baseline updated.")
print("-" * 40)

# --- MAIN LOOP --------------------------------------------------------------

while True:
    try:
        # Example 1: CENTROID MODE (higher-level touch positions)
        data = craft.read()
        touches = Touches1D(data)

        if not touches.is_empty():
            print("Active touches:", touches.get_num_touches())
            for i, touch in enumerate(touches.get_touches()):
                position, size = touch
                print("  Touch {}: position={} size={}".format(i, position, size))
        else:
            print("No touches (centroid)")

        # Example 2: RAW MODE (uncomment if you want to see raw channels)
        # craft.set_mode(MODE_RAW)
        # raw_data = craft.read()
        # print("Raw channels:", raw_data)
        # craft.set_mode(MODE_CENTROID)

        time.sleep(0.1)

    except Exception as e:
        print("Error:", e)
        time.sleep(1)
