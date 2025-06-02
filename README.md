# dungeon-crawler
dungeon crawler game run code and data

utilises pygame to create dungeon crawler

## setup

conda activate dungeoncrawler

## notes

- for collision detection, just add Body() to the entities
- state update logic currently contained within event response, meaning not currently possible to hold down multiple keys


# TO DO List
- video: 21:43

## Ten-minute Tasks
- duplicated code for loading and writing of files (level.py, levelmaker.py, mapmaker.py?)
- functionality/refactor to tidy entity data handling (level.py, levelmaker.py, objects.py)
- add content path as an env var (to tidy env vars) (.env, config.py)
- make item types into a dict for easier referencing, rather than a list (item_types.py)
- add other items to be collected, and improve levelmaker functionality for procedurally generating items of various types (item_types.py, levelmaker.py)
- utilise distance function (math_ext.py) in other sqrt functions (search for sqrt)
- improve hittable class - attackable? has_health? (usable.py)
- add Body() to closed doors (in usable function) to enable collision detection (and remove it for open doors) (usable.py)

## short-term tasks
- save inventory and other data into a save game file
- line of sight for player, blocked by walls etc (instead of 5-tile bubble)
- utilise texture atlasses
- add unit tests on tiles.json to check uniqueness of name, id, config
- add minimap

## long-term tasks
- player classes
- mobs