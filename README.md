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

## short-term tasks
- add field of vision
- add fog (unexplored area)
- add shadow (area outside of field of vision)
- utilise texture atlasses
- add unit tests on tiles.json to check uniqueness of name, id, config

## long-term tasks
- player classes
- mobs