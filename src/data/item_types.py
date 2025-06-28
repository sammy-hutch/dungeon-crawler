from components.inventory import ItemType

item_types = [
    ItemType("Gold", "gold.png", 5, equippable=False),
    ItemType("Long Sword", "long_sword1.png", 1, damage=3, range=46, equippable=True),
    ItemType("Mace", "mace1.png", 1, damage=25, range=46, equippable=True)
]