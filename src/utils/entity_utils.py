from src.engine.structs.entity import *
from src.engine.structs.entities import *
from src.engine.structs.treasure import *

def get_collision_entities_positions(entities: EntitiesT):
    """
    returns: a set of RoomPosT, of all positions of entities in entities list
    """
    # entities to skip bcs cant collid or handle seperatly
    ENTITIES_TO_SKIP = { T_ENTITIES_DRAGONS, T_ENTITIES_ITEMS }

    # init with dragons positions first
    entities_positions = [dragon[T_BASE_ENTITY_ROOM_POS] for dragon in entities[T_ENTITIES_DRAGONS]]

    # other single ents
    for entity_type, entity in enumerate(entities):
        if entity_type in ENTITIES_TO_SKIP:
            continue

        # check if valid ent and not just empty ent
        if isinstance(entity, list) and len(entity) >= T_BASE_ENTITY_COUNT:
            entities_positions.append(entity[T_BASE_ENTITY_ROOM_POS]) # adventurer

    return entities_positions
