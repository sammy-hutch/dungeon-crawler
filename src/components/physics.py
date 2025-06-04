from pygame import Rect
from data.config import TILE_SIZE

# set default hitbox size to be 1 pixel smaller on every side than the tile
hitbox_x = 1
hitbox_y = 1
hitbox_width = TILE_SIZE - 2
hitbox_height = TILE_SIZE - 2

bodies = []
triggers = []

def reset_physics():
    global bodies, triggers
    bodies.clear()
    triggers.clear()

class PhysicalObj:
    def __init__(self, x, y, width, height):
        self.hitbox = Rect(x, y, width, height)
    
    def is_colliding_with(self, other):
        x = self.entity.x + self.hitbox.x
        y = self.entity.y + self.hitbox.y
        other_x = other.entity.x + other.hitbox.x
        other_y = other.entity.y + other.hitbox.y

        if x < other_x + other.hitbox.width and \
            x + self.hitbox.width > other_x and \
            y < other_y + other.hitbox.height and \
            y + self.hitbox.height > other_y:
            return True
        else:
            return False
        

class Trigger(PhysicalObj):
    def __init__(self, on, x=0, y=0, width=TILE_SIZE, height=TILE_SIZE):
        super().__init__(x, y, width, height)
        triggers.append(self)
        self.on = on

    def breakdown(self):
        global triggers
        triggers.remove(self)

class Body(PhysicalObj):
    def __init__(self, x=hitbox_x, y=hitbox_y, width=hitbox_width, height=hitbox_height):
        super().__init__(x, y, width, height)
        bodies.append(self)
        self.is_solid = True
    
    def breakdown(self):
        global bodies
        bodies.remove(self)
    
    def is_position_valid(self):
        from core.map import map
        x = self.entity.x + self.hitbox.x
        y = self.entity.y + self.hitbox.y
        if map.is_rect_solid(x, y, self.hitbox.width, self.hitbox.height):
            return False
        for body in bodies:
            if body != self and body.is_colliding_with(self) and body.is_solid == True:
                return False
        return True

        