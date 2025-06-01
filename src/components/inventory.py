import pygame

from components.physics import Trigger
from data.config import ITEM_IMAGE_FOLDER

item_image_folder = ITEM_IMAGE_FOLDER


# Information about each type (icon, value, stack size, etc)
class ItemType:
    def __init__(self, name, icon, stack_size=1, **kwargs):
        self.name = name
        self.icon_name = icon
        self.icon = pygame.image.load(item_image_folder + "/" + icon)
        self.value = 0
        self.weight = 0
        self.stack_size = stack_size
        self.stats = dict()
        for key in kwargs:
            self.stats[key] = kwargs[key]


# Can hold a quantity of item
class ItemSlot:
    def __init__(self):
        self.type = None
        self.amount = 0


# Has a certain number of slots for items
class Inventory:
    # Create a new inventory
    def __init__(self, capacity):
        self.capacity = capacity
        self.taken_slots = 0
        self.slots = []
        for _ in range(self.capacity):
            self.slots.append(ItemSlot())
        self.listener = None
    
    # Lets a listener know that the inventory changed
    def notify(self):
        if self.listener is not None:
            self.listener.refresh()
    
    def get_best(self, stat):
        best = {"power": 0, "item": None}
        for s in self.slots:
            if s.type is not None and stat in s.type.stats:
                p = int(s.type.stats[stat])
                if p > best["power"]:
                    best["power"] = p
                    best["item"] = s.type
        return best

    def add(self, item_type, amount=1):
        """
        Attempts to add a certain amount of an item to the inventory
        Default is 1 of that item
        Returns any excess items it couldn't add
        """
        # First sweep for any open stacks
        if item_type.stack_size > 1:
            for slot in self.slots:
                if slot.type == item_type:
                    add_amo = amount
                    if add_amo > item_type.stack_size - slot.amount:
                        add_amo = item_type.stack_size - slot.amount
                    slot.amount += add_amo
                    amount -= add_amo
                    if amount <= 0:
                        self.notify()
                        return 0
        # Next, place the item in the next slot
        for slot in self.slots:
            if slot.type == None:
                slot.type = item_type
                if item_type.stack_size < amount:
                    slot.amount = item_type.stack_size
                    self.notify()
                    return self.add(item_type, amount - item_type.stack_size)
                else:
                    slot.amount = amount
                    self.notify()
                    return 0

    def remove(self, item_type, amount=1):
        """
        Attempts to remove a certain amount of an item from the inventory
        Default is 1 of that item
        Returns what it was able to remove
        """
        found = 0
        for slot in self.slots:
            if slot.type == item_type:
                if slot.amount < amount:
                    found += slot.amount
                    slot.amount = 0
                    slot.type = None
                    self.notify()
                    continue
                elif slot.amount == amount:
                    found += amount
                    slot.amount = 0
                    slot.type = None
                    self.notify()
                    return found
                else:
                    found += amount
                    slot.amount -= amount
                    self.notify()
                    return found
        return found

    def has(self, item_type, amount=1):
        """
        Returns whether a certain amount of an item is present in the inventory
        """
        found = 0
        for slot in self.slots:
            if slot.type == item_type:
                found += slot.amount
                if found >= amount:
                    return True
        return False

    def get_index(self, item_type):
        """
        Returns the first slot number of where an item is
        """
        for index, slot in enumerate(self.slots):
            if slot.type == item_type:
                return index
        return -1

    # Returns a string of the inventory
    def __str__(self):
        s = ""
        for i in self.slots:
            if i.type is not None:
                s += str(i.type_name) + ": " + str(i.amount) + "\t"
            else:
                s += "Empty Slot\t"
        return s

    def get_free_slots(self):
        """
        Returns how many inventory slots are currently open
        """
        i = 0
        for slot in self.slots:
            if slot.type is None:
                i += 1
        return i

    def is_full(self):
        """
        Returns True if all slots have an item. Stacks do not need to be full
        """
        return self.get_free_slots() == 0

    def get_weight(self):
        """
        Returns the total weight of all items in the inventory
        """
        weight = 0
        for i in self.slots:
            weight += i.weight * i.amount
        return weight

    def get_value(self):
        """
        Returns the total value of all items in the inventory
        """
        value = 0
        for i in self.slots:
            value += i.value * i.amount
        return value


def pick_up(item, other):
    from components.player import Player, inventory
    if other.has(Player):
        extra = inventory.add(item.item_type, item.quantity)
        item.quantity -= item.quantity - extra
        if item.quantity <= 0:
            from core.engine import engine
            engine.remove_entity(item.entity)

# An item on the ground you can pick up
class DroppedItem(Trigger):
    def __init__(self, item_type, quantity):
        self.item_type = item_type
        self.quantity = quantity
        super().__init__(lambda other: pick_up(self, other), 0, 0, 32, 32)