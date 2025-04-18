from core.engine import Engine, lvl_num
from core.levelmaker import level_maker
from core.mapmaker import map_maker
from stages.menu import menu
from stages.play import play

## The following preserved from old main
## is used to make the initial map & level
## TODO: need to find a way to elegantly incorporate this
## might be handled during next step (menu step)
map_maker(lvl_num)
level_maker(lvl_num)
# level_name = save_name + "_1.lvl"
# level = Level(level_name, tile_kinds)

e = Engine("Red Mouse Dungeon Crawler")
e.register("Menu", menu)
e.register("Play", play)
e.switch_to("Menu")
e.run()