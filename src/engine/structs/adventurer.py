# engine stuff
from src.engine.structs.entity import *
from src.engine.asset_manager import *

# utils
from src.utils.logging import *


# types
MovementPathT = list[RoomPosT]
AdventurerT = list[RoomPosT | int | MovementPathT]

# enum for adventurer structure that inherits from entity
ADVENTURER_PATH = 2
ADVENTURER_COUNT = ENTITY_COUNT + 1


def adventurer_init(adventurer: AdventurerT, level: int = 1, room_pos: list[int] = [0, 0]):
    entity_init(adventurer, level, room_pos, ADVENTURER_COUNT)

def adventurer_render(adventurer: AdventurerT, assets: AssetsT):
    knight_image = assets[ASSETS_CHARACTERS][CHARACTERS_ADVENTURER]

    entity_render(adventurer, knight_image)
