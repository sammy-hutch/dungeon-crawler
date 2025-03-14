import os
from dotenv import load_dotenv
from pygame import Rect

load_dotenv()

# set default hitbox size to be 1 pixel smaller on every side than the tile
tile_size = int(os.getenv("TILE_SIZE"))
hitbox_x = 1
hitbox_y = 1
hitbox_width = tile_size - 2
hitbox_height = tile_size - 2

bodies = []

class Body:
    def __init__(self, x=hitbox_x, y=hitbox_y, width=hitbox_width, height=hitbox_height):
        self.hitbox = Rect(x, y, width, height)
        bodies.append(self)
    
    def is_position_valid(self):
        from core.map import map
        x = self.entity.x + self.hitbox.x
        y = self.entity.y + self.hitbox.y
        if map.is_rect_solid(x, y, self.hitbox.width, self.hitbox.height):
            return False
        for body in bodies:
            if body != self and body.is_colliding_with(self):
                return False
        return True
    
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
        