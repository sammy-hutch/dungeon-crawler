from random import randrange, choice
import json
import logging


map_width = 10
map_height = 10

# handle tile data file
tile_file = open('data/tiles.json',)
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
    Checks if the current tile's borders match the neighbouring tiles' borders.

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
                    # print(f"tile: {tile}, x: {x}, y: {y}")
                    # print("schema:")
                    # for row in schema:
                    #     print(row)
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

def write_map_to_file(map):
    try:
        with open('maps/start.map', 'w') as map_file:
            for counter, row in enumerate(map):
                data_to_write = '"' + '","'.join(row) + '"'
                map_file.write(data_to_write)
                if counter != len(map) - 1:
                    map_file.write('\n')
    except:
        logging.error("error whilst writing map to file")

# TODO: add function to enrich map with water, items, holes, etc

# TODO: add probability to tiles to improve build

# TODO: add function to rebuild map if all rooms don't join up

# TODO: add tests on tiles.json to check uniqueness of name, id, config

def map_maker():
    schema = build_schema(map_width, map_height, available_tiles)
    basic_map = build_basic_map(schema, tile_list)
    write_map_to_file(basic_map)

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
    
    write_map_to_file(basic_map)