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

def get_bodies_within_circle(circle_x, circle_y, radius):
    items = []
    for body in bodies:
        if body.is_circle_colliding_with(circle_x, circle_y, radius):
            items.append(body)
    return items

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
    
    def is_circle_colliding_with(self, circle_x, circle_y, radius):
        body_x = self.entity.x + self.hitbox.x
        body_y = self.entity.y + self.hitbox.y
        circle_dist_x = abs(circle_x - body_x)
        circle_dist_y = abs(circle_y - body_y)

        if circle_dist_x > (self.hitbox.width/2 + radius):
            return False
        if circle_dist_y > (self.hitbox.height/2 + radius):
            return False
        if circle_dist_x <= (self.hitbox.width/2):
            return True
        if circle_dist_y <= (self.hitbox.height/2):
            return True

        corner_dist_squared = (circle_dist_x - self.hitbox.width/2)**2 + \
                                (circle_dist_y - self.hitbox.height/2)**2
        
        return corner_dist_squared <= radius**2
        

class Trigger(PhysicalObj):
    def __init__(self, on, x=0, y=0, width=TILE_SIZE, height=TILE_SIZE):
        super().__init__(x, y, width, height)
        triggers.append(self)
        self.on = on

    def breakdown(self):
        global triggers
        triggers.remove(self)

class Body(PhysicalObj):
    def __init__(self, x=hitbox_x, y=hitbox_y, width=hitbox_width, height=hitbox_height, blocks_vision=False, is_solid=True):
        super().__init__(x, y, width, height)
        bodies.append(self)
        self.is_solid = is_solid
        self.blocks_vision = blocks_vision
        # TODO: add a components args field (e.g. to hold blocks_vision) and use add() function to add them to the  body (see entity.py for logic)
    
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

        