from core.map import TileKind


tile_kinds = {
    "w": TileKind("wall", "catacombs0.png", True),
    "f": TileKind("floor", "limestone1.png", False),
    "^": TileKind("stairs_up", "stone_stairs_up.png", False),
    "v": TileKind("stairs_down", "stone_stairs_down.png", False)
}