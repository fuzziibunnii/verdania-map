# Verdania Story Map

Read-only snapshot of the Echoes of Verdania story map, embedded on the "Verdania Story Map" page of the Notion campaign hub.

- `index.html`: the snapshot page, with the map image and pins built in (generated, so don't edit it by hand)
- `pins.json`: the pins in this snapshot, exported from the live map's database
- `src/live-map.html`: source of the live, editable map (Claude artifact)
- `src/verdania-map.jpg`: the Meridian League map
- `build.py`: rebuilds `index.html` from `src/` and `pins.json` (`python3 build.py`)

Pins are edited on the live map. A weekly scheduled task (Tuesday mornings) exports the pins, rebuilds the snapshot, pushes it here, and swaps it into Notion.
