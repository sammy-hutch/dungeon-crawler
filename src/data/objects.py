import os
from dotenv import load_dotenv
from components.entity import Entity
from components.sprite import Sprite
from components.player import Player
from components.physics import Body

load_dotenv()

tile_size = int(os.getenv("TILE_SIZE"))

entity_factories = [
    # 0 - Make a Player
    lambda args: Entity(Player(), Sprite("formicid.png"), Body()),

    # 1 - Make a Mob
    lambda args: Entity(Sprite("..."), Body()),

    # 2 - Make an Item
    lambda args: Entity(Body()),
]


def create_entity(id, x, y, data=None):
    factory = entity_factories[id]
    e = factory(data)
    e.x = x * tile_size
    e.y = y * tile_size
    return e
