from math import ceil

from components.entity import Entity
from components.label import Label
from components.sprite import Sprite
from components.ui.window import Window, create_window

items_per_row = 5  # How many item slots are there per row
padding_size = 5   # How many empty pixels surround the inventory slots
gap_size = 5       # How many empty pixels are between each slot
item_size = 32     # How big is each slot in pixels

class InventoryView:
    # Creates a new inventory view, drawing a given inventory
    def __init__(self, 
                 inventory, 
                 slot_image="inventory_slot.png", 
                 selected_slot_image="selected_inventory_slot.png"):
        from core.engine import engine
        self.inventory = inventory
        self.slot_image = slot_image
        self.selected_slot_image = selected_slot_image

        width = padding_size \
                + (items_per_row * item_size) \
                + ((items_per_row-1) * gap_size) \
                + padding_size
        rows = ceil(inventory.capacity / items_per_row)
        height = padding_size \
                 + (rows * item_size) \
                 + ((rows-1) * gap_size) \
                 + padding_size
        
        from core.camera import camera
        x = camera.width - width
        y = 0

        self.window = create_window(x, y, width, height)
        self.slot_container_sprites = []
        self.slot_sprites = []

        engine.active_objs.append(self)

        inventory.listener = self

        self.render()
    
    def update(self):
        import pygame
        from core.input import is_mouse_just_pressed
        mouse_pos = pygame.mouse.get_pos()

        if is_mouse_just_pressed(1):
            if self.window.x <= mouse_pos[0] <= self.window.x + self.window.get(Window).width and \
                self.window.y <= mouse_pos[1] <= self.window.y + self.window.get(Window).height:
                
                x = mouse_pos[0] - self.window.x
                y = mouse_pos[1] - self.window.y
                x_slot = int(x / (item_size + gap_size))
                y_slot = int(y / (item_size + gap_size))
                x_local_pos = x % (item_size + gap_size)
                y_local_pos = y % (item_size + gap_size)

                if 0 < x_local_pos < item_size and \
                    0 < y_local_pos < item_size:

                    index = int(x_slot + (y_slot * items_per_row))
                    self.inventory.equipped_changed = True
                    if self.inventory.equipped_slot == index:
                        self.inventory.equipped_slot = None
                    else:
                        self.inventory.equipped_slot = index
                    self.refresh()

    # Creates all the UI elements to display the inventory
    def render(self):
        row = 0
        column = 0
        for index, slot in enumerate(self.inventory.slots):
            x = column * (item_size + gap_size) + self.window.x + padding_size
            y = row * (item_size + gap_size) + self.window.y + padding_size
            slot_image = \
                self.selected_slot_image if index == self.inventory.equipped_slot \
                else self.slot_image
            container_sprite = Entity(Sprite("ui", slot_image, True), x=x, y=y)
            self.window.get(Window).items.append(container_sprite)
            if slot.type is not None:
                item_sprite = Entity(Sprite("item", slot.type.icon_name, True), x=x, y=y)
                if slot.type.stack_size > 1:
                    label = Entity(Label("RedRose-Regular.ttf", 
                                         str(slot.amount), 
                                         colour=(255, 255, 0), 
                                         size=30), x=x, y=y)
                    self.window.get(Window).items.append(label)
                self.window.get(Window).items.append(item_sprite)
            column += 1
            if column >= items_per_row:
                column = 0
                row += 1

    # Destroys all the UI elements
    def clear(self):
        for i in self.window.get(Window).items:
            if i.has(Sprite):
                i.get(Sprite).breakdown()
            elif i.has(Label):
                i.get(Label).breakdown()
        self.window.get(Window).items.clear()

    # Calls clear, then render
    def refresh(self):
        self.clear()
        self.render()
