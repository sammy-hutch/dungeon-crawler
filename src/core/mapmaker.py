import os
from dotenv import load_dotenv
from random import randrange, choice, shuffle
import json
import logging

load_dotenv()

map_width = int(os.getenv("MAP_WIDTH"))
map_height = int(os.getenv("MAP_HEIGHT"))
map_coverage_threshold = float(os.getenv("MAP_COVERAGE_THRESHOLD")) 

data_folder = os.getenv("DATA_FOLDER")
map_folder = os.getenv("MAP_FOLDER")

# handle tile data file
tile_file = open(data_folder + "/" + 'tiles.json',)
tiles = json.load(tile_file)
tile_file.close()
tile_list = tiles["tiles"]
# available_tiles: list[str] = [tile['id'] for tile in tile_list]
# available_tiles = []
# for tile in tile_list:
#     probability = tile['probability']
#     available_tiles.extend(tile['id'] for tile in range(probability))
available_tiles = [tile["id"] for tile in tile_list for _ in range(tile["probability"])]
# print(available_tiles)
ignored_tile_types = ["w"]



def no_empty_tiles(schema, empty_tile) -> bool:
    """
    Checks if schema is complete, i.e. no undefined fields.
    """
    for i, row in enumerate(schema):
        for i, v in enumerate(row):
            if v == empty_tile:
                return False
    return True


# Helper function to get a tile's edge
def get_edge(tile_id: str, side: str):
    """
    Helper function to get a tile's edge.

    Args:
        tile_id (str): the id of the tile to get the edge of, e.g. "042".
        side (str): the side of the tile to get the edge of. Handles cardinal directions, i.e. "N","E","S" or "W"
    
    Returns:
        edge (list[str]): the config of the tile's edge, e.g. ["w","w","f"]
    """

    tile_data = next((t for t in tile_list if t["id"] == tile_id), None)
    if tile_data is None:
        return None  # Or raise an exception if a missing tile is an error TODO: review this
    if side == "W": return [row[0] for row in tile_data['config']]
    if side == "E": return [row[2] for row in tile_data['config']]
    if side == "N": return tile_data['config'][0]
    if side == "S": return tile_data['config'][2]
    return None

# Helper function to get a tile's corner
def get_corner(tile_id: str, directions: list[str]):
    """
    Helper function to get a tile's corner.

    Args:
        tile_id (str): the id of the tile to get the edge of, e.g. "042".
        directions (list[str]): the cardinal directions of the corner, e.g. ["N","E"] or ["S","W"]
    
    Returns:
        corner (str): the config of the tile's corner, e.g. "w"
    """
    
    tile_data = next((t for t in tile_list if t["id"] == tile_id), None)
    if tile_data is None:
        return None  # Or raise an exception if a missing tile is an error TODO: review this
    if "W" in directions and "N" in directions: return tile_data['config'][0][0]
    if "N" in directions and "E" in directions: return tile_data['config'][0][2]
    if "E" in directions and "S" in directions: return tile_data['config'][2][2]
    if "S" in directions and "W" in directions: return tile_data['config'][2][0]
    return None

