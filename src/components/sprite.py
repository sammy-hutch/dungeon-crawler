import pygame

from core.camera import camera
from data.config import ARTWORK_IMAGE_FOLDER, DNGN_IMAGE_FOLDER, ITEM_IMAGE_FOLDER, SPRITE_IMAGE_FOLDER, UI_IMAGE_FOLDER

loaded = {}

class Sprite:
    def __init__(self, type, image, is_ui=False):
        from core.engine import engine

        self.set_image(type, image)

        if is_ui:
            engine.ui_drawables.append(self)
        else:
            engine.drawables.append(self)
        
        self.is_ui = is_ui
        self.type = type
    
    def set_image(self, type, image):
        """
        Args:
            type (str): can be 'char', 'dngn', 'art', 'item', 'ui'
            image (str): .png file name of image
        """
        if image in loaded:
            self.image = loaded[image]
        else:
            image_folder = ''
            if type == 'char': image_folder = SPRITE_IMAGE_FOLDER
            elif type == 'dngn': image_folder = DNGN_IMAGE_FOLDER
            elif type == 'art': image_folder = ARTWORK_IMAGE_FOLDER
            elif type == 'item': image_folder = ITEM_IMAGE_FOLDER
            elif type == 'ui': image_folder = UI_IMAGE_FOLDER
            self.image = pygame.image.load(image_folder + "/" + image)
            loaded[image] = self.image
    
    def breakdown(self):
        from core.engine import engine
        if self.is_ui:
            engine.ui_drawables.remove(self)
        else:
            engine.drawables.remove(self)
    
    def draw(self, screen):
        pos = (self.entity.x - camera.x, self.entity.y - camera.y) \
                if not self.is_ui \
                else (self.entity.x, self.entity.y)
        screen.blit(self.image, pos)

