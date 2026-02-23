# CircuitPython Trill Sensor library
# Copyright (C) 2021 H. Groefsema
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
CircuitPython library for Bela's Trill touch sensors.

This library provides implementations for various Trill sensors including:
- Trill Bar
- Trill Square  
- Trill Craft
- Trill Ring
- Trill Hex

Example usage:
```python
import board
import busio
from trill_circuitpython import Square, Touches2D

i2c = busio.I2C(board.SCL, board.SDA)

square = Square(i2c)
data = square.read()
touches = Touches2D(data)

for touch in touches.get_touches():
    print(touch)
```
"""

from .trill import TrillSensor, Bar, Square, Craft, Ring, Hex
from .trill import MODE_CENTROID, MODE_RAW, MODE_BASELINE, MODE_DIFF
from .touch import Touches, Touches1D, Touches2D

__version__ = "1.0.0"
__repo__ = "https://github.com/your-username/trill-circuitpython"

__all__ = [
    "TrillSensor",
    "Bar", 
    "Square",
    "Craft", 
    "Ring",
    "Hex",
    "MODE_CENTROID",
    "MODE_RAW", 
    "MODE_BASELINE",
    "MODE_DIFF",
    "Touches",
    "Touches1D",
    "Touches2D"
]
