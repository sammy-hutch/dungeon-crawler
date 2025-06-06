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
            from core.effect import Effect
            Effect(self.entity.x, self.entity.y, 0, 0, 10, "cloud_misery0.png")

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
        from components.physics import Body
        player = other.get(Player)
        self_body = self.entity.get(Body)
        other_body = other.get(Body)

        # If in range
        if distance > 46: #TODO: calculate distance based on tile size, rather than hardcoded
            if player is not None:
                player.show_message("This is a " + self.obj_name + ", but i need to get closer to interact with it")
        # And player not passing through
        elif self_body.is_solid == False and other_body.is_colliding_with(self_body):
            return
        # Then
        else:
            self.current_state += 1
            if self.current_state > self.max_state:
                self.current_state = 0
            self.current_image = self.states[self.current_state]["image"]
            self.entity.get(Sprite).set_image('dngn', self.current_image)
            self_body.is_solid = self.states[self.current_state]["is_solid"].lower() == "true"  # TODO: tidy these lines to make conditional (only apply if those features exist in target body)
            self_body.blocks_vision = self.states[self.current_state]["blocks_vision"].lower() == "true"
            if player is not None:
                player.show_message(self.states[self.current_state]["message"])
            return
            

        