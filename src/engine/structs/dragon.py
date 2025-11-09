from random import randrange

# engine stuff
from src.engine.structs.dungeon import *
from src.engine.asset_manager import *

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
    if len(dragon) != DRAGON_COUNT:
        dragon[:] = [None] * DRAGON_COUNT

    dragon[DRAGON_LEVEL] = 1
    dragon[DRAGON_ROOM_POS] = [randrange(0, 6), randrange(0, 6)]

def dragon_render(dragon: DragonT, assets: AssetsT):
    knight_image = assets[ASSETS_CHARACTERS][CHARACTERS_DRAGONS]

    room_size = BLOCK_SCALED_SIZE
    dragon_pos: list[int] = dragon[DRAGON_ROOM_POS]

    # get draw position based on room location
    draw_x = room_size[0] * dragon_pos[0] 
    draw_y = room_size[1] * dragon_pos[1]

    # add to draw position so we draw the dragon in the center of the room and not corner
    draw_x += (room_size[0] / 2) - (CHARACTERS_SIZES[0] / 2)
    draw_y += (room_size[1] / 2) - (CHARACTERS_SIZES[1] / 2)

    log_debug_full(f"[dragon] (draw_x, draw_y): {(draw_x, draw_y)}")
    fltk_ext.image_memoire(draw_x, draw_y, knight_image, ancrage="nw")
