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

        # Check if player has something they can use to hit
        if hit_best["power"] <= 0:
            player.show_message("You need a weapon to hit this " + self.obj_name)
            return
        
        # If in range
        if distance < 50:
            player.show_message("hitting " + self.obj_name)
            from core.engine import engine
            engine.remove_entity(self.entity)
        else:
            player.show_message("I need to get closer")
        