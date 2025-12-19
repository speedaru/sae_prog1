from src.engine.structs.entity import *
from src.engine.structs.treasure import *

def get_entities_positions(entities: EntitiesT):
    """
    returns: a set of RoomPosT, of all positions of entities in entities list
    """
    entities_positions = [dragon[ENTITY_ROOM_POS] for dragon in entities[ENTITIES_DRAGONS]]
    entities_positions.append(entities[ENTITIES_ADVENTURER][ENTITY_ROOM_POS]) # adventurer

    treasure = entities[ENTITIES_TREASURE]
    if treasure_is_valid(treasure):
        entities_positions.append(treasure[TREASURE_ROOM_POS]) # treasure

    return entities_positions
