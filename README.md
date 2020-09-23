# PaKOMM data API

## Installation

Requires
* Python3

```$ python3 -m pip install -r requirements.txt ```

set a reference point in UTM32N that describes where (0,0) in Euclidean coordinates translates to.

## Usage

for a debug server:
`$ cd backend; python3 main.py`

frontend: open `frontend/index.html` in browser

## API endpoints

* `/send_data` with GET params: `pos_x`, `pos_y`, `type`. Adds a new point feature
* `/get_geojson`. Returns current map state in GeoJSON format (WGS84, lon-lat order)