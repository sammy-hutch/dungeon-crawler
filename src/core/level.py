from core.map import Map
from core.math_ext import safe_div, angle_from_north
from data.config import LEVEL_FOLDER, MAP_FOLDER, TILE_SIZE, VISION_RADIUS

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
        vision_radius = VISION_RADIUS
        for e in engine.entities:
            if e.id == 0:
                player_x = e.x
                player_y = e.y
                field_of_vision = []
                obstacles = []
                for map in engine.background_drawables:
                    for y, row in enumerate(map.tiles):
                        for x, tile in enumerate(row): # TODO: invert tile_size (i.e. divide player x and y by tile_size)
                            tile_x = x * self.tile_size
                            tile_y = y * self.tile_size
                            x_diff = player_x - tile_x
                            y_diff = player_y - tile_y
                            distance =  round((x_diff**2 + y_diff**2)**0.5)
                            if distance <= vision_radius * self.tile_size:
                                vector = [x_diff, y_diff]
                                angle = angle_from_north(vector)
                                tile_data = {
                                    "x": x, "y": y, "distance": distance, 
                                    "angle": angle, "is_visible": True
                                    }
                                field_of_vision.append(tile_data)
                                if map.tile_kinds[tile].is_solid: # TODO: change from is_solid. add new property to tiles, is_transparent
                                    variance = 0.5*self.tile_size
                                    nw_angle = angle_from_north([x_diff - variance, y_diff - variance])
                                    ne_angle = angle_from_north([x_diff + variance, y_diff - variance])
                                    se_angle = angle_from_north([x_diff + variance, y_diff + variance])
                                    sw_angle = angle_from_north([x_diff - variance, y_diff + variance])
                                    min_angle = min(nw_angle, ne_angle, se_angle, sw_angle)
                                    max_angle = max(nw_angle, ne_angle, se_angle, sw_angle)
                                    limit = max_angle - min_angle > 90
                                    tile_data = {
                                        "x": x, "y": y, "distance": distance, 
                                        "min_angle": min_angle, "max_angle": max_angle, "limit": limit
                                        }
                                    obstacles.append(tile_data)
                for tile in field_of_vision:
                    for obs in obstacles:
                        if (
                            tile["distance"] > obs["distance"] and (
                                (obs["limit"] and (tile["angle"] > obs["max_angle"] or tile["angle"] < obs["min_angle"]))
                                or
                                (not obs["limit"] and obs["min_angle"] < tile["angle"] < obs["max_angle"])
                            )
                        ):
                            tile["is_visible"] = False
                for y, row in enumerate(self.fog):
                    for x, tile in enumerate(row):
                        if tile == " " or tile == "o":
                            self.fog[y][x] = "o"
                        else:
                            self.fog[y][x] = "x"
                        for tile in field_of_vision:
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