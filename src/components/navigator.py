import os
from core.levelmaker import level_maker
from core.mapmaker import map_maker
from components.physics import Trigger
from data.config import SAVE_NAME, LEVEL_FOLDER


lvl_num = 1

def navigate(direction):
    """
    Function for managing the current level number, building new levels & maps, and loading level files.

    Args: 
        direction (str): the direction of travel, corresponding to the map space of the stairs, either up ("^") or down ("v").
    """
    global lvl_num
    from core.level import level

    # adjust level number depending on direction of travel
    if direction == "^":
        lvl_num -= 1
    if direction == "v":
        lvl_num += 1

    level_file = SAVE_NAME + "_" + str(lvl_num) + ".lvl"
    level_file_path = "./" + LEVEL_FOLDER + "/" + level_file

    # if travelling to new level, create map and level files
    if not os.path.exists(level_file_path):
        map_maker(lvl_num)
        level_maker(lvl_num)
    
    # load level file
    level.load_file(level_file)

class Navigator(Trigger):
    def __init__(self, direction, x=0, y=0, width=32, height=32):
        super().__init__(lambda: navigate(direction), x, y, width, height)