import pygame

from components.player import Player

from data.config import FOG, SCREEN_WIDTH, SCREEN_HEIGHT
from data.key_binds import load_key_bindings

pygame.init()

engine = None
lvl_num = 1

class Engine:
    def __init__(self, game_title):
        self.step = 0
        global engine
        engine = self

        self.lvl_num = lvl_num
        self.active_objs = []  # Anything with an update() method that can be called
        self.entities = [] # global list of all entities
        self.background_drawables = []
        self.drawables = []  # Anything to be drawn in the world
        self.fog_drawables = [] # fog layer
        self.ui_drawables = []  # Anything to be drawn as UI
        self.usables = []
        self.changed_player_state = False
        self.valid_event = True # flag for escaping invalid events

        from core.camera import create_screen
        self.clear_colour = (0, 0, 0)  # Default colour if nothing else is drawn
        self.screen = create_screen(SCREEN_WIDTH, SCREEN_HEIGHT, game_title)  # The rectangle in the window itself
        self.stages = {}
        self.current_stage = None

        load_key_bindings()
    
    def register(self, stage_name, func):
        self.stages[stage_name] = func

    def switch_to(self, stage_name):
        self.reset()
        self.current_stage = stage_name
        func = self.stages[stage_name]
        print(f"Switching to {self.current_stage}")
        func()

    def run(self):
        from core.input import keys_down, keys_just_pressed, mouse_buttons_just_pressed
        movement_delay = 100  # milliseconds between movements
        last_movement_time = {} # Dictionary to store last movement time for each key

        self.running = True
        while self.running:
            self.step += 1
            mouse_buttons_just_pressed.clear()
            keys_just_pressed.clear()

            # Handle events
            for event in pygame.event.get():
                if engine.valid_event == False:
                    for a in self.active_objs:
                        if a.entity.has(Player):
                            a.update()
                engine.valid_event = True

                # Handle quit event
                if event.type == pygame.QUIT:
                    self.quit()
                
                # Handle keydown and keyup events
                elif event.type == pygame.KEYDOWN:
                    keys_down.add(event.key)
                    keys_just_pressed.add(event.key)
                    last_movement_time[event.key] = 0
                elif event.type == pygame.KEYUP:
                    if event.key in keys_down:
                        keys_down.remove(event.key)
                    if event.key in last_movement_time:
                        del last_movement_time[event.key]
                
                # Handle mouse click events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_buttons_just_pressed.add(event.button)
                    self.changed_player_state = True
            
                # Handle movement
                current_time = pygame.time.get_ticks()
                for key in keys_down:
                    if key in last_movement_time:
                        if current_time - last_movement_time[key] >= movement_delay:
                            self.changed_player_state = True
                            last_movement_time[key] = current_time
                
                # TODO: move this to a better place, or handle better
                for f in self.fog_drawables:
                    f.update()

            # Update code
            if engine.changed_player_state == True:
                for a in self.active_objs:
                    if engine.valid_event:
                        a.update()
                engine.changed_player_state = False

            # Draw code
            self.screen.fill(self.clear_colour)

            # Draw background items like the tiles
            for b in self.background_drawables:
                b.draw(self.screen)
            
            # Draw the main objects
            for s in self.drawables:
                s.draw(self.screen)
            
            # Draw the effects
            from core.effect import effects
            for e in effects:
                e.draw(self.screen)

            # Draw the fog
            if FOG:
                for f in self.fog_drawables:
                    f.draw(self.screen)
            
            # Draw UI stuff
            for l in self.ui_drawables:
                l.draw(self.screen)
            
            pygame.display.flip()

            # Cap the frames
            pygame.time.delay(17)
        
        pygame.quit()

    def reset(self):
        from components.physics import reset_physics
        reset_physics()
        self.active_objs.clear()
        self.entities.clear()
        self.drawables.clear()
        self.ui_drawables.clear()
        self.background_drawables.clear()
        self.fog_drawables.clear()
        self.usables.clear()
        from core.effect import effects
        effects.clear()
        engine.valid_event = False
    
    def quit(self):
        from data.file_manager import save_game

        # Save the game
        save_game()
        
        # close the application    
        self.running = False
    
    def remove_entity(self, e): # TODO: see if entities should be handled in level instead
        self.entities.remove(e)
        for c in e.components:
            g = getattr(c, "breakdown", None)
            if callable(g):
                c.breakdown()
