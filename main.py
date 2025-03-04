# Example file showing a basic pygame "game loop"
import pygame
from libs.map import TileKind, Map
from libs.mapmaker import map_maker

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1024, 1024))
clock = pygame.time.Clock()
running = True

tile_kinds = {
    "w": TileKind("wall", "images/catacombs0.png", True),
    "f": TileKind("floor", "images/limestone1.png", False),
    "^": TileKind("stairs_up", "images/stone_stairs_up.png", False),
    "v": TileKind("stairs_down", "images/stone_stairs_down.png", False)
}
map_maker()
map = Map("maps/start.map", tile_kinds, 32)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw code
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    map.draw(screen)

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(10)  # limits FPS to 60

pygame.quit()