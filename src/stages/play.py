import os

from core.levelmaker import level_maker
from core.mapmaker import map_maker
from core.level import Level
from data.tile_types import tile_kinds
from data.config import LEVEL_FOLDER, SAVE_NAME

def play():
    from core.engine import engine
    level_file = SAVE_NAME + "_" + str(engine.lvl_num) + ".lvl"
    level_file_path = "./" + LEVEL_FOLDER + "/" + level_file
    if not os.path.exists(level_file_path):
        map_maker(engine.lvl_num)
        level_maker(engine.lvl_num)
    Level(level_file, tile_kinds)