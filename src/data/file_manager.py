import os
from data.config import DEBUG_MODE, LEVEL_FOLDER, MAP_FOLDER, SAVE_NAME

level_folder_path = "./" + LEVEL_FOLDER + "/"
map_folder_path = "./" + MAP_FOLDER + "/"
editables = [level_folder_path, map_folder_path]

def save_game():
    # if in debug mode, delete all map and level files (all files in folders listed in editables)
    if DEBUG_MODE:
        for folder_path in editables:
            for filename in os.listdir(folder_path):
                if filename.startswith(SAVE_NAME):
                    path = os.path.join(folder_path, filename)
                    os.remove(path)
    # TODO: add functionality to save files otherwise, such as by providing save name