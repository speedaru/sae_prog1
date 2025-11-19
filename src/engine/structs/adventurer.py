# engine stuff
from src.engine.asset_manager import *
from src.engine.structs.entity import *

# utils
from src.utils.logging import *


# types
AdventurerT = list[list[int] | int | list[tuple[int, int]]]

# enum for adventurer structure
ADVENTURER_ROOM_POS = 0
ADVENTURER_LEVEL = 1
ADVENTURER_PATH = 2
ADVENTURER_COUNT = 3


def adventurer_init(adventurer: AdventurerT, level: int = 1, room_pos: list[int] = [0, 0]):
    entity_init(adventurer, level, room_pos)

def adventurer_render(adventurer: AdventurerT, assets: AssetsT):
    knight_image = assets[ASSETS_CHARACTERS][CHARACTERS_ADVENTURER]

    entity_render(adventurer, knight_image)
