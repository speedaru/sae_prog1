from random import randrange

# engine stuff
from src.engine.structs.dungeon import *
from src.engine.asset_manager import *
from src.engine.structs.entity import *

# utils
import src.utils.fltk_extensions as fltk_ext
from src.utils.logging import *


# types
DragonT = list[list[int] | int]

# enum for dragon structure
DRAGON_ROOM_POS = 0
DRAGON_LEVEL = 1
DRAGON_COUNT = 2


def dragon_init(dragon: DragonT, level: int = 1, room_pos: list[int] = [0, 0]):
    room_pos = [randrange(0, 6), randrange(0, 6)]
    entity_init(dragon, level, room_pos)

def dragon_render(dragon: DragonT, assets: AssetsT):
    dragon_image = assets[ASSETS_CHARACTERS][CHARACTERS_DRAGONS]

    entity_render(dragon, dragon_image)
