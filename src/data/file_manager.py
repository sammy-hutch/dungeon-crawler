import os
from dotenv import load_dotenv

load_dotenv()

debug_mode = os.getenv("DEBUG_MODE")
level_folder_path = "./" + os.getenv("LEVEL_FOLDER") + "/"
map_folder_path = "./" + os.getenv("MAP_FOLDER") + "/"
save_name = os.getenv("SAVE_NAME")
editables = [level_folder_path, map_folder_path]

def save_game():
    # if in debug mode, delete all map and level files (all files in folders listed in editables)
    if debug_mode == "yes":
        for folder_path in editables:
            for filename in os.listdir(folder_path):
                if filename.startswith(save_name):
                    path = os.path.join(folder_path, filename)
                    os.remove(path)
    # TODO: add functionality to save files otherwise, such as by providing save name