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
- tidy movement handler and keyup and keydown events (engine.py) - JUMPY MOVEMENT!
- manage initial map and level (main.py)
- camera not snapping to player when changing dngn level (player.py?)
- duplicated code for loading and writing of files (level.py, levelmaker.py, mapmaker.py?)
- turn singletons into classes where appropriate
- functionality/refactor to tidy entity data handling (level.py, levelmaker.py, objects.py)

## short-term tasks
- add field of vision
- add fog (unexplored area)
- add shadow (area outside of field of vision)
- utilise texture atlasses
- spawn player on down stairs when travelling upwards
- add unit tests on tiles.json to check uniqueness of name, id, config

## long-term tasks
- player classes
- mobs