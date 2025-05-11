import pygame

from components.entity import Entity
from components.inventory import Inventory
from components.label import Label
from components.physics import Body, triggers
from components.sprite import Sprite
from components.ui.inventory_view import InventoryView

from core.camera import camera
from core.input import is_key_pressed

from data.config import TILE_SIZE
from data.key_binds import key_binds


# player moves one tile per key press
movement_speed = TILE_SIZE

inventory = Inventory(20)

class Player:
    def __init__(self):
        from core.engine import engine
        from core.level import level

        # Create Labels
        self.loc_label = Entity(Label("RedRose-Regular.ttf", "X: 0 - Y: 0")).get(Label)
        self.level_label = Entity(Label("RedRose-Regular.ttf", level.name)).get(Label)
        self.inventory_window = Entity(InventoryView(inventory))
        self.loc_label.entity.y = camera.height - 50
        self.loc_label.entity.x = 10
        self.level_label.entity.x = 10
        
        engine.active_objs.append(self)
    
    def update(self):
        from core.engine import engine
        from core.level import level

        self.loc_label.set_text(f"X: {self.entity.x} - Y: {self.entity.y}")
        previous_x = self.entity.x
        previous_y = self.entity.y
        sprite = self.entity.get(Sprite)
        body = self.entity.get(Body)

        # Update user input
        if engine.changed_player_state == True:
            attempted_move = False

            # Handle mouse clicks
            from core.input import is_mouse_just_pressed
            mouse_pos = pygame.mouse.get_pos()
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
            
            # Check if position is invalid
            if not body.is_position_valid():
                self.entity.x = previous_x
                self.entity.y = previous_y
        
        camera.x = self.entity.x - camera.width/2 + sprite.image.get_width()/2
        camera.y = self.entity.y - camera.height/2 + sprite.image.get_height()/2
    
    def interact(self, mouse_pos):
        from core.engine import engine
        for usable in engine.usables:
            if usable.entity.has(Sprite):
                usable_sprite = usable.entity.get(Sprite)
                x_sprite = usable.entity.x - camera.x
                y_sprite = usable.entity.y - camera.y
                width_sprite = usable_sprite.image.get_width()
                height_sprite = usable_sprite.image.get_height()

                # Check if the mouse is clicking this
                if x_sprite < mouse_pos[0] < x_sprite + width_sprite and \
                    y_sprite < mouse_pos[1] < y_sprite + height_sprite:
                    my_sprite = self.entity.get(Sprite)

                    from core.math_ext import distance
                    # Calculate the distance between these two sprites, from their centres
                    # TODO: simplify this using tilesizes
                    d = distance(x_sprite + usable_sprite.image.get_width()/2,
                                 y_sprite + usable_sprite.image.get_height()/2,
                                 self.entity.x - camera.x + my_sprite.image.get_width()/2,
                                 self.entity.y - camera.y + my_sprite.image.get_height()/2)

                    # Call the usable function
                    usable.on(self.entity, d)