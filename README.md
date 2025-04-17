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
- manage initial map and level (main.py)
- duplicated code for loading and writing of files (level.py, levelmaker.py, mapmaker.py?)
- functionality/refactor to tidy entity data handling (level.py, levelmaker.py, objects.py)
- add content path as an env var (to tidy env vars) (.env, config.py)
- add fog layer to level save file (level.py)

## short-term tasks
- new game function creates new game rather than restarts current (menu.py)
- utilise texture atlasses
- add unit tests on tiles.json to check uniqueness of name, id, config

## long-term tasks
- player classes
- mobs