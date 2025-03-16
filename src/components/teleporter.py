import os
from dotenv import load_dotenv

from core.mapmaker import map_maker
from core.levelmaker import level_maker
from components.physics import Trigger
from components.player import Player

load_dotenv()

lvl_num = 1
path = "./" + os.getenv("LEVEL_FOLDER") + "/start.lvl"

def teleport(direction):
    global lvl_num
    from core.level import level
    print(f"before teleport, level number: {lvl_num}")

    if direction == "^":
        lvl_num -= 1
    if direction == "v":
        lvl_num += 1

    level_file = "test" + str(lvl_num) + ".lvl"
    level_file_path = "./" + os.getenv("LEVEL_FOLDER") + "/" + level_file

    path_exists = os.path.exists(level_file_path)
    print(f"file path exists: {path_exists}")

    if not os.path.exists(level_file_path):
        map_maker(lvl_num)
        level_maker(lvl_num)
    level.load_file(level_file)
    print(f"after teleport, level number: {lvl_num}")

class Teleporter(Trigger):
    def __init__(self, direction, x=0, y=0, width=32, height=32):
        super().__init__(lambda: teleport(direction), x, y, width, height)