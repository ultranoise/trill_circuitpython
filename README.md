# Trill CircuitPython Library

CircuitPython port of the [MicroPython Trill Sensor Library](https://github.com/Heerkog/MicroPythonTrill) for Bela's [Trill capacitive touch sensors](https://bela.io/products/trill/).

This library lets you read Trill sensors from CircuitPython boards (e.g. ESP32-S2 mini), and optionally visualize and configure them using the official Processing sketches provided by the Trill makers.

## Features

- Support for these Trill boards:
  - Bar
  - Square
  - Craft
  - Ring
  - Hex
- High-level centroid touch data (1D / 2D) via `Touches1D` and `Touches2D` helpers
- Access to raw, baseline, and differential scan modes
- Configuration of:
  - scan speed and resolution (bits)
  - prescaler
  - noise threshold
  - minimum touch size
  - auto scan interval
- Optional Processing bridge to reuse the original Trill visualization & configuration sketches

## Source Layout

- `trill_circuitpython/`
  - `trill.py` – core sensor classes (`TrillSensor`, `Bar`, `Square`, `Craft`, `Ring`, `Hex`)
  - `touch.py` – touch interpretation helpers (`Touches`, `Touches1D`, `Touches2D`)
  - `__init__.py` – public API re-exports
  - `examples/`
    - `trill_bar_example.py`
    - `trill_square_example.py`
    - `trill_craft_example.py`
    - `trill_craft_processing_bridge.py` – bridge for Processing sketches

## Credits

This is a **CircuitPython port** of the original MicroPython library by **H. Groefsema**:

- Repository: https://github.com/Heerkog/MicroPythonTrill

The I2C register map, data formats, and class design are based closely on that project. All original copyright and GPL licensing terms apply; see `trill_circuitpython/LICENSE`.

Trill hardware and original Processing examples are by **Bela**:

- Trill: https://bela.io/products/trill/
- Processing examples are from the Trill repository / documentation.

## Installation on a CircuitPython Board

1. Install CircuitPython on your board (e.g. ESP32-S2 mini) following Adafruit's guide.
2. Download or clone this repository.
3. Copy the following folders to the `CIRCUITPY` drive:
   - `trill_circuitpython/` → `/lib/trill_circuitpython/`
   - `adafruit_bus_device/` (from the Adafruit CircuitPython bundle) → `/lib/adafruit_bus_device/`
4. Put one of the example scripts on the root of the board as `code.py`.

> **Note on I2C pull-up resistors**
>
> Trill uses I2C. You **must** have pull-up resistors on SDA and SCL to 3.3 V. Many boards (and STEMMA QT / Qwiic connectors) already have internal 4.7 kΩ pull-ups. If your setup does not, add **4.7–10 kΩ** resistors from SDA to 3.3 V and from SCL to 3.3 V.

## Standalone Usage Examples

### Example: Trill Craft (1D centroid touches)

See `trill_circuitpython/examples/trill_craft_example.py` for a complete script. Typical structure:

```python
import time
import board
import busio

from trill_circuitpython import Craft, Touches1D, MODE_CENTROID

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize Trill Craft
craft = Craft(i2c, address=0x30, mode=MODE_CENTROID)

# Optional configuration
g_speed = 1
bits = 12
craft.set_scan_settings(speed=g_speed, resolution=bits)
craft.set_prescaler(4)
craft.set_noise_threshold(30)
craft.update_baseline()

while True:
    data = craft.read()
    touches = Touches1D(data)

    if not touches.is_empty():
        for position, size in touches.get_touches():
            print("position=", position, "size=", size)
    else:
        print("no touches")

    time.sleep(0.1)
```

### Example: Trill Square (2D centroid touches)

See `trill_circuitpython/examples/trill_square_example.py`. Typical structure:

```python
import time
import board
import busio

from trill_circuitpython import Square, Touches2D, MODE_CENTROID

i2c = busio.I2C(board.SCL, board.SDA)

square = Square(i2c, address=0x28, mode=MODE_CENTROID)

while True:
    data = square.read()
    touches = Touches2D(data)

    for x, y, size_x, size_y in touches.get_touches():
        print("x=", x, "y=", y, "size_x=", size_x, "size_y=", size_y)

    time.sleep(0.1)
```

## Using the Processing Visualisers

The Trill project includes Processing sketches (e.g. `TrillCraft.pde`, `TrillCraftSettings.pde`) that visualize sensor values and allow changing configuration parameters over serial. This library includes a **bridge script** to talk to those sketches from CircuitPython.

### 1. Set up the CircuitPython bridge

1. Copy `trill_circuitpython/examples/trill_craft_processing_bridge.py` to the root of your `CIRCUITPY` drive as `code.py`.
2. Ensure the `trill_circuitpython` library and `adafruit_bus_device` are present in `/lib` as described above.
3. Connect your Trill Craft board to the CircuitPython board via I2C (3.3 V, GND, SDA, SCL), with appropriate pull-ups.
4. Open a serial console; on reset you should see:
   - `Trill Craft Processing bridge started`
   - `Streaming sensor data over USB serial for Processing…`
5. The board will continuously print lines of space-separated integers (raw channel values) over USB serial.

### 2. Run the Processing sketches

1. Open Processing.
2. From the Trill Processing examples, open:
   - `TrillCraft/TrillCraft.pde` for simple bar-graph visualization, or
   - `TrillCraftSettings/TrillCraftSettings.pde` for visualization **and** configuration controls.
3. In the Processing console, note the list printed by `Serial.list()` and set `gPortNumber` in the sketch to the index that corresponds to your CircuitPython board's USB serial port.
4. Run the Processing sketch. It will:
   - Read the space-separated integers from the CircuitPython bridge and display them.
   - In the `TrillCraftSettings` version, send text commands back over serial.

### 3. Supported configuration commands from Processing

When using `TrillCraftSettings.pde`, the following commands (typed into the GUI or selected from its dropdown) are understood by `trill_craft_processing_bridge.py`:

- `baseline` – call `update_baseline()` on the sensor.
- `prescaler: N` – set prescaler to `N` (1–8).
- `threshold: N` – set noise threshold to `N` (0–255).
- `bits: N` – set resolution (number of bits) to `N` (9–16) and update scan settings.
- `mode: centroid` – use centroid mode.
- `mode: raw` – use raw channel mode (default for Visualization bridge).
- `mode: baseline` – read baseline values.
- `mode: differential` – read difference-from-baseline values.

The bridge parses these strings and applies the corresponding `Craft` methods, while continuing to stream sensor data back to Processing.

## License

The original MicroPython Trill library and this CircuitPython port are licensed under the **GNU General Public License v3.0 or later (GPL-3.0-or-later)**. See `trill_circuitpython/LICENSE` for full terms.
