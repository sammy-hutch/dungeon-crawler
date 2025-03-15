# functions to take the basic map file and enrich it with
#  - start location
#  - starting mobs
#  - items
#  - features (altars, portals, etc)
# etc

import os
from dotenv import load_dotenv
import logging

load_dotenv()

level_folder = os.getenv("LEVEL_FOLDER")
map_folder = os.getenv("MAP_FOLDER")

map_file = "start.map"
level_file = "start.lvl"


# function to extract data from .map or .lvl file
def load_file(file_folder, file):
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


# function to create stairs up entity
def stairs_up_entity(map):
    entity = []
    factory_type = str(1)
    entity.append(factory_type)
    try:
        for y, row in enumerate(map):
            for x, tile in enumerate(row):
                if tile == "^":
                    entity.append(str(x))
                    entity.append(str(y))
    except:
        logging.error("no valid location found during stairs_up_entity() func")
    return entity


# function to create stairs down entity
def stairs_down_entity(map):
    entity = []
    factory_type = str(2)
    entity.append(factory_type)
    try:
        for y, row in enumerate(map):
            for x, tile in enumerate(row):
                if tile == "v":
                    entity.append(str(x))
                    entity.append(str(y))
    except:
        logging.error("no valid location found during stairs_down_entity() func")
    return entity


# function to create player entity
def player_entity(map):
    entity = []
    factory_type = str(0)
    entity.append(factory_type)
    try:
        for y, row in enumerate(map):
            for x, tile in enumerate(row):
                if tile == "^":
                    entity.append(str(x))
                    entity.append(str(y))
    except:
        logging.error("no valid location found during player_entity() func")
    return entity

# function to add mobs , including player
# def entity_list(map):
#     entities = []



# function to randomly generate mobs


# function to write level file
def write_level_to_file(level, entities):
    try:
        with open(level_folder + "/" + 'start.lvl', 'w') as level_file:

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


def level_maker(map_file, level_file):
    map = load_file(map_folder, map_file)
    level = load_file(level_folder, level_file)
    entities = []
    stairs_up = stairs_up_entity(map)
    entities.append(stairs_up)
    stairs_down = stairs_down_entity(map)
    entities.append(stairs_down)
    player = player_entity(map)
    entities.append(player)
    write_level_to_file(map, entities)


if __name__ == "__main__":
    level_maker(map_file, level_file)