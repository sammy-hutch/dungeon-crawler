from components.button import Button
from components.entity import Entity
from components.label import Label
from components.sprite import Sprite

from data.file_manager import save_game

def new_game():
    from core.engine import engine
    save_game()
    engine.lvl_num = 1
    engine.switch_to("Play")

def resume_game():
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
                                   "New Game", 50, 
                                   (150, 0, 0)))
    resume_game_button = Entity(Label("RedRose-Regular.ttf",
                                      "Resume Game", 50,
                                      (150, 0, 0)))
    quit_game_button = Entity(Label("RedRose-Regular.ttf", 
                                    "Quit Game", 50, 
                                    (150, 0, 0)))
    
    # Set button size
    new_game_button_size = new_game_button.get(Label).get_bounds()
    resume_game_button_size = resume_game_button.get(Label).get_bounds()
    quit_game_button_size = quit_game_button.get(Label).get_bounds()

    # Set button position
    from core.camera import camera
    new_game_button.x = camera.width/2 - new_game_button_size.width/2 - 275
    new_game_button.y = camera.height - 750
    resume_game_button.x = camera.width/2 - resume_game_button_size.width/2 - 275
    resume_game_button.y = camera.height - 675
    quit_game_button.x = camera.width/2 - quit_game_button_size.width/2 - 275
    quit_game_button.y = camera.height - 600

    # Add button functionality
    new_game_button.add(Button(new_game, new_game_button_size))
    resume_game_button.add(Button(resume_game, resume_game_button_size))
    quit_game_button.add(Button(quit_game, quit_game_button_size))