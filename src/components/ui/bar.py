import pygame

from data.config import TILE_SIZE

tile_size = TILE_SIZE

class Bar:
    def __init__(self, max, back_color, front_color, type, width=300, height=20):
        self.amount = max
        self.max = max
        self.back_color = back_color
        self.front_color = front_color
        self.width = width
        self.height = height
        self.type = type
        from core.engine import engine
        engine.ui_drawables.append(self)
    
    def draw(self, screen):
        from core.camera import camera
        visible = False
        # Always draw player bars
        if self.type == "player":
            visible = True
        # Conditionally draw enemy bars if in player field of vision
        else:
            from components.player import player_vision
            for tile in player_vision:
                if self.entity.y + camera.y == tile["y"]*tile_size \
                    and self.entity.x + camera.x == tile["x"]*tile_size \
                    and tile["is_visible"]:
                    visible = True
        
        if visible:
            if self.type == "enemy" and self.amount == self.max:
                pass
            else:
                filled = self.amount / self.max
                # Draw background
                pygame.draw.rect(screen, 
                                self.back_color, 
                                pygame.Rect(self.entity.x, 
                                            self.entity.y, 
                                            self.width, 
                                            self.height))
                # Draw foreground
                pygame.draw.rect(screen, 
                                self.front_color, 
                                pygame.Rect(self.entity.x, 
                                            self.entity.y, 
                                            self.width*filled, 
                                            self.height))