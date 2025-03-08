import pygame
import logging
from libs.camera import camera

class TileKind:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image = pygame.image.load(image)
        self.is_solid = is_solid

class Map:
    def __init__(self, map_file, tile_kinds, tile_size):
        self.tile_kinds = tile_kinds
        
        # file = open(map_file, "r")
        # data = csv.reader(file)
        # file.close()

        # Load the file
        file = open(map_file, "r")
        data = file.read()
        file.close()

        # Set up the tiles from loaded data
        self.tiles = []
        for line in data.split("\n"):
            row = [item.strip('"') for item in line.strip().split(',')]
            self.tiles.append(row)
        
        # Set the size
        self.tile_size = tile_size
    
    def draw(self, screen):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                location = (x * self.tile_size - camera.x, 
                            y * self.tile_size - camera.y)
                image = self.tile_kinds[tile].image
                screen.blit(image, location)
    
    def start_location(self):
        start_location = {"y": 0, "x": 0}
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile == "^":
                    start_location["y"] = y
                    start_location["x"] = x
                    return start_location
        return logging.error("no start location found during start_location() func")
