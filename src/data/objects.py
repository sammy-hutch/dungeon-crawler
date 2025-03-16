import os
from dotenv import load_dotenv
from components.entity import Entity
from components.sprite import Sprite
from components.player import Player
from components.physics import Body

load_dotenv()

tile_size = int(os.getenv("TILE_SIZE"))

entity_factories = [
    # 0 - Makes a Player
    lambda args: Entity(Player(), Sprite("formicid.png"), Body()),

    # 1 - Makes an Up Stair
    lambda args: Entity(Sprite("stone_stairs_up.png")),

    # 2 - Makes a Down Stair
    lambda args: Entity(Sprite("stone_stairs_down.png")),

    # 3 - Makes a Mob
    lambda args: Entity(Sprite("..."), Body()),

    # 4 - Makes an Item
    lambda args: Entity(Body()),
]


def create_entity(id, x, y, data=None):
    factory = entity_factories[id]
    e = factory(data)
    e.x = x * tile_size
    e.y = y * tile_size
    return e
