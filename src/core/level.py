from core.map import Map
from data.config import LEVEL_FOLDER, MAP_FOLDER, SAVE_NAME, TILE_SIZE

level = None

class Level:
    def __init__(self, level_file, tile_types):
        global level
        level = self
        self.tile_types = tile_types
        self.load_level_file(level_file)
    
    def load_level_file(self, level_file):
        from data.objects import create_entity
        from core.engine import engine

        # Read all the data from the file
        file = open(LEVEL_FOLDER + "/" + level_file, "r")
        data = file.read()
        file.close()

        self.name = level_file.split(".")[0].title().replace("_", " ")

        # Split up the data by minus signs
        chunks = data.split('\n-')
        tile_map_data = chunks[0]
        entity_data = chunks[1]

        # Load the map
        self.map = Map(tile_map_data, self.tile_types)

        # Load the entities
        self.entities = []
        entity_lines = entity_data.split('\n')[1:]
        for line in entity_lines:
            try:
                items = line.split(',')
                id = int(items[0])
                x = int(items[1])
                y = int(items[2])
                entity = create_entity(id, x, y, items)
                self.entities.append(entity)
                engine.entities.append(entity)
            except:
                print(f"Error parsing line: {line}")
    
    def save_file(self):
        from core.engine import engine
        from core.levelmaker import load_map_file, write_level_to_file
        from components.navigator import lvl_num

        map_file = SAVE_NAME + "_" + str(lvl_num) + ".map"
        map = load_map_file(MAP_FOLDER, map_file)

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
                        
        write_level_to_file(map, entity_list, lvl_num)
