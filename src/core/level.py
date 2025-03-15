from core.map import Map
from data.objects import create_entity

level = None
level_folder = "content/levels"

class Level:
    def __init__(self, level_file, tile_types):
        global level
        level = self
        self.tile_types = tile_types
        self.load_file(level_file)
    
    def load_file(self, level_file):
        # Read all the data from the file
        file = open(level_folder + "/" + level_file, "r")
        data = file.read()
        file.close()

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
                self.entities.append(create_entity(id, x, y, items))
            except:
                print(f"Error parsing line: {line}")