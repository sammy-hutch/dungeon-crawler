import pygame
from libs.sprite import Sprite
from libs.input import is_key_pressed
from libs.camera import camera
from libs.entity import active_objs

# TODO: create key bindings file so keys can be modified

movement_speed = 32

class Player:
    def __init__(self):
        active_objs.append(self)
    
    def update(self):
        sprite = self.entity.get(Sprite)
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
        camera.x = self.entity.x - camera.width/2 + sprite.image.get_width()/2
        camera.y = self.entity.y - camera.height/2 + sprite.image.get_height()/2