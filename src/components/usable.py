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
        print("hitting object")