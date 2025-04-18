from components.entity import Entity
from components.physics import Body
from components.player import Player
from components.sprite import Sprite
from components.navigator import Navigator
from data.config import TILE_SIZE

entity_factories = [
    # 0 - Makes a Player
    lambda args: Entity(Player(), Sprite("char", "formicid.png"), Body()),

    # 1 - Makes an Up Stair
    lambda args: Entity(Navigator(args[3]), Sprite("dngn", "stone_stairs_up.png")),

    # 2 - Makes a Down Stair
    lambda args: Entity(Navigator(args[3]), Sprite("dngn", "stone_stairs_down.png")),

    # 3 - Makes a Door
    lambda args: Entity(Sprite("dngn", "closed_door.png")),

    # 4 - Makes a Mob
    lambda args: Entity(Sprite("char", "..."), Body()),

    # 5 - Makes an Item
    lambda args: Entity(Sprite("char", "..."), Body())
]


def create_entity(id, x, y, data=None):
    factory = entity_factories[id]
    e = factory(data)
    e.id = id
    e.x = x * TILE_SIZE
    e.y = y * TILE_SIZE
    e.data = data
    return e
