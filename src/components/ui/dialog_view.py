import logging
import pygame

from components.button import Button
from components.entity import Entity
from components.label import Label
from components.sprite import Sprite


from components.ui.window import create_window, Window

dialog_box_width = 750
dialog_box_height = 100
padding_bottom = 50

speaker_label_x = 25
speaker_label_y = 10

content_label_x = 25
content_label_y = 40

helper_label_x = 25
helper_label_y = 70

class DialogView:
    def __init__(self, lines, npc, player, dialog_box_sprite="text_box.png"):
        self.lines = lines
        self.npc = npc
        self.player = player

        from core.camera import camera
        window_x = camera.width/2 - dialog_box_width/2
        window_y = camera.height - padding_bottom - dialog_box_height
        self.window = create_window(window_x, window_y, 
                                    dialog_box_width, 
                                    dialog_box_height).get(Window)

        self.background = Entity(Sprite("ui", dialog_box_sprite, is_ui=True), 
                                 x=window_x, y=window_y).get(Sprite)
        
        self.speaker_label = Entity(Label("RedRose-Regular.ttf", "", 
                                          size=25, colour=(0,0,0)),
                                    x=window_x+speaker_label_x, 
                                    y=window_y+speaker_label_y).get(Label)
        
        self.content_label = Entity(Label("RedRose-Regular.ttf", "", 
                                          size=25, colour=(0,0,0)),
                                    x=window_x+content_label_x, 
                                    y=window_y+content_label_y).get(Label)
        
        self.helper_label = Entity(Label("RedRose-Regular.ttf", 
                                         "[Press Space]", 
                                          size=25, colour=(0,0,0)),
                                    x=window_x+helper_label_x, 
                                    y=window_y+helper_label_y).get(Label)
        
        self.window.items.append(self.background)
        self.window.items.append(self.speaker_label)
        self.window.items.append(self.content_label)
        self.window.items.append(self.helper_label)

        from core.engine import engine
        engine.active_objs.append(self)

        self.current_line = -1
        self.next_line()

    # Get the next line of dialog
    def next_line(self):
        self.current_line += 1
        if self.current_line >= len(self.lines):
            self.breakdown()
            return
        line = self.lines[self.current_line]
        type = line[0]
        text = line[1:]
        if len(line) == 0:
            self.next_line()
            return
        if type == '!':
            self.command(line)
        elif type == '$':
            self.narrate(text)
        elif type == '-':
            self.npc_speak(text)
        elif type == '+':
            self.player_speak(text)
        else:
            logging.error(f"no actor associated with line {self.current_line} of dialog with {self.npc.obj_name}")

    # Have the NPC speak the next line of dialog
    def npc_speak(self, text):
        self.speaker_label.set_text(self.npc.obj_name)
        self.content_label.set_text(text)

    # Have the player speak the next line of dialog
    def player_speak(self, text):
        self.speaker_label.set_text("You")
        self.content_label.set_text(text)

    # Place some text in the window without anyone speaking
    def narrate(self, text):
        self.speaker_label.set_text("")
        self.content_label.set_text(text)

    # Execute some special command 
    # (e.g. giving item to player, navigating to particular line)
    def command(self, line):
        words = line.split(" ")
        command = words[1]
        arguments = words[2:]
        if command == "give":
            from components.player import inventory
            from data.item_types import item_types
            t = item_types[int(arguments[0])]
            amount = int(arguments[1])
            excess = inventory.add(t, amount)
            amount_added = amount - excess
            if amount_added == 0:
                self.speaker_label.set_text("")
                self.content_label.set_text(f"Your inventory is full")
            else:
                self.speaker_label.set_text("")
                self.content_label.set_text(f"You receive {amount_added} {t.name}")
        elif command == "take":
            from components.player import inventory
            from data.item_types import item_types
            t = item_types[int(arguments[0])]
            amount = int(arguments[1])
            removed = inventory.remove(t, amount)
            if removed < amount:
                inventory.add(t, removed)
                self.current_line = int(arguments[2])-2
                self.next_line()
            else:
                if removed > amount:
                    inventory.add(t, removed - amount)
                self.current_line = int(arguments[3])-2
                self.next_line()
        elif command == "goto":
            self.current_line = int(arguments[0])-2
            self.next_line()
        elif command == "end":
            self.breakdown()
        elif command == "random":
            import random
            next_lines = [int(x) for x in arguments]
            result = random.choice(next_lines)
            self.current_line = result-2
            self.next_line()
        else:
            print(f"unknown command: {command}")

    # Check if a key is pressed to move to the next line
    def update(self):
        from core.input import is_key_just_pressed
        if is_key_just_pressed(pygame.K_SPACE):
            self.next_line()
        
        if is_key_just_pressed(pygame.K_w) or \
            is_key_just_pressed(pygame.K_e) or \
            is_key_just_pressed(pygame.K_d) or \
            is_key_just_pressed(pygame.K_c) or \
            is_key_just_pressed(pygame.K_x) or \
            is_key_just_pressed(pygame.K_z) or \
            is_key_just_pressed(pygame.K_a) or \
            is_key_just_pressed(pygame.K_q):    # TODO: tidy this. make reference of movement keys and loop through them
            self.breakdown()

    # Destroy the window when the dialog is done
    def breakdown(self):
        from core.engine import engine
        engine.active_objs.remove(self)
        for c in self.window.items:
            c.breakdown()