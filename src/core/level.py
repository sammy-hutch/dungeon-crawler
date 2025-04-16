from core.map import Map
from data.config import LEVEL_FOLDER, MAP_FOLDER, SAVE_NAME, TILE_SIZE

level = None

class Level:
    def __init__(self, level_file, tile_types):
        from core.engine import engine
        engine.fog_drawables.append(self)
        global level
        level = self
        self.tile_types = tile_types
        self.tile_size = TILE_SIZE
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

        # Create fog
        self.fog = []
        for row in self.map.tiles:
            tile_row = []
            for tile in row:
                tile_row.append("x")
            self.fog.append(tile_row)

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
        # TODO: save fog instead of map to lvl file (add additional part in load step to load from both map as well as lvl files)
        from core.engine import engine
        from core.levelmaker import load_map_file, write_level_to_file

        map_file = SAVE_NAME + "_" + str(engine.lvl_num) + ".map"
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
                        
        write_level_to_file(map, entity_list, engine.lvl_num)
    
    def update(self):
        from core.engine import engine
        for e in engine.entities:
            if e.id == 0:
                player_x = e.x
                player_y = e.y
                for y, row in enumerate(self.fog):
                    for x, tile in enumerate(row):
                        tile_x = x * self.tile_size
                        tile_y = y * self.tile_size
                        x_diff = player_x - tile_x
                        y_diff = player_y - tile_y
                        diff =  round((x_diff**2 + y_diff**2)**0.5)
                        if diff <= 5 * self.tile_size:
                            self.fog[y][x] = " "
                        elif tile == " " or tile == "o":
                            self.fog[y][x] = "o"
                        else:
                            self.fog[y][x] = "x"

    def draw(self, screen):
        from core.camera import camera
        for y, row in enumerate(self.fog):
            for x, tile in enumerate(row):
                location = (x * self.tile_size - camera.x, 
                            y * self.tile_size - camera.y)
                image = self.tile_types[tile].image
                screen.blit(image, location)