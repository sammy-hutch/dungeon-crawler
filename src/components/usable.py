class Usable:
    def __init__(self, obj_name):
        self.obj_name = obj_name
        from core.engine import engine
        engine.usables.append(self)
    
    def breakdown(self):
        from core.engine import engine
        engine.usables.remove(self)
    
    def on(self, other, distance):
        print("Base on function called")
    
class Hittable(Usable):
    def __init__(self, obj_name):
        super().__init__(obj_name)
    
    def on(self, other, distance):
        from components.player import Player, inventory
        player = other.get(Player)
        hit_best = inventory.get_best("hit_power")

        # If in range
        if distance > 46:
            player.show_message("I need to get closer")
        # Check if player has something they can use to hit
        elif hit_best["power"] <= 0:
            player.show_message("I need a weapon to hit this " + self.obj_name)
            return
        else:
            player.show_message("hitting " + self.obj_name)
            from core.engine import engine
            engine.remove_entity(self.entity)

class Changeable(Usable):
    def __init__(self, obj_name, default_state=0):
        super().__init__(obj_name)
        from data.states import states
        self.states = states[obj_name]
        self.current_state = default_state
        self.current_image = self.states[self.current_state]["image"]
        self.max_state = len(self.states) - 1
    
    def on(self, other, distance):
        from components.player import Player
        from components.sprite import Sprite
        player = other.get(Player)

        # If in range
        if distance > 46: #TODO: calculate distance based on tile size, rather than hardcoded
            player.show_message("This is a " + self.obj_name + ", but i need to get closer to interact with it")
        else:
            self.current_state += 1
            if self.current_state > self.max_state:
                self.current_state = 0
            self.current_image = self.states[self.current_state]["image"]
            self.entity.get(Sprite).set_image('dngn', self.current_image)

        