from components.enemy import Enemy
from components.entity import Entity
from components.inventory import DroppedItem
from components.physics import Body
from components.player import Player
from components.sprite import Sprite
from components.navigator import Navigator
from components.npc import NPC
from components.usable import Changeable

from data.config import TILE_SIZE
from data.item_types import item_types
from data.npc_types import npc_types

entity_factories = [
    # 0 - Makes a Player
    lambda args: Entity(Player(100), Sprite("char", "formicid.png"), Body()),

    # 1 - Makes an Up Stair
    lambda args: Entity(Navigator(args[3]), Sprite("dngn", "stone_stairs_up.png")),

    # 2 - Makes a Down Stair
    lambda args: Entity(Navigator(args[3]), Sprite("dngn", "stone_stairs_down.png")),

    # 3 - Makes a Door
    lambda args: Entity(Sprite("dngn", "closed_door.png"), Body(blocks_vision=True), Changeable("door")),

    # 4 - Makes a Mob
    lambda args: Entity(Sprite("char", "draconian_green.png", is_permanent=False), Enemy(20, 1), Body()),

    # 5 - Makes an Item
    lambda args: Entity(
                    DroppedItem(item_types[int(args[3])], int(args[4])), 
                    Sprite("item", item_types[int(args[3])].icon_name)
        ),
    
    # 6 - Makes an NPC
    lambda args: Entity(
                    Sprite("char", npc_types[int(args[3])]["image"]), 
                    NPC(npc_types[int(args[3])]["name"], npc_types[int(args[3])]["npc_file"])
        )
]


def create_entity(id, x, y, data=None):
    factory = entity_factories[id]
    e = factory(data)
    e.id = id
    e.x = x * TILE_SIZE
    e.y = y * TILE_SIZE
    e.data = data
    return e
