from components.usable import Usable
from data.config import NPC_FOLDER

npc_folder = NPC_FOLDER
npc_talk_distance = 60

class NPC(Usable):
    def __init__(self, obj_name, npc_file):
        super().__init__(obj_name)
        self.npc_file = npc_file
    
    def on(self, other, distance):
        from components.player import Player
        player = other.get(Player)
        if distance < npc_talk_distance:
            file = open(npc_folder + "/" + self.npc_file, "r")
            data = file.read()
            file.close()
            lines = data.split("\n")
            from components.ui.dialog_view import DialogView
            DialogView(lines, self, player)
        else:
            player.show_message("Who is this? I need to get closer")