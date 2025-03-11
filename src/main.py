# Example file showing a basic pygame "game loop"
import os
from dotenv import load_dotenv
import pygame
from core import input
from core.map import TileKind, Map
from core.mapmaker import map_maker
from components.player import Player
from components.sprite import Sprite, sprites
from core.camera import create_screen
from components.entity import Entity, active_objs
from components.physics import Body

load_dotenv()

# pygame setup
pygame.init()
screen_width = int(os.getenv("SCREEN_WIDTH"))
screen_height = int(os.getenv("SCREEN_HEIGHT"))
screen = create_screen(screen_width, screen_height, "Red Mouse Dungeon Crawler")

clock = pygame.time.Clock()
running = True

tile_size = int(os.getenv("TILE_SIZE"))
tile_kinds = {
    "w": TileKind("wall", "catacombs0.png", True),
    "f": TileKind("floor", "limestone1.png", False),
    "^": TileKind("stairs_up", "stone_stairs_up.png", False),
    "v": TileKind("stairs_down", "stone_stairs_down.png", False)
}
map_maker()
map = Map("start.map", tile_kinds, tile_size)
start_location = map.start_location()
start_x = start_location["x"] * tile_size
start_y = start_location["y"] * tile_size

player = Entity(Player(), Sprite("formicid.png"), Body(), x=start_x, y=start_y)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            input.keys_down.add(event.key)
        elif event.type == pygame.KEYUP:
            input.keys_down.remove(event.key)
    
    # Update code
    for a in active_objs:
        a.update()

    # Draw code
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    map.draw(screen)
    for s in sprites:
        s.draw(screen)

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(10)  # limits FPS to 60

pygame.quit()