"""Bridge between Trill Craft and Processing visualisers.

Streams Trill Craft sensor data over USB serial in the same format
expected by the official Processing sketches (space-separated integers
terminated by a newline). Also listens for configuration commands sent
from the TrillCraftSettings Processing sketch (baseline, prescaler,
threshold, bits, mode).

Use this as your CircuitPython `code.py` when running the Processing
visualisers.
"""

import sys
import time
import board
import busio
import supervisor

from trill_circuitpython import Craft
from trill_circuitpython import MODE_CENTROID, MODE_RAW, MODE_BASELINE, MODE_DIFF

# ---------------------------------------------------------------------------
# I2C and sensor setup
# ---------------------------------------------------------------------------

# Initialize I2C bus (ESP32-S2 mini default pins)
i2c = busio.I2C(board.SCL, board.SDA)

# Wait for I2C lock (sometimes needed on ESP32-S2)
while not i2c.try_lock():
    pass
i2c.unlock()

# Start Trill Craft in RAW mode so that the Processing sketch
# receives per-channel data matching its expectations.
craft = Craft(i2c, address=0x30, mode=MODE_RAW)

# Keep track of scan settings so we can change bits from commands
_current_speed = 1
_current_bits = 12

# Reasonable default settings for calibration/visualisation
craft.set_scan_settings(speed=_current_speed, resolution=_current_bits)
craft.set_prescaler(4)
craft.set_noise_threshold(30)
craft.update_baseline()

print("Trill Craft Processing bridge started")
print("Streaming sensor data over USB serial for Processing…")

# ---------------------------------------------------------------------------
# Command handling from Processing (TrillCraftSettings)
# ---------------------------------------------------------------------------

_command_buffer = ""
_last_serial_time = 0.0


def _handle_command(cmd: str) -> None:
    """Parse and apply a single command string.

    Supported commands (case-insensitive):
      baseline
      prescaler: <1-8>
      threshold: <0-255>
      bits: <9-16>
      mode: centroid|raw|baseline|differential
    """
    global _current_speed, _current_bits

    text = cmd.strip()
    if not text:
        return

    lower = text.lower()

    # Baseline update
    if lower.startswith("baseline"):
        craft.update_baseline()
        return

    # Prescaler
    if lower.startswith("prescaler"):
        rest = lower.replace("prescaler", "", 1).replace(":", " ")
        parts = rest.split()
        if not parts:
            return
        try:
            value = int(parts[0])
        except ValueError:
            return
        if value < 1:
            value = 1
        if value > 8:
            value = 8
        craft.set_prescaler(value)
        return

    # Noise threshold
    if lower.startswith("threshold"):
        rest = lower.replace("threshold", "", 1).replace(":", " ")
        parts = rest.split()
        if not parts:
            return
        try:
            value = int(parts[0])
        except ValueError:
            return
        if value < 0:
            value = 0
        if value > 255:
            value = 255
        craft.set_noise_threshold(value)
        return

    # Resolution bits (affects scan settings)
    if lower.startswith("bits"):
        rest = lower.replace("bits", "", 1).replace(":", " ")
        parts = rest.split()
        if not parts:
            return
        try:
            bits = int(parts[0])
        except ValueError:
            return
        if bits < 9:
            bits = 9
        if bits > 16:
            bits = 16
        _current_bits = bits
        craft.set_scan_settings(speed=_current_speed, resolution=_current_bits)
        return

    # Mode selection
    if lower.startswith("mode"):
        rest = lower.replace("mode", "", 1).replace(":", " ")
        parts = rest.split()
        if not parts:
            return
        m = parts[0]
        if m.startswith("centroid"):
            craft.set_mode(MODE_CENTROID)
        elif m.startswith("raw"):
            craft.set_mode(MODE_RAW)
        elif m.startswith("baseline"):
            craft.set_mode(MODE_BASELINE)
        elif m.startswith("diff") or m.startswith("differential"):
            craft.set_mode(MODE_DIFF)
        return


def _poll_serial_commands() -> None:
    """Collect bytes from USB serial and detect complete commands.

    The original Processing sketch sends commands like:
      "baseline"
      "prescaler: 4"
      "threshold: 30"
      "bits: 12"
      "mode: raw"

    It may or may not append a newline, so we use an inactivity timeout
    to detect end-of-command if no newline is present.
    """
    global _command_buffer, _last_serial_time

    now = time.monotonic()

    # Read all available bytes without blocking
    while supervisor.runtime.serial_bytes_available:
        try:
            ch = sys.stdin.read(1)
        except Exception as e:
            # If reading from stdin fails for any reason, stop polling
            # this cycle and try again on the next iteration.
            # This avoids killing the main loop silently.
            return
        if ch in ("\n", "\r"):
            if _command_buffer:
                _handle_command(_command_buffer)
                _command_buffer = ""
        else:
            _command_buffer += ch
            _last_serial_time = now

    # If we have buffered characters but there has been a pause in input,
    # treat that as end-of-command even if no newline arrived.
    if _command_buffer and (now - _last_serial_time) > 0.2:
        _handle_command(_command_buffer)
        _command_buffer = ""


# ---------------------------------------------------------------------------
# Main loop: stream data to Processing and handle commands
# ---------------------------------------------------------------------------

while True:
    try:
        # Read from Trill Craft according to its current mode.
        data = craft.read()

        # Stream values as space-separated integers, one line per frame.
        # This matches what the Processing sketches expect.
        if data is not None:
            try:
                line = " ".join(str(int(v)) for v in data)
                print(line)
            except Exception:
                # If anything weird happens with the data, skip this frame.
                pass

        # Check for any incoming configuration commands
        _poll_serial_commands()

        # Small delay to keep output to a reasonable rate
        time.sleep(0.01)

    except Exception as e:
        # On unexpected errors, report and pause briefly before continuing
        print("Error in main loop:", e)
        time.sleep(0.1)
