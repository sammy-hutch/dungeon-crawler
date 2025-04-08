import os
from dotenv import load_dotenv

load_dotenv()

# Visuals
SCREEN_WIDTH = int(os.getenv("SCREEN_WIDTH", "1024"))
SCREEN_HEIGHT = int(os.getenv("SCREEN_HEIGHT", "1024"))
TILE_SIZE = int(os.getenv("TILE_SIZE", "32"))

# Map building
MAP_WIDTH = int(os.getenv("MAP_WIDTH", "10"))
MAP_HEIGHT = int(os.getenv("MAP_HEIGHT", "10"))
MAP_COVERAGE_THRESHOLD = float(os.getenv("MAP_COVERAGE_THRESHOLD", "0.3"))

# Content
DATA_FOLDER = os.getenv("DATA_FOLDER")
SPRITE_IMAGE_FOLDER = os.getenv("SPRITE_IMAGE_FOLDER")
DNGN_IMAGE_FOLDER = os.getenv("DNGN_IMAGE_FOLDER")
LEVEL_FOLDER = os.getenv("LEVEL_FOLDER")
MAP_FOLDER = os.getenv("MAP_FOLDER")
FONT_FOLDER = os.getenv("FONT_FOLDER")
ARTWORK_IMAGE_FOLDER = os.getenv("ARTWORK_IMAGE_FOLDER")

# Defaults
SAVE_NAME = os.getenv("SAVE_NAME")
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
