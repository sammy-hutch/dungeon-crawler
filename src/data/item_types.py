from components.inventory import ItemType

item_types = [
    ItemType("Gold", "gold.png", 5),
    ItemType("Long Sword", "long_sword1.png", 1, damage=10, cooldown=0.5, range=50),
    ItemType("Mace", "mace1.png", 1, damage=20, cooldown=0.5, range=50)
]