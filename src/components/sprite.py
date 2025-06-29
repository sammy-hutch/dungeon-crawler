import pygame

from core.camera import camera
from core.math_ext import angle_from_north, safe_div
from data.config import ARTWORK_IMAGE_FOLDER, DNGN_IMAGE_FOLDER, ITEM_IMAGE_FOLDER, SPRITE_IMAGE_FOLDER, TILE_SIZE, UI_IMAGE_FOLDER, VISION_RADIUS

loaded = {}

class Sprite:
    def __init__(self, type, image, is_ui=False, is_permanent=True):
        from core.engine import engine

        self.set_image(type, image)

        if is_ui:
            engine.ui_drawables.append(self)
        else:
            engine.drawables.append(self)
        
        self.is_ui = is_ui
        self.type = type
        self.is_permanent = is_permanent
    
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
        tile_size = TILE_SIZE
        pos = (self.entity.x - camera.x, self.entity.y - camera.y) \
                if not self.is_ui \
                else (self.entity.x, self.entity.y)
        # Always draw permanent sprites
        if self.is_permanent:
            screen.blit(self.image, pos)
        # Conditionally draw non-permanent sprites if in player field of vision
        else:
            from components.player import player_vision
            for tile in player_vision:
                if self.entity.y == tile["y"]*tile_size \
                    and self.entity.x == tile["x"]*tile_size \
                    and tile["is_visible"]:
                    screen.blit(self.image, pos)

    
    def line_of_sight(self, target, field_of_vision: list, obstacles: list):
        """
        Helper function for field_of_vision. 
        Identifies if target is within sprite's field of vision.
        Updates field_of_vision and obstacles lists with data of the specified target
        
        Args:
        - target (dict): x-coord, y-coord, is_obstacle flag, target type
        - field_of_vision (list): list of tiles in field of vision
        - obstacles (list): list of obstacles in field of vision

        Returns:
        - field_of_vision (list)
        - obstacles (list)
        """

        vision_radius = VISION_RADIUS
        tile_size = TILE_SIZE
        self_x = safe_div(self.entity.x, tile_size)
        self_y = safe_div(self.entity.y, tile_size)
        # field_of_vision = field_of_vision
        # obstacles = obstacles
        x = target["x"]
        y = target["y"]
        is_obstacle = target["is_obstacle"]
        type = target["type"]

        x_diff = self_x - x
        y_diff = self_y - y

        distance =  round((x_diff**2 + y_diff**2)**0.5)
        if distance <= vision_radius:
            if type == "tile":
                angle = angle_from_north([x_diff, y_diff])
                tile_data = {
                    "x": x, "y": y, "distance": distance, 
                    "angle": angle, "is_visible": True
                    }
                field_of_vision.append(tile_data)
            if is_obstacle:
                nw_angle = angle_from_north([x_diff - 0.5, y_diff - 0.5])
                ne_angle = angle_from_north([x_diff + 0.5, y_diff - 0.5])
                se_angle = angle_from_north([x_diff + 0.5, y_diff + 0.5])
                sw_angle = angle_from_north([x_diff - 0.5, y_diff + 0.5])
                min_angle = min(nw_angle, ne_angle, se_angle, sw_angle)
                max_angle = max(nw_angle, ne_angle, se_angle, sw_angle)
                over_limit = max_angle - min_angle > 90
                obstacle_data = {
                    "x": x, "y": y, "distance": distance, 
                    "min_angle": min_angle, "max_angle": max_angle, 
                    "over_limit": over_limit
                    }
                obstacles.append(obstacle_data)
        return field_of_vision, obstacles

    def field_of_vision(self, type="vision"):
        from core.engine import engine
        from components.physics import bodies
        tile_size = TILE_SIZE
        field_of_vision = []
        obstacles = []
        
        # Determine field of vision and identify obstacles on background_drawables layer
        for map in engine.background_drawables:
            for y, row in enumerate(map.tiles):
                for x, tile in enumerate(row):
                    is_obstacle = map.tile_kinds[tile].is_solid # TODO: change from is_solid. add new property to tiles, is_transparent
                    target = {"x": x, "y": y, "is_obstacle": is_obstacle, "type": "tile"}
                    field_of_vision, obstacles = self.line_of_sight(target, field_of_vision, obstacles)
        # Identify obstacles on bodies
        for b in bodies:
            if b.blocks_vision:
                is_obstacle = b.blocks_vision
                x = safe_div(b.entity.x, tile_size)
                y = safe_div(b.entity.y, tile_size)
                target = {"x": x, "y": y, "is_obstacle": is_obstacle, "type": "body"}
                field_of_vision, obstacles = self.line_of_sight(target, field_of_vision, obstacles)
        # Remove tiles from field of vision if blocked by obstacles
        for tile in field_of_vision:
            for obs in obstacles:
                if (
                    tile["distance"] > obs["distance"] and (
                        (obs["over_limit"] and (tile["angle"] > obs["max_angle"] or tile["angle"] < obs["min_angle"]))
                        or (not obs["over_limit"] and obs["min_angle"] < tile["angle"] < obs["max_angle"])
                    )
                ):
                    tile["is_visible"] = False
        if type == "vision":
            return field_of_vision