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
    lambda args: Entity(Navigator(args['data']), Sprite("dngn", "stone_stairs_up.png")),

    # 2 - Makes a Down Stair
    lambda args: Entity(Navigator(args['data']), Sprite("dngn", "stone_stairs_down.png")),

    # 3 - Makes a Door
    lambda args: Entity(Sprite("dngn", "closed_door.png"), Body(blocks_vision=True), Changeable("door")),

    # 4 - Makes a Mob
    lambda args: Entity(Sprite("char", "draconian_green.png", is_permanent=False), Enemy(20, 1), Body()),

    # 5 - Makes an Item
    lambda args: Entity(
                    DroppedItem(item_types[args['item_type']], args['quantity']), 
                    Sprite("item", item_types[args['item_type']].icon_name)
        ),
    
    # 6 - Makes an NPC
    lambda args: Entity(
                    Sprite("char", npc_types[args['npc_type']]["image"]), 
                    NPC(npc_types[args['npc_type']]["name"], npc_types[args['npc_type']]["npc_file"])
        )
]


def create_entity(entity_data):
    factory = entity_factories[entity_data['entity_type']]
    e = factory(entity_data)
    e.id = entity_data['entity_type']
    e.x = entity_data['x'] * TILE_SIZE
    e.y = entity_data['y'] * TILE_SIZE
    e.data = entity_data
    return e
