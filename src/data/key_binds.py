import logging
import json
import pygame

from data.config import DATA_FOLDER

key_binds = {}

def load_key_bindings(file="keybinds.json"):
    try:
        with open(DATA_FOLDER + "/" + file, "r") as f:
            loaded_bindings = json.load(f)
            for action, key_name in loaded_bindings.items():
                try:
                    loaded_bindings[action] = "pygame." + key_name
                    loaded_bindings[action] = getattr(pygame, key_name)
                    key_binds[action] = loaded_bindings[action]
                except AttributeError:
                    logging.error(f"Warning: Invalid key name '{key_name}' in keybindings.json")
    except FileNotFoundError:
        logging.error("Keybindings file not found. Using default bindings.")
    except json.JSONDecodeError:
        logging.error("Error decoding keybindings.json. Using default bindings.")
