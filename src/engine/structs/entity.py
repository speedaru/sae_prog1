# engine stuff
from src.engine.structs.dungeon import *
from src.engine.asset_manager import *

# utils
import src.utils.fltk_extensions as fltk_ext
from src.utils.logging import *

# types
EntityT = list[RoomPosT | int]

# enum for adventurer structure
ENTITY_ROOM_POS = 0
ENTITY_LEVEL = 1
ENTITY_COUNT = 2

EntitiesT = list[EntityT | list[EntityT]]
ENTITIES_ADVENTURER = 0
ENTITIES_DRAGONS = 1
ENTITIES_TREASURE = 2
ENTITIES_COUNT = 3

def entities_init(entities: EntitiesT):
    entities[:] = [list() for _ in range(ENTITIES_COUNT)]

def entity_init(entity: EntityT, level: int = 1, room_pos: RoomPosT = (0, 0), entity_size: int = ENTITY_COUNT):
    """
    Initializes a generic entity (like an adventurer or a dragon).

    It sets up the entity structure with a level and a position in the dungeon.
    If the list size is incorrect, it resizes it to fit the entity structure.

    Args:
        entity (EntityT): The list representing the entity (modified in-place).
        level (int, optional): The entity's level. Defaults to 1.
        room_pos (list[int], optional): The [x, y] position in the dungeon. Defaults to [0, 0].

    Doctest :

    >>> e = []
    >>> # Standard initialization
    >>> entity_init(e, level=5, room_pos=(2, 3))
    >>> e
    [(2, 3), 5]

    >>> # Accessing data with constants
    >>> e[ENTITY_LEVEL]
    5
    >>> e[ENTITY_ROOM_POS]
    (2, 3)

    >>> # Default initialization
    >>> e2 = [None, None]
    >>> entity_init(e2)
    >>> e2
    [(0, 0), 1]
    """
    if len(entity) != entity_size:
        entity[:] = [None] * entity_size

    entity[ENTITY_LEVEL] = level
    entity[ENTITY_ROOM_POS] = room_pos

def entity_base_render(entity_pos: RoomPosT, image) -> tuple[int, int]:
    """
    returns (draw_x, draw_y)
    """
    room_size = BLOCK_SCALED_SIZE

    # get draw position based on room location
    draw_x = room_size[0] * entity_pos[0]
    draw_y = room_size[1] * entity_pos[1] 

    # add to draw position so we draw the entity in the center of the room and not corner
    draw_x += (room_size[0] // 2) - (CHARACTERS_SIZES[0] // 2)
    draw_y += (room_size[1] // 2) - (CHARACTERS_SIZES[1] // 2)

    # draw entity
    log_debug_full(f"[entity] (draw_x, draw_y): {(draw_x, draw_y)}")
    fltk_ext.image_memoire(draw_x, draw_y, image, ancrage="nw")
    return (draw_x, draw_y)

def entity_render(entity: EntityT, image):
    """
    Renders an entity on the screen centered in its room.

    Calculates the exact pixel coordinates based on the room position and the block size,
    then draws the entity's image and its level (as text).

    Args:
        entity (EntityT): The entity structure to render.
        image: The tkinter PhotoImage object representing the entity.

    Note: This function performs graphical operations and cannot be tested via doctest.
    """
    room_pos: RoomPosT = entity[ENTITY_ROOM_POS]
    draw_x, draw_y = entity_base_render(room_pos, image)

    # draw player level
    TEXT_OFFSET = (CHARACTERS_SIZES[0] + 4, CHARACTERS_SIZES[1])
    TEXT_POLICE_SIZE = 12
    TEXT_SIZE = fltk.taille_texte(str(entity[ENTITY_LEVEL]), taille=TEXT_POLICE_SIZE)
    TEXT_BG_SIZE = (TEXT_SIZE[0], TEXT_SIZE[1])

    # render player level
    text_pos_x, text_pos_y = draw_x + TEXT_OFFSET[0], draw_y
    fltk.rectangle(text_pos_x, text_pos_y, text_pos_x + TEXT_BG_SIZE[0], text_pos_y + TEXT_BG_SIZE[1], "white", "white")
    fltk.texte(text_pos_x, text_pos_y, str(entity[ENTITY_LEVEL]), ancrage="nw", taille=TEXT_POLICE_SIZE)
