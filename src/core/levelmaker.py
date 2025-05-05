# functions to take the basic map file and enrich it with
#  - start location
#  - starting mobs
#  - items
#  - features (altars, portals, doors, etc)
# etc

import logging
import json
from math import ceil
from random import randrange

from data.config import DATA_FOLDER, LEVEL_FOLDER, MAP_FOLDER, SAVE_NAME

map_file = "start.map"
level_file = "start.lvl"

# handle entity data file
entity_file = open(DATA_FOLDER + "/" + 'entities.json',)
entities = json.load(entity_file)
entity_file.close()


# function to create a blanket fog across entire map
def create_fog(map):
    fog = []
    for row in map:
        tile_row = []
        for tile in row:
            tile_row.append("x")
        fog.append(tile_row)
    return fog


# function to extract data from .map or .lvl file
def load_map_file(file_folder, file):
    # Read all the data from the file
    file = open(file_folder + "/" + file, "r")
    data = file.read()
    file.close()
    
    # Set up the tiles from loaded data
    file = []
    for line in data.split("\n"):
        row = [item.strip('"') for item in line.strip().split(',')]
        file.append(row)
    
    return file


def add_predefined_entity(entity, map, data=None):
    """
    Helper function to create list of entity and associated data (x and y coords)
    Searches for predefined entities in map file and adds them to the level

    Args:
        entity (str): name of entity, matching names in entities.json, e.g. "player"
        map: matrix data of map
    
    Returns:
        entity_data (list): list containing 3 items: entity factory number, x coord, y coord. e.g. [0, 26, 3]
    """

    entity_list = []
    try:
        for y, row in enumerate(map):
            for x, tile in enumerate(row):
                if tile == entities[entity]["start"]:
                    entity_data = []
                    factory_type = str(entities[entity]["factory"])
                    entity_data.append(factory_type)
                    entity_data.append(str(x))
                    entity_data.append(str(y))
                    if data != None:
                        entity_data.append(data)
                    entity_list.append(entity_data)
    except:
        logging.error(f"error whilst assigning {entity} entity during add_predefined_entity() func")

    return entity_list


def add_random_entity(entity, map, coverage):
    """
    Helper function to create list of entity and associated data (x and y coords)
    Randomly places entities in level according to coverage threshold

    Args:
        entity (str): name of entity, matching names in entities.json, e.g. "player"
        map: matrix data of map
        coverage (float): proportion of open space in map to be occupied by chosen entity
    
    Returns:
        entity_data (list): list containing entity factory number, x coord, y coord, any other variables such as item type, quantity e.g. [6, 26, 3, 0, 5]
    """

    valid_tiles = 0
    valid_tile_type = entities[entity]["start"]
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if tile == valid_tile_type:
                valid_tiles += 1
    
    entities_to_add = int(ceil(valid_tiles * coverage))
    map_width = len(map[0])
    map_height = len(map)

    entity_list = []
    try:
        while entities_to_add > 0:
            x = randrange(0,map_width)
            y = randrange(0,map_height)
            if map[y][x] == valid_tile_type:
                # TODO: tidy this code, to be more optimised
                quantity = randrange(0,4)
                entity_data = []
                factory_type = str(entities[entity]["factory"])
                entity_data.append(factory_type)
                entity_data.append(str(x))
                entity_data.append(str(y))
                entity_data.append(str(0))          # currently hardcoded to gold item.     TODO: add more functionality
                entity_data.append(str(quantity))   # currently adding a random quantity.   TODO: add more functionality
                entity_list.append(entity_data)
                entities_to_add -= 1
    except:
        logging.error(f"error whilst assigning {entity} entity during add_predefined_entity() func")

    return entity_list


# function to add mobs , including player
def populate_map(map):
    entity_list = []

    # Add stairs
    entity_list.extend(add_predefined_entity("stairs_up", map, "^"))
    entity_list.extend(add_predefined_entity("stairs_down", map, "v"))

    # Add doors
    entity_list.extend(add_predefined_entity("door", map))

    # Add items
    entity_list.extend(add_random_entity("item", map, 0.1))

    # Add Player
    entity_list.extend(add_predefined_entity("player", map))

    return entity_list


# helper function to randomly generate mobs
# ...


# function to write level file
def write_level_to_file(fog, entities, lvl_num):
    try:
        file_name = SAVE_NAME + "_" + str(lvl_num) + ".lvl"
        with open(LEVEL_FOLDER + "/" + file_name, 'w') as level_file:

            # add fog to file
            for row in fog:
                data_to_write = '"' + '","'.join(row) + '"'
                level_file.write(data_to_write)
                level_file.write('\n')
            
            # add chunk break ('-')
            level_file.write('-')
            level_file.write('\n')

            # add entities
            for entity_counter, entity in enumerate(entities):
                for item_counter, value in enumerate(entity):
                    level_file.writelines(value)
                    if item_counter != len(entity) - 1:
                        level_file.write(',')
                if entity_counter != len(entities) - 1:
                    level_file.write('\n')

    except:
        logging.error("error whilst writing level to file")


def level_maker(lvl_num):
    map_file = SAVE_NAME + "_" + str(lvl_num) + ".map"
    map = load_map_file(MAP_FOLDER, map_file)
    fog = create_fog(map)
    entity_list = populate_map(map)
    write_level_to_file(fog, entity_list, lvl_num)


if __name__ == "__main__":
    level_maker(lvl_num=1)