import pygame

from core.camera import camera
from data.config import SPRITE_IMAGE_FOLDER

loaded = {}

class Sprite:
    def __init__(self, image, is_ui=False):
        from core.engine import engine
        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(SPRITE_IMAGE_FOLDER + "/" + image)
            loaded[image] = self.image
        if is_ui:
            engine.ui_drawables.append(self)
        else:
            engine.drawables.append(self)
        self.is_ui = is_ui
    
    def delete(self):
        from core.engine import engine
        engine.drawables.remove(self)
    
    def draw(self, screen):
        pos = (self.entity.x - camera.x, self.entity.y - camera.y) \
                if not self.is_ui \
                else (self.entity.x, self.entity.y)
        screen.blit(self.image, pos)

