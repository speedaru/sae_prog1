from src.engine.structs.dungeon import *

# base class for all entities
BaseEntityT = list[RoomPosT]

# enum for base entity struct
T_BASE_ENTITY_ROOM_POS = 0
T_BASE_ENTITY_COUNT = 1

def base_entity_create(room_pos: RoomPosT = (0, 0), base_entity_size: int = T_BASE_ENTITY_COUNT) -> BaseEntityT:
    base_entity: BaseEntityT = [room_pos_create(0, 0)] * base_entity_size

    base_entity[T_BASE_ENTITY_ROOM_POS] = room_pos

    return base_entity

def base_entity_init(base_entity: BaseEntityT, room_pos: RoomPosT = (0, 0), base_entity_size: int = T_BASE_ENTITY_COUNT):
    if len(base_entity) != base_entity_size:
        base_entity[:] = [room_pos_create(0, 0)] * base_entity_size

    base_entity[T_BASE_ENTITY_ROOM_POS] = room_pos

def base_entity_render(base_entity: BaseEntityT, image) -> tuple[int, int]:
    """
    returns (draw_x, draw_y)
    """
    room_size = BLOCK_SCALED_SIZE
    entity_pos = base_entity[T_BASE_ENTITY_ROOM_POS]

    # get draw position based on room location
    draw_x = room_size[0] * entity_pos[0]
    draw_y = room_size[1] * entity_pos[1] 

    # add to draw position so we draw the entity in the center of the room and not corner
    draw_x += (room_size[0] // 2) - (CHARACTERS_SIZES[0] // 2)
    draw_y += (room_size[1] // 2) - (CHARACTERS_SIZES[1] // 2)

    # draw entity
    log_debug_full(f"[base entity] (draw_x, draw_y): {(draw_x, draw_y)}")
    fltk_ext.image_memoire(draw_x, draw_y, image, ancrage="nw")
    return (draw_x, draw_y)
