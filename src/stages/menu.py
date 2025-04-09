from components.button import Button
from components.entity import Entity
from components.label import Label
from components.sprite import Sprite

def new_game():
    from core.engine import engine
    engine.switch_to("Play")

def quit_game():
    from core.engine import engine
    engine.quit()

def menu():
    # Add background
    Entity(Sprite("art", "art1.png", is_ui=True))

    # Create buttons
    new_game_button = Entity(Label("RedRose-Regular.ttf", 
                                   "New Game", 70, 
                                   (150, 0, 0)))
    quit_game_button = Entity(Label("RedRose-Regular.ttf", 
                                    "Quit Game", 70, 
                                    (150, 0, 0)))
    
    # Set button size
    new_game_button_size = new_game_button.get(Label).get_bounds()
    quit_game_button_size = quit_game_button.get(Label).get_bounds()

    # Set button position
    from core.camera import camera
    new_game_button.x = camera.width/2 - new_game_button_size.width/2 - 275
    new_game_button.y = camera.height - 750
    quit_game_button.x = camera.width/2 - quit_game_button_size.width/2 - 275
    quit_game_button.y = camera.height - 650

    # Add button functionality
    new_game_button.add(Button(new_game, new_game_button_size))
    quit_game_button.add(Button(quit_game, quit_game_button_size))