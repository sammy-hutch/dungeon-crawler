import os
import pygame
from dotenv import load_dotenv

from components.label import labels
from components.sprite import sprites
from components.entity import active_objs
from components.navigator import lvl_num
from core import input
from core.camera import create_screen
from core.level import Level, level
from core.levelmaker import level_maker
from core.mapmaker import map_maker
from data.key_binds import load_key_bindings
from data.tile_types import tile_kinds

load_dotenv()

debug_mode = os.getenv("DEBUG_MODE")
level_folder_path = "./" + os.getenv("LEVEL_FOLDER") + "/"
map_folder_path = "./" + os.getenv("MAP_FOLDER") + "/"
save_name = os.getenv("SAVE_NAME")

# pygame setup
pygame.init()
screen_width = int(os.getenv("SCREEN_WIDTH"))
screen_height = int(os.getenv("SCREEN_HEIGHT"))
screen = create_screen(screen_width, screen_height, "Red Mouse Dungeon Crawler")
tile_size = int(os.getenv("TILE_SIZE"))

clock = pygame.time.Clock()
running = True

load_key_bindings()
map_maker(lvl_num)
level_maker(lvl_num)

level_name = save_name + "_1.lvl"
level = Level(level_name, tile_kinds)


while running:
    # poll for events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            # if in debug mode, delete all map and level files
            if debug_mode == "yes":
                for filename in os.listdir(map_folder_path):
                    if filename.startswith(save_name):
                        path = os.path.join(map_folder_path, filename)
                        os.remove(path)
                for filename in os.listdir(level_folder_path):
                    if filename.startswith(save_name):
                        path = os.path.join(level_folder_path, filename)
                        os.remove(path)  
            # close the application              
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
    
    # Draw UI stuff
    for l in labels:
        l.draw(screen)

    # Render code

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(10)  # limits FPS to 10 # TODO: find a better way to manage the key presses

pygame.quit()