# TODO: add exceptions/logging
def tile_borders_match(tile, schema, x, y, empty_tile) -> bool:
    """
    Helper function to check if the current tile's borders match the neighbouring tiles' borders.

    Args:
        tile (str): id of currently selected tile
        schema (list[list[]]): matrix overview of current schema
        x (int): x-axis position of current tile in schema
        y (int): y-axis position of current tile in schema
        empty_tile: the default value of empty tile, for identifying if current and neighbouring tiles are empty
    """

    current_tile_data = next((t for t in tile_list if t["id"] == tile), None)
    if current_tile_data is None:  # Handle the case where the tile is not found # TODO: review this
        return False
    
    # set neighbour values
    n_tile = schema[y-1][x] if y > 0 else "001"
    ne_tile = schema[y-1][x+1] if x < len(schema[0]) - 1 and y > 0 else "001"
    e_tile = schema[y][x+1] if x < len(schema[0]) - 1 else "001"
    se_tile = schema[y+1][x+1] if x < len(schema[0]) - 1 and y < len(schema) -1 else "001"
    s_tile = schema[y+1][x] if y < len(schema) - 1 else "001"
    sw_tile = schema[y+1][x-1] if x > 0 and y < len(schema) -1 else "001"
    w_tile = schema[y][x-1] if x > 0 else "001"
    nw_tile = schema[y-1][x-1] if x > 0 and y > 0 else "001"

    # Check neighbors
    if n_tile != empty_tile and get_edge(tile, "N") != get_edge(n_tile, "S"): return False
    if ne_tile != empty_tile and get_corner(tile, ["N", "E"]) != get_corner(ne_tile, ["S", "W"]): return False
    if e_tile != empty_tile and get_edge(tile, "E") != get_edge(e_tile, "W"): return False
    if se_tile != empty_tile and get_corner(tile, ["S", "E"]) != get_corner(se_tile, ["N", "W"]): return False
    if s_tile != empty_tile and get_edge(tile, "S") != get_edge(s_tile, "N"): return False
    if sw_tile != empty_tile and get_corner(tile, ["S", "W"]) != get_corner(sw_tile, ["N", "E"]): return False
    if w_tile != empty_tile and get_edge(tile, "W") != get_edge(w_tile, "E"): return False
    if nw_tile != empty_tile and get_corner(tile, ["N", "W"]) != get_corner(nw_tile, ["S", "E"]): return False
    return True

def navigable_tile_dict(basic_map, ignored_tile_types):
    """
    Helper function which produces dict of navigable tiles

    Args:
        basic_map (list[list[str]]): matrix of tiles
        ignored_tile_types (list[str]): list of values in matrix which are non navigable and thus should be ignored
    
    Returns:
        tile_groups (list[dict()]): a list of dict entries where each entry is a navigable tile in the map. entries include:
            group: the grouping of tiles to which this particular tile belongs
            y: the y-coordinate of the tile in the map
            x: the x-coordinate of the tile in the map
    """
    tile_groups = []
    group_counter = 0

    ## enumerate through each tile in the basic map
    for y_index, row in enumerate(basic_map):
        for x_index, tile in enumerate(row):

            ## only consider non-wall tiles
            if tile not in ignored_tile_types:
                current_tile = {"group": 0, "y": y_index, "x": x_index}
                neighbour_groups = []

                ## check if bordering any neighbour tiles
                for neighbour in tile_groups:
                    # W neighbour
                    if neighbour["y"] == y_index and neighbour["x"] == x_index - 1:
                        neighbour_groups.append(neighbour["group"])
                    # NW neighbour
                    if neighbour["y"] == y_index - 1 and neighbour["x"] == x_index - 1:
                        neighbour_groups.append(neighbour["group"])
                    # N neighbour
                    if neighbour["y"] == y_index - 1 and neighbour["x"] == x_index:
                        neighbour_groups.append(neighbour["group"])
                    # NE neighbour
                    if neighbour["y"] == y_index - 1 and neighbour["x"] == x_index + 1:
                        neighbour_groups.append(neighbour["group"])
                
                ## add tile to existing group and update neighbour values
                if neighbour_groups:
                    current_tile["group"] = min(neighbour_groups)
                    for group in neighbour_groups:
                        for tile in tile_groups:
                            if tile["group"] == group and tile["group"] != current_tile["group"]:
                                tile["group"] = current_tile["group"]
                    tile_groups.append(current_tile)
                ## else create new group if no adjacent groups
                else:
                    group_counter += 1
                    current_tile["group"] = group_counter
                    tile_groups.append(current_tile)
    
    return tile_groups


def tile_group_volumes(tile_groups):
    """
    Helper function to count how many tiles in each tile group.

    Args:
        tile_groups: product of navigable_tile_dict() function
    Returns:
        groups: dict of group number (key) and that group's volume (value)
    """

    groups = {}
    for tile in tile_groups:
        if tile["group"] in groups:
            groups[tile["group"]] += 1
        else:
            groups.update({tile["group"]: 1})
    # print(groups)
    # print(f"number of groups: {len(groups)}")

    return groups

