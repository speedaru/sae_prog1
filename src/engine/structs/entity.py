# engine stuff
from src.engine.structs.base_entity import *
from src.engine.structs.dungeon import *
from src.engine.asset_manager import *

# utils
# import src.utils.fltk_extensions as fltk_ext
from src.utils.logging import *


# BaseEntityT -> EntityT
EntityT = list[RoomPosT | int]

# enum for entity struct
T_ENTITY_LEVEL = T_BASE_ENTITY_COUNT
T_ENTITY_COUNT = T_BASE_ENTITY_COUNT + 1

# def entity_init(entity: EntityT, level: int = 1, room_pos: RoomPosT = (0, 0), entity_size: int = T_ENTITY_COUNT):
#     """
#     Initializes a generic entity (like an adventurer or a dragon).
#
#     It sets up the entity structure with a level and a position in the dungeon.
#     If the list size is incorrect, it resizes it to fit the entity structure.
#
#     Args:
#         entity (EntityT): The list representing the entity (modified in-place).
#         level (int, optional): The entity's level. Defaults to 1.
#         room_pos (list[int], optional): The [x, y] position in the dungeon. Defaults to [0, 0].
#
#     Doctest :
#
#     >>> e = []
#     >>> # Standard initialization
#     >>> entity_init(e, level=5, room_pos=(2, 3))
#     >>> e
#     [(2, 3), 5]
#
#     >>> # Accessing data with constants
#     >>> e[T_ENTITY_LEVEL]
#     5
#     >>> e[T_ENTITY_ROOM_POS]
#     (2, 3)
#
#     >>> # Default initialization
#     >>> e2 = [None, None]
#     >>> entity_init(e2)
#     >>> e2
#     [(0, 0), 1]
#     """
#     base_entity_create()
#
#     entity[T_ENTITY_LEVEL] = level
#     entity[T_BASE_ENTITY_ROOM_POS] = room_pos

def entity_init():
    pass

def entity_create(entity_type: EntityE = E_ENTITY_UNKNOWN,
                  room_pos: RoomPosT = room_pos_create(0, 0),
                  level: int = 1,
                  entity_size: int = T_ENTITY_COUNT) -> EntityT:
    entity: list = base_entity_create(entity_type=entity_type, room_pos=room_pos, size=entity_size)

    entity[T_ENTITY_LEVEL] = level

    return entity

def entity_render(dungeon, entity: EntityT, image):
    """
    Renders an entity on the screen centered in its room.

    Calculates the exact pixel coordinates based on the room position and the block size,
    then draws the entity's image and its level (as text).

    Args:
        entity (EntityT): The entity structure to render.
        image: The tkinter PhotoImage object representing the entity.

    Note: This function performs graphical operations and cannot be tested via doctest.
    """
    draw_x, draw_y = base_entity_render(dungeon, entity, image, CHARACTERS_SIZES)

    # draw player level
    TEXT_OFFSET = (CHARACTERS_SIZES[0] + 4, CHARACTERS_SIZES[1])
    TEXT_POLICE_SIZE = 12
    TEXT_SIZE = fltk.taille_texte(str(entity[T_ENTITY_LEVEL]), taille=TEXT_POLICE_SIZE)
    TEXT_BG_SIZE = (TEXT_SIZE[0], TEXT_SIZE[1])

    # render player level
    text_pos_x, text_pos_y = draw_x + TEXT_OFFSET[0], draw_y
    fltk.rectangle(text_pos_x, text_pos_y, text_pos_x + TEXT_BG_SIZE[0], text_pos_y + TEXT_BG_SIZE[1], "white", "white")
    fltk.texte(text_pos_x, text_pos_y, str(entity[T_ENTITY_LEVEL]), ancrage="nw", taille=TEXT_POLICE_SIZE)

