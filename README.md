# dungeon-crawler
dungeon crawler game run code and data

utilises pygame to create dungeon crawler

## setup

conda activate dungeoncrawler

## notes

- for collision detection, just add Body() to the entities
- state update logic currently contained within event response, meaning not currently possible to hold down multiple keys


# TO DO List

## Ten-minute Tasks
- duplicated code for loading and writing of files (level.py, levelmaker.py, mapmaker.py?)
- functionality/refactor to tidy entity data handling (level.py, levelmaker.py, objects.py)
- add content path as an env var (to tidy env vars) (.env, config.py)
- add fog layer to level save file (level.py)
- make item types into a dict for easier referencing, rather than a list (item_types.py)
- add other items to be collected, and improve levelmaker functionality for procedurally generating items of various types (item_types.py, levelmaker.py)

## short-term tasks
- new game function creates new game rather than restarts current (menu.py)
- line of sight for player, blocked by walls etc (instead of 5-tile bubble)
- utilise texture atlasses
- add unit tests on tiles.json to check uniqueness of name, id, config
- add minimap

## long-term tasks
- player classes
- mobs