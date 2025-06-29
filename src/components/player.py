import pygame

from components.enemy import Enemy
from components.entity import Entity
from components.inventory import Inventory
from components.label import Label
from components.physics import Body, triggers
from components.sprite import Sprite
from components.ui.bar import Bar
from components.ui.inventory_view import InventoryView

from core.camera import camera
from core.input import is_key_pressed

from data.config import TILE_SIZE
from data.key_binds import key_binds


# player moves one tile per key press
movement_speed = TILE_SIZE
message_time_seconds = 3

inventory = Inventory(20)

def on_player_death(entity):
    from stages.menu import new_game
    new_game()

class Player:
    def __init__(self, health):
        self.health = health
        from core.engine import engine
        from core.level import level

        # Create Labels
        self.loc_label = Entity(Label("RedRose-Regular.ttf", "X: 0 - Y: 0")).get(Label)
        self.message_label = Entity(Label("RedRose-Regular.ttf", level.name)).get(Label)
        self.inventory_window = Entity(InventoryView(inventory))

        self.loc_label.entity.y = camera.height - 50
        self.loc_label.entity.x = 10
        self.message_label.entity.x = 10
        self.show_message(f"Entering {level.name}")
        
        engine.active_objs.append(self)
    
    def setup(self):
        # Setup combat
        from components.combat import Combat
        combat = Combat(self.health, on_player_death)
        self.entity.add(combat)
        self.combat = combat
        del self.health

        # Setup health bar
        self.health_bar = Entity(Bar(self.combat.max_health, 
                                     (255, 0, 0), 
                                     (0, 255, 0),
                                     "player")).get(Bar)
        self.health_bar.entity.x = camera.width - self.health_bar.width
        self.health_bar.entity.y = camera.height - self.health_bar.height
    
    def update(self):
        from core.engine import engine
        from core.level import level

        if self.message_countdown > 0:
            self.message_countdown -= 1
            if self.message_countdown <= 0:
                self.message_label.set_text("")

        self.loc_label.set_text(f"X: {self.entity.x} - Y: {self.entity.y}")
        previous_x = self.entity.x
        previous_y = self.entity.y
        self.health_bar.amount = self.combat.health
        sprite = self.entity.get(Sprite)
        body = self.entity.get(Body)

        # Update user input
        if engine.changed_player_state == True:
            attempted_move = False
            attempted_attack = False
            target_entity = None

            # Handle mouse clicks
            from core.input import is_mouse_just_pressed
            mouse_pos = pygame.mouse.get_pos()

            if inventory.equipped_changed:
                if self.combat.equipped is not None:
                    self.combat.unequip()
                if inventory.equipped_slot is not None:
                    self.combat.equip(inventory.slots[inventory.equipped_slot].type)
                inventory.equipped_changed = False
            
            if is_mouse_just_pressed(1):
                self.interact(mouse_pos)

            # Handle key presses
            if is_key_pressed(key_binds["navigate_to_menu"]):
                level.save_file()
                engine.switch_to("Menu")
            
            if is_key_pressed(key_binds["interact_current_space"]):
                        for t in triggers:
                            if body.is_colliding_with(t):
                                t.on(self.entity)

            if is_key_pressed(key_binds["move_player_n"]):
                self.entity.y -= movement_speed
                attempted_move = True
            if is_key_pressed(key_binds["move_player_ne"]):
                self.entity.y -= movement_speed
                self.entity.x += movement_speed
                attempted_move = True
            if is_key_pressed(key_binds["move_player_e"]):
                self.entity.x += movement_speed
                attempted_move = True
            if is_key_pressed(key_binds["move_player_se"]):
                self.entity.y += movement_speed
                self.entity.x += movement_speed
                attempted_move = True
            if is_key_pressed(key_binds["move_player_s"]):
                self.entity.y += movement_speed
                attempted_move = True
            if is_key_pressed(key_binds["move_player_sw"]):
                self.entity.y += movement_speed
                self.entity.x -= movement_speed
                attempted_move = True
            if is_key_pressed(key_binds["move_player_w"]):
                self.entity.x -= movement_speed
                attempted_move = True
            if is_key_pressed(key_binds["move_player_nw"]):
                self.entity.y -= movement_speed
                self.entity.x -= movement_speed
                attempted_move = True
            
            # Check if colliding with interactable object
            if attempted_move:
                for usable in engine.usables:
                    if usable.entity.has(Body):
                        usable_body = usable.entity.get(Body)
                        if body.is_colliding_with(usable_body):
                            d = 0
                            usable.on(self.entity, d)
            
            # Check if colliding with enemy
            if attempted_move:
                for a in engine.active_objs:
                    try:
                        if a.entity.has(Enemy):
                            target_body = a.entity.get(Body)
                            if body.is_colliding_with(target_body):
                                target_entity = a.entity
                                attempted_attack = True
                    except:
                        pass
            
            # Check if position is invalid
            if not body.is_position_valid():
                self.entity.x = previous_x
                self.entity.y = previous_y
            
            if attempted_attack:
                from components.combat import Combat
                self.combat.attack(target_entity.get(Combat))
                target_entity = None
        
        camera.x = self.entity.x - camera.width/2 + sprite.image.get_width()/2
        camera.y = self.entity.y - camera.height/2 + sprite.image.get_height()/2
    
    def show_message(self, message):
        self.message_label.set_text(message)
        self.message_countdown = message_time_seconds * 15
    
    def interact(self, mouse_pos):
        from core.engine import engine
        from core.math_ext import dist_to_mouse_target
        attempted_attack = False
        target_entity = None

        # Check if interacting with a usable
        for usable in engine.usables:
            if usable.entity.has(Sprite):
                dist = dist_to_mouse_target(self.entity, usable.entity, mouse_pos, camera)
                # Call the usable function
                if dist is not None:
                    usable.on(self.entity, dist)
        
        # Check if interacting with an enemy
        for a in engine.active_objs:
            try:
                if a.entity.has(Enemy) and a.entity.has(Sprite):
                    dist = dist_to_mouse_target(self.entity, a.entity, mouse_pos, camera)
                    range = 50 # hardcoded. TODO: make dynamic according to item stats
                    # Call the attack function
                    if dist is not None and range > dist:
                        target_entity = a.entity
                        attempted_attack = True
            except:
                pass
        
        if attempted_attack:
            from components.combat import Combat
            self.combat.attack(target_entity.get(Combat))
            target_entity = None