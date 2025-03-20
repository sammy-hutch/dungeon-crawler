import pygame
import logging
from math import ceil

from data.config import DNGN_IMAGE_FOLDER, MAP_FOLDER, TILE_SIZE

map = None

class TileKind:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image = pygame.image.load(DNGN_IMAGE_FOLDER + "/" + image)
        self.is_solid = is_solid

class Map:
    def __init__(self, data, tile_kinds):
        from core.engine import engine
        engine.background_drawables.append(self)

        global map
        self.tile_kinds = tile_kinds
        map = self

        # Set up the tiles from loaded data
        self.tiles = []
        for line in data.split("\n"):
            row = [item.strip('"') for item in line.strip().split(',')]
            self.tiles.append(row)
        
        # Set the size
        self.tile_size = TILE_SIZE
    
    def is_point_solid(self, x, y):
        x_tile = int(x / self.tile_size)
        y_tile = int(y / self.tile_size)
        if y_tile < 0 or \
            x_tile < 0 or \
            y_tile >= len(self.tiles) or \
            x_tile >= len(self.tiles[y_tile]):
            return False
        tile = self.tiles[y_tile][x_tile]
        return self.tile_kinds[tile].is_solid

    def is_rect_solid(self, x, y, width, height):
        x_checks = int(ceil(width/self.tile_size))
        y_checks = int(ceil(height/self.tile_size))
        for yi in range(y_checks):
            for xi in range(x_checks):
                x = xi * self.tile_size + x
                y = yi * self.tile_size + y
                if self.is_point_solid(x, y):  # NW corner for each tile in affected area
                    return True
        if self.is_point_solid(x + width, y):  # NE corner
            return True
        if self.is_point_solid(x, y + height):  # SW corner
            return True
        if self.is_point_solid(x + width, y + height):  # SE corner
            return True
        return False

    def draw(self, screen):
        from core.camera import camera
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                location = (x * self.tile_size - camera.x, 
                            y * self.tile_size - camera.y)
                image = self.tile_kinds[tile].image
                screen.blit(image, location)
    

