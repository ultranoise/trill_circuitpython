"""
Example of using Trill Bar sensor with CircuitPython
"""

import board
import busio
import time
from trill_circuitpython import Bar, Touches1D, MODE_CENTROID

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize Trill Bar sensor
bar = Bar(i2c, mode=MODE_CENTROID)

print("Trill Bar Example")
print(f"Sensor type: {bar.get_type()}")
print(f"Firmware version: {bar.get_firmware_version()}")
print(f"Size: {bar.get_size()}")
print(f"Channels: {bar.get_num_channels()}")
print("-" * 40)

# Main loop
while True:
    try:
        # Read touch data
        data = bar.read()
        touches = Touches1D(data)
        
        if not touches.is_empty():
            print(f"Active touches: {touches.get_num_touches()}")
            for i, touch in enumerate(touches.get_touches()):
                position, size = touch
                print(f"  Touch {i}: position={position}, size={size}")
        else:
            print("No touches detected")
            
        time.sleep(0.1)  # Small delay between reads
        
    except KeyboardInterrupt:
        print("Stopping...")
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)
