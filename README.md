# dungeon-crawler
dungeon crawler game run code and data

utilises pygame to create dungeon crawler

## setup

conda activate dungeoncrawler

## notes

- for collision detection, just add Body() to the entities
- state update logic currently contained within event response, meaning not currently possible to hold down multiple keys


# TO DO List

## this feature branch
- creating level files is updated - now need to update saving level files

## Ten-minute Tasks
- duplicated code for loading and writing of files (level.py, levelmaker.py, mapmaker.py?)
- functionality/refactor to tidy entity data handling (level.py, levelmaker.py, objects.py)
- add content path as an env var (to tidy env vars) (.env, config.py)
- make item types into a dict for easier referencing, rather than a list (item_types.py)
- add other items to be collected, and improve levelmaker functionality for procedurally generating items of various types (item_types.py, levelmaker.py)
- utilise distance function (math_ext.py) in other sqrt functions (search for sqrt)
- bug in line of sight north tiles not blocked - something to do with the doors
- refactor python data and content data files (src/data/ and content/data/) to be more consistent. e.g. add dictionaries for all objects which objects.py needs to reference
- spawn npcs not next to walls (same logic as stairs) and not on stairs and give them solid bodies, and make moving into them trigger interactions - avoid any entities spawning on top of each other
- equipped items are unequipped when navigating between levels

## short-term tasks
- persist state of objects in level save file (open doors currently default to being closed)
- save inventory and other data into a save game file
- utilise texture atlasses
- add unit tests on tiles.json to check uniqueness of name, id, config
- add minimap
- add zoom functionality

## long-term tasks
- player classes
- mobs
- puzzle rooms (e.g. moving levers/blocks to open secret door, gap to cross, sacrificial altar)
- window layout

# Design goals
- use classes rather than dictionaries to improve type safety
- use more enums
- call down, signal up