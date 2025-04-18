from core.engine import Engine
from stages.menu import menu
from stages.play import play

e = Engine("Red Mouse Dungeon Crawler")
e.register("Menu", menu)
e.register("Play", play)
e.switch_to("Menu")
e.run()