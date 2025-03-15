
import os
import pygame
from dotenv import load_dotenv

from components.sprite import sprites
from components.entity import active_objs
from core import input
from core.camera import create_screen
from core.level import Level, level
from core.levelmaker import level_maker
from core.mapmaker import map_maker
from data.key_binds import load_key_bindings
from data.tile_types import tile_kinds

load_dotenv()

# pygame setup
pygame.init()
screen_width = int(os.getenv("SCREEN_WIDTH"))
screen_height = int(os.getenv("SCREEN_HEIGHT"))
screen = create_screen(screen_width, screen_height, "Red Mouse Dungeon Crawler")

clock = pygame.time.Clock()
running = True

map_file = "start.map"
level_file = "start.lvl"

tile_size = int(os.getenv("TILE_SIZE"))
load_key_bindings()
map_maker()
level_maker(map_file, level_file)
level = Level("start.lvl", tile_kinds)


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
    level.map.draw(screen)
    for s in sprites:
        s.draw(screen)

    # Render code

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(10)  # limits FPS to 60

pygame.quit()