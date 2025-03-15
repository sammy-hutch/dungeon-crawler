import os
from dotenv import load_dotenv
import json
import pygame

load_dotenv()

data_folder = os.getenv("DATA_FOLDER")
key_binds = {}

def load_key_bindings(file="keybinds.json"):
    try:
        with open(data_folder + "/" + file, "r") as f:
            loaded_bindings = json.load(f)
            for action, key_name in loaded_bindings.items():
                try:
                    loaded_bindings[action] = "pygame." + key_name
                    loaded_bindings[action] = getattr(pygame, key_name)
                    key_binds[action] = loaded_bindings[action]
                except AttributeError:
                    print(f"Warning: Invalid key name '{key_name}' in keybindings.json")
    except FileNotFoundError:
        print("Keybindings file not found. Using default bindings.")
    except json.JSONDecodeError:
        print("Error decoding keybindings.json. Using default bindings.")
