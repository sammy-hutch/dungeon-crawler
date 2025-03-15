import os
from dotenv import load_dotenv
import pygame
from components.sprite import Sprite
from core.input import is_key_pressed
from core.camera import camera
from components.entity import active_objs
from components.physics import Body

load_dotenv()

# TODO: create key bindings file so keys can be modified

# player moves one tile per key press
movement_speed = int(os.getenv("TILE_SIZE"))

class Player:
    def __init__(self):
        active_objs.append(self)
    
    def update(self):
        previous_x = self.entity.x
        previous_y = self.entity.y
        sprite = self.entity.get(Sprite)
        body = self.entity.get(Body)

        if is_key_pressed(pygame.K_w):
            self.entity.y -= movement_speed
        if is_key_pressed(pygame.K_e):
            self.entity.y -= movement_speed
            self.entity.x += movement_speed
        if is_key_pressed(pygame.K_d):
            self.entity.x += movement_speed
        if is_key_pressed(pygame.K_c):
            self.entity.y += movement_speed
            self.entity.x += movement_speed
        if is_key_pressed(pygame.K_x):
            self.entity.y += movement_speed
        if is_key_pressed(pygame.K_z):
            self.entity.y += movement_speed
            self.entity.x -= movement_speed
        if is_key_pressed(pygame.K_a):
            self.entity.x -= movement_speed
        if is_key_pressed(pygame.K_q):
            self.entity.y -= movement_speed
            self.entity.x -= movement_speed
        
        if not body.is_position_valid():
            self.entity.x = previous_x
            self.entity.y = previous_y
        
        camera.x = self.entity.x - camera.width/2 + sprite.image.get_width()/2
        camera.y = self.entity.y - camera.height/2 + sprite.image.get_height()/2