from components.entity import Entity
from components.label import Label
from components.physics import Body, triggers
from components.sprite import Sprite
from core.camera import camera
from core.input import is_key_pressed
from data.config import TILE_SIZE
from data.key_binds import key_binds


# player moves one tile per key press
movement_speed = TILE_SIZE

class Player:
    def __init__(self):
        from core.engine import engine
        from core.level import level

        # Create Labels
        self.loc_label = Entity(Label("RedRose-Regular.ttf", "X: 0 - Y: 0")).get(Label)
        self.level_label = Entity(Label("RedRose-Regular.ttf", level.name)).get(Label)
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

            if is_key_pressed(key_binds["navigate_to_menu"]):
                level.save_file()
                engine.switch_to("Menu")
            
            if is_key_pressed(key_binds["interact_current_space"]):
                        for t in triggers:
                            if body.is_colliding_with(t):
                                t.on()

            if is_key_pressed(key_binds["move_player_n"]):
                self.entity.y -= movement_speed
            if is_key_pressed(key_binds["move_player_ne"]):
                self.entity.y -= movement_speed
                self.entity.x += movement_speed
            if is_key_pressed(key_binds["move_player_e"]):
                self.entity.x += movement_speed
            if is_key_pressed(key_binds["move_player_se"]):
                self.entity.y += movement_speed
                self.entity.x += movement_speed
            if is_key_pressed(key_binds["move_player_s"]):
                self.entity.y += movement_speed
            if is_key_pressed(key_binds["move_player_sw"]):
                self.entity.y += movement_speed
                self.entity.x -= movement_speed
            if is_key_pressed(key_binds["move_player_w"]):
                self.entity.x -= movement_speed
            if is_key_pressed(key_binds["move_player_nw"]):
                self.entity.y -= movement_speed
                self.entity.x -= movement_speed
            
            if not body.is_position_valid():
                self.entity.x = previous_x
                self.entity.y = previous_y
        
        camera.x = self.entity.x - camera.width/2 + sprite.image.get_width()/2
        camera.y = self.entity.y - camera.height/2 + sprite.image.get_height()/2