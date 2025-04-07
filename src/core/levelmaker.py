# functions to take the basic map file and enrich it with
#  - start location
#  - starting mobs
#  - items
#  - features (altars, portals, doors, etc)
# etc

import logging
import json

from data.config import DATA_FOLDER, LEVEL_FOLDER, MAP_FOLDER, SAVE_NAME

map_file = "start.map"
level_file = "start.lvl"

# handle entity data file
entity_file = open(DATA_FOLDER + "/" + 'entities.json',)
entities = json.load(entity_file)
entity_file.close()


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

# function to create level based on map file or existing level file
# ...


def add_entity(entity, map, data=None):
    """
    Helper function to create list of entity and associated data (x and y coords)

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
        logging.error(f"error whilst assigning {entity} entity during add_entity() func")

    return entity_list


# function to add mobs , including player
def populate_map(map):
    entity_list = []

    # Add stairs
    entity_list.extend(add_entity("stairs_up", map, "^"))
    entity_list.extend(add_entity("stairs_down", map, "v"))

    # Add doors
    entity_list.extend(add_entity("door", map))

    # Add Player
    entity_list.extend(add_entity("player", map))

    return entity_list


# helper function to randomly generate mobs
# ...


# function to write level file
def write_level_to_file(level, entities, lvl_num):
    try:
        file_name = SAVE_NAME + "_" + str(lvl_num) + ".lvl"
        with open(LEVEL_FOLDER + "/" + file_name, 'w') as level_file:

            # add level to file
            for row in level:
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
    entity_list = populate_map(map)
    write_level_to_file(map, entity_list, lvl_num)


if __name__ == "__main__":
    level_maker(lvl_num=1)