def valid_stair_placements(tile_groups, group_index):
    """
    Helper function which creates a list of valid stair placements.

    Args:
        tile_groups: product of navigable_tiles_dict() helper function
        group_index: the tile group for which to check
    """

    # create list of only the tiles for the relevant group
    group = [entry for entry in tile_groups if entry.get('group') == group_index]

    # check if location is valid for stairs (surrounded by room tiles)
    valid_stair_locations = []
    for current_tile in group:
        x = current_tile["x"]
        y = current_tile["y"]
        neighbours = 0
        for comparison_tile in group:
            # TODO: check against all cardinal neighbours. if all 8 are in group, it is valid location
            if (
                   (comparison_tile["x"] == x     and comparison_tile["y"] == y - 1) # N
                or (comparison_tile["x"] == x + 1 and comparison_tile["y"] == y - 1) # NE
                or (comparison_tile["x"] == x + 1 and comparison_tile["y"] == y)     # E
                or (comparison_tile["x"] == x + 1 and comparison_tile["y"] == y + 1) # SE
                or (comparison_tile["x"] == x     and comparison_tile["y"] == y + 1) # S
                or (comparison_tile["x"] == x - 1 and comparison_tile["y"] == y + 1) # SW
                or (comparison_tile["x"] == x - 1 and comparison_tile["y"] == y)     # W
                or (comparison_tile["x"] == x - 1 and comparison_tile["y"] == y - 1) # NW
            ):
                neighbours += 1
        if neighbours == 8:
            valid_stair_locations.append(current_tile)
    
    # find the distance between each pair of locations
    location_diffs = []
    for i, curr_tile in enumerate(valid_stair_locations):
        for j, comp_tile in enumerate(valid_stair_locations):
            if j > i: # only take later items in list to only compare each pair once
                x = abs(comp_tile["x"] - curr_tile["x"])  # find x diff
                y = abs(comp_tile["y"] - curr_tile["y"])  # find y diff
                diff =  round((x**2 + y**2)**0.5)  # find straight-line distance
                entry = {
                    "x1": curr_tile["x"], 
                    "y1": curr_tile["y"], 
                    "x2": comp_tile["x"], 
                    "y2": comp_tile["y"],
                    "diff": diff
                    }
                location_diffs.append(entry)

    # Check if there is at least one pair at a valid distance
    valid_pairs = [p for p in location_diffs if p["diff"] >= 5]
    return valid_pairs

def set_stair_placement(location_pairs):
    """
    Function to set the location of the entry and exit stairs.

    Args:
        location_pairs: list of valid stair pair locations. Output of valid_stair_placements() function.
    Returns:
        stair_placements: dict with coordinates of entry and exit stairs
    """
    # in future, logic could be adjusted to make it any pair which is above a certain distance apart,
    # not necessarily the furthest pair
    
    max_diff = max(d["diff"] for d in location_pairs)
    candidates = [d for d in location_pairs if d["diff"] == max_diff]
    furthest_pair = choice(candidates)
    pair_list = [
        {"x": furthest_pair["x1"], "y": furthest_pair["y1"]},
        {"x": furthest_pair["x2"], "y": furthest_pair["y2"]}
        ]
    shuffle(pair_list)
    stair_placements = {
        "entry": pair_list[0],
        "exit": pair_list[1]
        }    
    return stair_placements


def build_schema(map_width: int, map_height: int, available_tiles: list[str]):
    """
    Builds 'schema', which is high-level overview of map layout.

    Args:
        map_width (int): how many 'chunks' wide the map is
        map_height (int): how many 'chunks' tall the map is
        available_tiles (list[str]): the tiles to choose from when building the schema
    Returns:
        schema (list[list[str]]): a matrix of size map_width * map_height
    """

    empty_tile = 3
    complete_schema: bool = False
    schema = [[empty_tile for _ in range(map_width)] for _ in range(map_height)]

    try:
        while not complete_schema:
            x = randrange(0,map_width)
            y = randrange(0,map_height)
            if schema[y][x] == empty_tile:
                valid_remaining_tiles = available_tiles.copy()
                valid_tile_placement = False
                while not valid_tile_placement:
                    tile = choice(valid_remaining_tiles)
                    if tile_borders_match(tile, schema, x, y, empty_tile):
                        schema[y][x] = tile
                        valid_tile_placement = True
                    else: 
                        valid_remaining_tiles = [j for j in valid_remaining_tiles if j != tile]
            if no_empty_tiles(schema, empty_tile):
                complete_schema = True
    except:
        logging.error("Error whilst building schema")
    
    return schema


