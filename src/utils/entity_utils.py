from src.engine.structs.entity import *
from src.engine.structs.dragon import *
from src.engine.entity_system import *
from src.engine.structs.treasure import *

def _get_entity_system_positions(entity_system, entity_system_to_skip: set[EntityE]) -> set[RoomPosT]:
    # init with dragons positions first
    # entity_system_positions = [dragon[T_BASE_ENTITY_ROOM_POS] for dragon in entity_system[T_ENTITY_SYSTEM_DRAGONS]]
    positions = set()

    # other single ents
    for entity in entity_system:
        if entity[T_BASE_ENTITY_TYPE] in entity_system_to_skip:
            continue

        # check if valid ent and not just empty ent
        if isinstance(entity, list) and len(entity) >= T_BASE_ENTITY_COUNT:
            positions.add(entity[T_BASE_ENTITY_ROOM_POS])

    return positions

def get_collision_entity_positions(entity_system: EntitySystemT) -> set[RoomPosT]:
    """
    returns: a set of RoomPosT, of all positions of entity_system in entity_system list
    """
    # skip items bcs they cant interupt movement path
    return _get_entity_system_positions(entity_system, ENTITY_ITEMS)

def get_dragon_positions(entity_system) -> set[DragonT]:
    dragon_positions = set()

    for base_entity in entity_system:
        if base_entity[T_BASE_ENTITY_TYPE] == E_ENTITY_DRAGON:
            dragon_positions.add(base_entity[T_BASE_ENTITY_ROOM_POS])

    return dragon_positions

def get_all_entity_positions(entity_system: EntitySystemT) -> set[RoomPosT]:
    return _get_entity_system_positions(entity_system, set())
