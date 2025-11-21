# engine stuff
from src.engine.structs.dungeon import *
from src.engine.asset_manager import *

# utils
import src.utils.fltk_extensions as fltk_ext
from src.utils.logging import *

# types
EntityT = list[list[int] | int]

# enum for adventurer structure
ENTITY_ROOM_POS = 0
ENTITY_LEVEL = 1
ENTITY_COUNT = 2


def entity_init(entity: EntityT, level: int = 1, room_pos: list[int] = [0, 0], entity_size: int = ENTITY_COUNT):
    if len(entity) != entity_size:
        entity[:] = [None] * entity_size

    entity[ENTITY_LEVEL] = level
    entity[ENTITY_ROOM_POS] = room_pos

def entity_render(entity: EntityT, image):
    room_size = BLOCK_SCALED_SIZE
    entity_pos: list[int] = entity[ENTITY_ROOM_POS]

    # get draw position based on room location
    draw_x = room_size[0] * entity_pos[0] 
    draw_y = room_size[1] * entity_pos[1]

    # add to draw position so we draw the entity in the center of the room and not corner
    draw_x += (room_size[0] / 2) - (CHARACTERS_SIZES[0] / 2)
    draw_y += (room_size[1] / 2) - (CHARACTERS_SIZES[1] / 2)

    # draw player
    log_debug_full(f"[entity] (draw_x, draw_y): {(draw_x, draw_y)}")
    fltk_ext.image_memoire(draw_x, draw_y, image, ancrage="nw")

    # draw player level
    TEXT_OFFSET = (CHARACTERS_SIZES[0] + 4, CHARACTERS_SIZES[1])
    TEXT_POLICE_SIZE = 12
    TEXT_SIZE = fltk.taille_texte(str(entity[ENTITY_LEVEL]), taille=TEXT_POLICE_SIZE)
    TEXT_BG_SIZE = (TEXT_SIZE[0], TEXT_SIZE[1])

    # render player level
    text_pos_x, text_pos_y = draw_x + TEXT_OFFSET[0], draw_y
    fltk.rectangle(text_pos_x, text_pos_y, text_pos_x + TEXT_BG_SIZE[0], text_pos_y + TEXT_BG_SIZE[1], "white", "white")
    fltk.texte(text_pos_x, text_pos_y, str(entity[ENTITY_LEVEL]), ancrage="nw", taille=TEXT_POLICE_SIZE)
