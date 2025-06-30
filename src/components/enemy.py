import random

from components.entity import Entity
from components.physics import Body
from components.ui.bar import Bar

from core.math_ext import distance

from data.config import TILE_SIZE
from data.item_types import item_types

movement_speed = TILE_SIZE

def on_enemy_death(entity):
    from core.engine import engine
    engine.remove_entity(entity)
    from core.effect import Effect
    Effect(entity.x, entity.y, 0, 0, 10, "cloud_misery0.png")

class Enemy:
    def __init__(self, health, weapon_item_id) -> None:
        # Base combat attributes
        self.health = health
        self.weapon = item_types[weapon_item_id]

        # AI Attributes
        self.target = None
        self.targeted_entity = None
        self.vision_range = 150

        # Make updatable
        from core.engine import engine
        engine.active_objs.append(self)
    
    def setup(self):
        # Setup combat
        from components.combat import Combat
        from core.camera import camera
        self.entity.add(Combat(self.health, on_enemy_death))
        self.combat = self.entity.get(Combat)
        self.combat.equip(self.weapon)
        del self.health

        # Setup health bar
        self.health_bar = Entity(Bar(self.combat.max_health, 
                                     (255, 0, 0), 
                                     (0, 255, 0),
                                     "enemy",
                                     width=TILE_SIZE, 
                                     height=TILE_SIZE/16)).get(Bar)
        self.health_bar.entity.x = self.entity.x
        self.health_bar.entity.y = self.entity.y
    
    def breakdown(self):
        from core.engine import engine
        engine.active_objs.remove(self)
        engine.ui_drawables.remove(self.health_bar)
    
    def update_ai(self):
        from components.physics import get_bodies_within_circle
        from components.player import Player
        seen_objects = get_bodies_within_circle(self.entity.x,
                                                self.entity.y,
                                                self.vision_range)
        found_player = False
        for s in seen_objects:
            if s.entity.has(Player):
                self.target = (s.entity.x, s.entity.y)
                self.targeted_entity = s.entity
                found_player = True
        if not found_player:
            self.target = None
            self.targeted_entity = None

    def update(self):
        from core.camera import camera

        self.health_bar.amount = self.combat.health
        self.update_ai()
        
        if self.targeted_entity is not None:
            weapon_range = int(self.combat.equipped.stats['range'])
            dist = distance(self.entity.x, 
                            self.entity.y,
                            self.targeted_entity.x,
                            self.targeted_entity.y)
            if weapon_range > dist:
                from components.combat import Combat
                self.combat.attack(self.targeted_entity.get(Combat))
        
        if self.target is not None:
            body = self.entity.get(Body)
            prev_x = self.entity.x
            prev_y = self.entity.y
            if self.entity.x < self.target[0]:
                self.entity.x += movement_speed
            if self.entity.x > self.target[0]:
                self.entity.x -= movement_speed
            if self.entity.y < self.target[1]:
                self.entity.y += movement_speed
            if self.entity.y > self.target[1]:
                self.entity.y -= movement_speed
            if not body.is_position_valid():
                self.entity.x = prev_x
                self.entity.y = prev_y
        
        self.health_bar.entity.x = self.entity.x
        self.health_bar.entity.y = self.entity.y