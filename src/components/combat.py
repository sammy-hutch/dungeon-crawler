

class Combat:
    def __init__(self, health, on_death):
        self.health = health
        self.max_health = health
        self.equipped = None
        self.regen = 1
        self.on_death = on_death
        self.weapon_sprite = None
        from core.engine import engine
        engine.active_objs.append(self)
    
    def equip(self, item):
        from components.entity import Entity
        from components.sprite import Sprite
        self.equipped = item
        self.weapon_sprite = Entity(Sprite("item", self.equipped.icon_name.replace(".png", "_equipped.png"))).get(Sprite)
    
    def unequip(self):
        self.equipped = None
        self.weapon_sprite.entity.delete_self()
        self.weapon_sprite = None
    
    def breakdown(self):
        from core.engine import engine
        engine.active_objs.remove(self)
        self.weapon_sprite.entity.delete_self()
        self.weapon_sprite = None

    def attack(self, other):
        if self.equipped == None:
            # Code for unarmed attacks. TODO: make unarmed damage stat and pass it in
            damage = 1
            other.health -= damage
        else:
            damage = int(self.equipped.stats['damage'])
            other.health -= damage

        if other.health <= 0:
            other.on_death(other.entity)
    
    # def perform_attack(self): # TODO: review if needed, possibly for spells or AoE attacks. commented out for now
    #     if self.equipped == None:
    #         # Code for unarmed attacks. need to figure out if needed
    #         return
        
    #     from components.physics import get_bodies_within_circle
    #     nearby_objs = get_bodies_within_circle(self.entity.x, 
    #                                            self.entity.y, 
    #                                            self.equipped.stats['range'])
        
    #     for o in nearby_objs:
    #         if o.entity.has(Combat) and o.entity != self.entity:
    #             self.attack(o.entity.get(Combat))
    
    def update(self):
        if self.health < self.max_health:
            self.health += self.regen
        if self.health > self.max_health:
            self.health = self.max_health
        
        if self.weapon_sprite is not None:
            self.weapon_sprite.entity.x = self.entity.x
            self.weapon_sprite.entity.y = self.entity.y