# functions to take the basic map file and enrich it with
#  - start location
#  - starting mobs
#  - items
#  - features (altars, portals, etc)
# etc

import logging

level_folder = "content/levels"
map_folder = "content/maps"

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


# function to set start location
def start_location(map):
    start_location = {"y": 0, "x": 0}
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if tile == "^":
                start_location["y"] = str(y)
                start_location["x"] = str(x)
                return start_location
    return logging.error("no start location found during start_location() func")


# function to create player entity
def player_entity(start_location):
    entity = []
    factory_type = str(0)
    entity.append(factory_type)
    player_x = start_location["x"]
    entity.append(player_x)
    player_y = start_location["y"]
    entity.append(player_y)
    # entity.append(factory_type, player_x, player_y)
    # entity = list(factory_type, player_x, player_y)
    return entity

# function to add mobs , including player
# def entity_list(map):
#     entities = []



# function to randomly generate mobs


# function to write level file
def write_level_to_file(level, player_entity_data):
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
            for counter, value in enumerate(player_entity_data):
                level_file.writelines(value)
                if counter != len(player_entity_data) - 1:
                    level_file.write(',')


    except:
        logging.error("error whilst writing level to file")


def level_maker(map_file, level_file):
    map = load_file(map_folder, map_file)
    level = load_file(level_folder, level_file)
    start = start_location(map)
    player_entity_data = player_entity(start)
    write_level_to_file(map, player_entity_data)


if __name__ == "__main__":
    level_maker(map_file, level_file)