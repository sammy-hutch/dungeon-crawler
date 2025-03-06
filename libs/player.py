import pygame
from libs.sprite import Sprite
from libs.input import is_key_pressed

# TODO: create key bindings file so keys can be modified

class Player(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.movement_speed = 32
    
    def update(self):
        if is_key_pressed(pygame.K_w):
            self.y -= self.movement_speed
        if is_key_pressed(pygame.K_e):
            self.y -= self.movement_speed
            self.x += self.movement_speed
        if is_key_pressed(pygame.K_d):
            self.x += self.movement_speed
        if is_key_pressed(pygame.K_c):
            self.y += self.movement_speed
            self.x += self.movement_speed
        if is_key_pressed(pygame.K_x):
            self.y += self.movement_speed
        if is_key_pressed(pygame.K_z):
            self.y += self.movement_speed
            self.x -= self.movement_speed
        if is_key_pressed(pygame.K_a):
            self.x -= self.movement_speed
        if is_key_pressed(pygame.K_q):
            self.y -= self.movement_speed
            self.x -= self.movement_speed