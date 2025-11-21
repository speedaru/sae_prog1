from random import randrange

# engine stuff
from src.engine.structs.dungeon import *
from src.engine.asset_manager import *
from src.engine.structs.entity import *

# utils
import src.utils.fltk_extensions as fltk_ext
from src.utils.logging import *


# types
DragonT = list[RoomPosT | int]

# enum for dragon structure that inherits from entity
DRAGON_COUNT = ENTITY_COUNT


def dragon_init(dragon: DragonT, level: int = 1, room_pos: list[int] = [0, 0]):
    # room_pos = [randrange(0, 6), randrange(0, 6)]
    entity_init(dragon, level, room_pos, DRAGON_COUNT)

def dragon_render(dragon: DragonT, assets: AssetsT):
    dragon_image = assets[ASSETS_CHARACTERS][CHARACTERS_DRAGONS]

    entity_render(dragon, dragon_image)

# if no count set it will automatically calculate number of dragons
def dragon_create_dragons(dragons: list[DragonT], dungeon_size: tuple[int, int], count: int | NoneType = None):
    DRAGON_TO_ROOM_RATIO = 1 / 12

    if count == None:
        area = dungeon_size[0] * dungeon_size[1]
        count = round(DRAGON_TO_ROOM_RATIO * area)
        count = max(count, 1) # at least 1 dragon

    assert(not isinstance(count, NoneType)) # count not none
    assert(count > 0) # at least 1 dragon

    for _ in range(count):
        d = DragonT()
        random_room = [randrange(0, dungeon_size[0]), randrange(0, dungeon_size[1])]
        log_debug_full(f"random room ({dungeon_size[0], dungeon_size[1]}): {random_room}")
        dragon_init(d, room_pos=random_room)
        dragons.append(d)
