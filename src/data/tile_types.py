from core.map import TileKind


tile_kinds = {
    "w": TileKind("wall", "catacombs0.png", True),
    "f": TileKind("floor", "limestone1.png", False),
    "^": TileKind("stairs_up", "limestone1.png", False),
    "v": TileKind("stairs_down", "limestone1.png", False)
}