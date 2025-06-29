from core.map import Map
from data.config import LEVEL_FOLDER, MAP_FOLDER, TILE_SIZE

level = None

class Level:
    def __init__(self, level_file, tile_types):
        global level
        level = self
        self.tile_types = tile_types
        self.tile_size = TILE_SIZE
        self.load_level_file(level_file)
    
    def load_level_file(self, level_file):
        from data.objects import create_entity
        from core.engine import engine
        engine.fog_drawables.append(self)

        # Read the data from the level file
        file = open(LEVEL_FOLDER + "/" + level_file, "r")
        level_data = file.read()
        file.close()

        # Read the data from the map file
        file = open(MAP_FOLDER + "/" + level_file.replace(".lvl", ".map"), "r")
        map_data = file.read()
        file.close()

        self.name = level_file.split(".")[0].title().replace("_", " ")

        # Split up the data by minus signs
        chunks = level_data.split('\n-')
        fog_data = chunks[0]
        entity_data = chunks[1]

        # Load the map
        self.map = Map(map_data, self.tile_types)

        # Load the fog
        self.fog = []
        for line in fog_data.split("\n"):
            row = [item.strip('"') for item in line.strip().split(',')]
            self.fog.append(row)

        # Load the entities
        entity_lines = entity_data.split('\n')[1:]
        for line in entity_lines:
            try:
                items = line.split(',')
                id = int(items[0])
                x = int(items[1])
                y = int(items[2])
                entity = create_entity(id, x, y, items)
                engine.entities.append(entity)
            except:
                print(f"Error parsing line: {line}")
    
    def save_file(self):
        from core.engine import engine
        from core.levelmaker import write_level_to_file

        fog = self.fog
        
        entity_list = []
        for entity in engine.entities:
            entity_data = []
            entity_data.append(str(entity.id))
            entity_data.append(str(int(entity.x / TILE_SIZE)))
            entity_data.append(str(int(entity.y / TILE_SIZE)))
            for i, val in enumerate(entity.data):
                if i > 2:
                    entity_data.append(val)
            entity_list.append(entity_data)
                        
        write_level_to_file(fog, entity_list, engine.lvl_num)
    
    def update(self):
        from core.engine import engine
        from components.player import player_vision
        from components.sprite import Sprite
        visible_tiles = []
        for e in engine.entities:
            if e.id == 0:
                visible_tiles = player_vision
        for y, row in enumerate(self.fog):
            for x, tile in enumerate(row):
                if tile == " " or tile == "o":
                    self.fog[y][x] = "o"
                else:
                    self.fog[y][x] = "x"
                for tile in visible_tiles:
                    if y == tile["y"] and x == tile["x"] and tile["is_visible"]:
                        self.fog[y][x] = " "

    def draw(self, screen):
        from core.camera import camera
        for y, row in enumerate(self.fog):
            for x, tile in enumerate(row):
                location = (x * self.tile_size - camera.x, 
                            y * self.tile_size - camera.y)
                image = self.tile_types[tile].image
                screen.blit(image, location)