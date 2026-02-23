"""
Example of using Trill Square sensor with CircuitPython
"""

import board
import busio
import time
from trill_circuitpython import Square, Touches2D, MODE_CENTROID

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize Trill Square sensor
square = Square(i2c, mode=MODE_CENTROID)

print("Trill Square Example")
print(f"Sensor type: {square.get_type()}")
print(f"Firmware version: {square.get_firmware_version()}")
print(f"Size: {square.get_size()}")
print(f"Channels: {square.get_num_channels()}")
print("-" * 40)

# Main loop
while True:
    try:
        # Read touch data
        data = square.read()
        touches = Touches2D(data)
        
        if not touches.is_empty():
            print(f"Active touches: {touches.get_num_touches()}")
            for i, touch in enumerate(touches.get_touches()):
                x, y, size_x, size_y = touch
                print(f"  Touch {i}: position=({x}, {y}) size=({size_x}, {size_y})")
        else:
            print("No touches detected")
            
        time.sleep(0.1)  # Small delay between reads
        
    except KeyboardInterrupt:
        print("Stopping...")
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)
