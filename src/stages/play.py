from core.level import Level
from data.tile_types import tile_kinds
from data.config import SAVE_NAME

def play():
    from core.engine import engine
    file = SAVE_NAME + "_" + str(engine.lvl_num) + ".lvl"
    Level(file, tile_kinds)