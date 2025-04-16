from core.map import TileKind


tile_kinds = {
    "x": TileKind("unknown", "effect", "unseen.png", False),
    "o": TileKind("shadow", "effect", "out_of_sight.png", False),
    " ": TileKind("visible", "effect", "visible.png", False),
    "w": TileKind("wall", "dungeon", "catacombs0.png", True),
    "f": TileKind("floor", "dungeon", "limestone1.png", False),
    "^": TileKind("stairs_up", "dungeon", "limestone1.png", False),
    "v": TileKind("stairs_down", "dungeon", "limestone1.png", False),
    "d": TileKind("door", "dungeon", "limestone1.png", False)
}