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
- returning bug: navigating between levels
- change combat range (distance) to tile adjacency?
- remove effects damage and add health bars to enemies
- refactor player acts, so player acts first and then all other active_objs act
- shouldn't be able to equip non-equipables such as gold

## Ten-minute Tasks
- duplicated code for loading and writing of files (level.py, levelmaker.py, mapmaker.py?)
- functionality/refactor to tidy entity data handling (level.py, levelmaker.py, objects.py)
- add content path as an env var (to tidy env vars) (.env, config.py)
- make item types into a dict for easier referencing, rather than a list (item_types.py)
- add other items to be collected, and improve levelmaker functionality for procedurally generating items of various types (item_types.py, levelmaker.py)
- utilise distance function (math_ext.py) in other sqrt functions (search for sqrt)
- remove hittable class (usable.py)
- bug in line of sight north tiles not blocked - something to do with the doors
- refactor python data and content data files (src/data/ and content/data/) to be more consistent. e.g. add dictionaries for all objects which objects.py needs to reference
- spawn npcs not next to walls (same logic as stairs) and not on stairs and give them solid bodies, and make moving into them trigger interactions

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