def build_basic_map(schema: list[list[str]], tile_list: json):
    """
    Builds basic map by pulling schema tile info from tile list.

    Args:
        schema (list[list[str]]): a matrix of tile IDs
        tile_list (json): a data file of tile info
    
    Returns:
        basic_map (list[list[str]]): a matrix of tiles
    """

    basic_map = []

    try: 
        for row in schema:
            for sub_row in range(3):
                detail_grid_row = []
                for chunk in row:
                    for tile in tile_list:
                        if tile['id'] == chunk:
                            for value in tile['config'][sub_row]:
                                detail_grid_row.append(value)
                basic_map.append(detail_grid_row)
    except:
        logging.error("error whilst building basic map")

    return basic_map


def map_accessibility_checks(basic_map, map_coverage_threshold):
    ## function to hold various accessibility checks for the map
    # TODO: break this up into smaller functions within the mapmaker handler

    map_tile_count_y = len(basic_map)
    map_tile_count_x = len(basic_map[0])
    map_size = map_tile_count_y * map_tile_count_x

    tile_groups = navigable_tile_dict(basic_map, ignored_tile_types)
    group_volumes = tile_group_volumes(tile_groups)

    largest_group_key = max(group_volumes, key=group_volumes.get)
    largest_group_volume = group_volumes[largest_group_key]

    ## map_coverage_check
    if  largest_group_volume / map_size < map_coverage_threshold:
        # print(f"map coverage check not passed. map size: {map_size}. largest group: {largest_group_volume}")
        return False
    # else:
    #     print(f"map coverage check passed. map size: {map_size}. largest group: {largest_group_volume}")
    
    ## valid stair placement check
    valid_pairs = valid_stair_placements(tile_groups, largest_group_key)
    if len(valid_pairs) < 1:
        return False
    
    stair_placements = set_stair_placement(valid_pairs)
    return stair_placements


def build_enriched_map(basic_map, stairs):
    """
    Adds stairs, water, holes and other static features to the map

    Args
        basic_map: the output of build_basic_map() function. A matrix of the tiles in the map
        stairs: the output of map_accessibility_checks() function. the locations of entry and exit stairs
    """
    # TODO: enrich map with water, items, holes, etc

    # add stairs to map
    entry_x = stairs["entry"]["x"]
    entry_y = stairs["entry"]["y"]
    exit_x = stairs["exit"]["x"]
    exit_y = stairs["exit"]["y"]
    basic_map[entry_y][entry_x] = "^"
    basic_map[exit_y][exit_x] = "v"

    return basic_map


def write_map_to_file(map, lvl_num):
    try:
        file_name = "test" + str(lvl_num) + ".map"
        with open(map_folder + "/" + file_name, 'w') as map_file:
            for counter, row in enumerate(map):
                data_to_write = '"' + '","'.join(row) + '"'
                map_file.write(data_to_write)
                if counter != len(map) - 1:
                    map_file.write('\n')
    except:
        logging.error("error whilst writing map to file")


def map_maker(lvl_num):
    valid_map = False
    while not valid_map:
        schema = build_schema(map_width, map_height, available_tiles)
        basic_map = build_basic_map(schema, tile_list)
        stair_placements = map_accessibility_checks(basic_map, map_coverage_threshold)
        if stair_placements:
            valid_map = True
    enriched_map = build_enriched_map(basic_map, stair_placements)
    write_map_to_file(enriched_map, lvl_num)

if __name__ == "__main__":

    schema = build_schema(map_width, map_height, available_tiles)

    print("")
    print("schema")
    for row in schema:

        print(row)

    basic_map = build_basic_map(schema, tile_list)

    print("")
    print("basic map:")
    for row in basic_map:
        print(row)
    
    stair_placements = map_accessibility_checks(basic_map, map_coverage_threshold)
    
    enriched_map = build_enriched_map(basic_map, stair_placements)
    
    write_map_to_file(basic_map)