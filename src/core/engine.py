import os
from dotenv import load_dotenv
import pygame

load_dotenv()
pygame.init()

engine = None
default_width = int(os.getenv("SCREEN_WIDTH"))
default_height = int(os.getenv("SCREEN_HEIGHT"))
debug_mode = os.getenv("DEBUG_MODE")
level_folder_path = "./" + os.getenv("LEVEL_FOLDER") + "/"
map_folder_path = "./" + os.getenv("MAP_FOLDER") + "/"
save_name = os.getenv("SAVE_NAME")

class Engine:
    def __init__(self, game_title):
        global engine
        engine = self

        self.active_objs = []  # Anything with an update() method that can be called
        self.background_drawables = []
        self.drawables = []  # Anything to be drawn in the world
        self.ui_drawables = []  # Anything to be drawn over the world

        from core.camera import create_screen
        self.clear_colour = (30, 150, 240)  # Default colour if nothing else is drawn
        self.screen = create_screen(default_width, default_height, game_title)  # The rectangle in the window itself
        self.stages = {}
        self.current_stage = None
    
    def register(self, stage_name, func):
        self.stages[stage_name] = func

    def switch_to(self, stage_name):
        self.reset()
        self.current_stage = stage_name
        func = self.stages[stage_name]
        print(f"Switching to {self.current_stage}")
        func()

    def run(self):
        from core.input import keys_down
        movement_delay = 100  # milliseconds between movements
        last_movement_time = {} # Dictionary to store last movement time for each key

        self.running = True
        while self.running:
            for event in pygame.event.get():
                # Handle quit event
                if event.type == pygame.QUIT:
                    # if in debug mode, delete all map and level files
                    # TODO: make this into its own function
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
                    self.running = False
                # Handle keydown and keyup events
                # TODO: tidy this
                elif event.type == pygame.KEYDOWN:
                    keys_down.add(event.key)
                    last_movement_time[event.key] = 0
                elif event.type == pygame.KEYUP:
                    if event.key in keys_down:
                        keys_down.remove(event.key)
                    if event.key in last_movement_time:
                        del last_movement_time[event.key]
            
                # Handle movement
                # TODO: tidy this
                current_time = pygame.time.get_ticks()
                for key in keys_down:
                    if key in last_movement_time:
                        if current_time - last_movement_time[key] >= movement_delay:
                            for a in self.active_objs:
                                a.update()
                            last_movement_time[key] = current_time

            
            # Draw code
            self.screen.fill(self.clear_colour)

            # Draw background items like the tiles
            for b in self.background_drawables:
                b.draw(self.screen)
            
            # Draw the main objects
            for s in self.drawables:
                s.draw(self.screen)
            
            # Draw UI stuff
            for l in self.ui_drawables:
                l.draw(self.screen)
            
            pygame.display.flip()

            # Cap the frames
            # TODO: find a better way to manage key presses etc
            # clock.tick(60)
            pygame.time.delay(17)
        
        pygame.quit()

    def reset(self):
        from components.physics import reset_physics
        reset_physics()
        self.active_objs.clear()
        self.drawables.clear()
        self.ui_drawables.clear()
        self.background_drawables.clear()