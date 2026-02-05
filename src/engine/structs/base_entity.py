from src.engine.structs.dungeon import *

from src.game.entity_definitions import *
from src.game.globals import *


# base class for all entities
BaseEntityT = list[RoomPosT | EntityE | NoneType]

# enum for base entity struct
T_BASE_ENTITY_TYPE = 0 # entity type like E_ENTITY_DRAGON
T_BASE_ENTITY_ROOM_POS = 1
T_BASE_ENTITY_COUNT = 2

def base_entity_create(entity_type: EntityE = E_ENTITY_UNKNOWN,
                       room_pos: RoomPosT = (0, 0),
                       size: int = T_BASE_ENTITY_COUNT) -> BaseEntityT:
    """
    fills extra empty spaces with None
    size: num of properties in entity to init
    """
    base_entity: BaseEntityT = [None] * size

    base_entity[T_BASE_ENTITY_TYPE] = entity_type
    base_entity[T_BASE_ENTITY_ROOM_POS] = room_pos

    if entity_type == E_ENTITY_UNKNOWN:
        log_warning(f"[base_entity_create] created unknown entity: {base_entity}")
    else:
        log_debug(f"[base_entity_create] created entity of type: {entity_type}")

    return base_entity

def base_entity_is(base_entity, entity_type: EntityE) -> bool:
    return base_entity[T_BASE_ENTITY_TYPE] == entity_type

def base_entity_render(dungeon, base_entity: BaseEntityT, image, image_size: tuple[int, int]) -> tuple[int, int]:
    """
    returns (draw_x, draw_y)
    """
    # room_size = BLOCK_SCALED_SIZE
    # entity_pos = base_entity[T_BASE_ENTITY_ROOM_POS]

    # dungeon_screen_size = (BLOCK_SCALED_SIZE[0] * dungeon_size[0], BLOCK_SCALED_SIZE[1] * dungeon_size[1])
    # start_x = g_window_size[0] // 2 - dungeon_screen_size[0] // 2
    # start_y = g_window_size[1] // 2 - dungeon_screen_size[1] // 2
    #
    # # get draw position based on room location
    # draw_x = start_x + room_size[0] * entity_pos[0]
    # draw_y = start_y + room_size[1] * entity_pos[1] 
    #
    # add to draw position so we draw the entity in the center of the room and not corner

    entity_pos: RoomPosT = base_entity[T_BASE_ENTITY_ROOM_POS]
    draw_x, draw_y = dungeon_get_room_screen_coords_center(dungeon, entity_pos)

    draw_x -= image_size[0] // 2
    draw_y -= image_size[1] // 2

    # draw entity
    fltk_ext.image_memoire(draw_x, draw_y, image, ancrage="nw")
    return (draw_x, draw_y)
