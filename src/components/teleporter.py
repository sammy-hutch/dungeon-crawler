from components.physics import Trigger
from components.player import Player

def teleport(level_file):
    from core.level import level
    level.load_file(level_file)

class Teleporter(Trigger):
    def __init__(self, level_file, x=0, y=0, width=32, height=32):
        super().__init__(lambda: teleport(level_file), x, y, width, height)