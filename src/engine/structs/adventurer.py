# engine stuff
from src.engine.structs.dungeon import *
from src.engine.asset_manager import *

# utils
import src.utils.fltk_extensions as fltk_ext
from src.utils.logging import *


# types
AdventurerT = list[list[int] | int]

# enum for adventurer structure
ADVENTURER_ROOM_POS = 0
ADVENTURER_LEVEL = 1
ADVENTURER_COUNT = 2


def adventurer_init(adventurer: AdventurerT, level: int = 1, room_pos: list[int] = [0, 0]):
    if len(adventurer) != ADVENTURER_COUNT:
        adventurer[:] = [None] * ADVENTURER_COUNT

    adventurer[ADVENTURER_LEVEL] = 1
    adventurer[ADVENTURER_ROOM_POS] = [0, 0]

def adventurer_render(adventurer: AdventurerT, assets: AssetsT):
    knight_image = assets[ASSETS_CHARACTERS][CHARACTERS_ADVENTURER]

    room_size = BLOCK_SCALED_SIZE
    adventurer_pos: list[int] = adventurer[ADVENTURER_ROOM_POS]

    # get draw position based on room location
    draw_x = room_size[0] * adventurer_pos[0] 
    draw_y = room_size[1] * adventurer_pos[1]

    # add to draw position so we draw the adventurer in the center of the room and not corner
    draw_x += (room_size[0] / 2) - (CHARACTERS_SIZES[0] / 2)
    draw_y += (room_size[1] / 2) - (CHARACTERS_SIZES[1] / 2)

    log_debug_full(f"[adventurer] (draw_x, draw_y): {(draw_x, draw_y)}")
    fltk_ext.image_memoire(draw_x, draw_y, knight_image, ancrage="nw")
