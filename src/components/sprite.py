import pygame

from core.camera import camera
from data.config import ARTWORK_IMAGE_FOLDER, DNGN_IMAGE_FOLDER, SPRITE_IMAGE_FOLDER

loaded = {}

class Sprite:
    def __init__(self, type, image, is_ui=False):
        from core.engine import engine
        if image in loaded:
            self.image = loaded[image]
        else:
            image_folder = ''
            if type == 'char': image_folder = SPRITE_IMAGE_FOLDER
            elif type == 'dngn': image_folder = DNGN_IMAGE_FOLDER
            elif type == 'art': image_folder = ARTWORK_IMAGE_FOLDER

            self.image = pygame.image.load(image_folder + "/" + image)
            loaded[image] = self.image
        if is_ui:
            engine.ui_drawables.append(self)
        else:
            engine.drawables.append(self)
        self.is_ui = is_ui
        self.type = type
    
    def delete(self):
        from core.engine import engine
        engine.drawables.remove(self)
    
    def draw(self, screen):
        pos = (self.entity.x - camera.x, self.entity.y - camera.y) \
                if not self.is_ui \
                else (self.entity.x, self.entity.y)
        screen.blit(self.image, pos)

