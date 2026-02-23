# CircuitPython Trill Sensor Library

This library offers implementations of Bela's [Trill touch sensors](https://bela.io/products/trill/) for CircuitPython.

## Supported Sensors

- **Trill Bar** - Linear touch sensor
- **Trill Square** - Square 2D touch sensor  
- **Trill Craft** - Customizable touch sensor
- **Trill Ring** - Circular touch sensor
- **Trill Hex** - Hexagonal 2D touch sensor

## Installation

### CircuitPython Library Manager
In CircuitPython 7.0+, use the library manager to install `trill-circuitpython`.

### Manual Installation
Download the library files and copy the `trill_circuitpython` directory to your board's `lib` folder.

## Usage

### Basic Example

```python
import board
import busio
from trill_circuitpython import Square, Touches2D

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize Trill Square sensor
square = Square(i2c)

# Read touch data
data = square.read()
touches = Touches2D(data)

# Process touches
for touch in touches.get_touches():
    print(f"Touch at ({touch[0]}, {touch[1]}) size: {touch[2]}x{touch[3]}")
```

### Bar Sensor Example

```python
import board
import busio
from trill_circuitpython import Bar, Touches1D

i2c = busio.I2C(board.SCL, board.SDA)

bar = Bar(i2c)
data = bar.read()
touches = Touches1D(data)

for touch in touches.get_touches():
    position, size = touch
    print(f"Touch at position {position} with size {size}")
```

## API Reference

### Sensor Classes

All sensor classes inherit from `TrillSensor` and provide these common methods:

- `identify()` - Identify the sensor type and firmware version
- `get_type()` - Get the sensor type as a string
- `get_firmware_version()` - Get the firmware version
- `get_size()` - Get the sensor dimensions as (x, y) tuple
- `get_num_channels()` - Get the number of channels
- `read()` - Read the latest scan data
- `set_mode(mode)` - Set the sensor mode
- `get_mode()` - Get the current sensor mode
- `set_scan_settings(speed, resolution)` - Configure scan settings
- `update_baseline()` - Update baseline capacitance
- `set_prescaler(prescaler)` - Set the prescaler (1-8)
- `set_noise_threshold(threshold)` - Set noise threshold (0-255)
- `set_IDAC_value(value)` - Set IDAC value (0-255)
- `set_minimum_touch_size(minSize)` - Set minimum touch size
- `set_auto_scan_interval(interval)` - Set auto scan interval
- `is_1D()` - Returns True for 1D sensors
- `is_2D()` - Returns True for 2D sensors

### Sensor Modes

- `MODE_CENTROID` - Centroid tracking mode (default)
- `MODE_RAW` - Raw capacitance values
- `MODE_BASELINE` - Baseline values
- `MODE_DIFF` - Difference from baseline

### Touch Classes

- `Touches1D` - For 1D sensors (Bar, Ring, Craft)
- `Touches2D` - For 2D sensors (Square, Hex)

Both provide:
- `get_touches()` - List of touch tuples
- `get_num_touches()` - Number of active touches
- `get_touch(index)` - Get specific touch
- `is_empty()` - Check if any touches are active

## I2C Addresses

Default I2C addresses for each sensor:
- Bar: `0x20`
- Square: `0x28`
- Craft: `0x30`
- Ring: `0x38`
- Hex: `0x40`

## CircuitPython Compatibility

This library is compatible with CircuitPython 7.0+ and requires:
- `busio` module
- `time` module
- `struct` module

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

Based on the original MicroPython Trill library by H. Groefsema.
- [About Trill](https://learn.bela.io/products/trill/about-trill/)
- [Trill Arduino](https://github.com/BelaPlatform/Trill-Arduino)
