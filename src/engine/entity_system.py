from src.engine.structs.entity import *

# other classes to render
from src.engine.structs.item import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *
from src.engine.structs.treasure import *
from src.engine.structs.strong_sword import *
from src.engine.structs.chaos_seal import *

from src.game.entity_definitions import *

# entity list
EntitySystemT = list[BaseEntityT]

# T_entity_system_ADVENTURER = 0
# T_entity_system_DRAGONS = 1 # list of dragons
# T_entity_system_TREASURE = 2
# T_entity_system_ITEMS = 3 # list of items that we can pickup and stuff
# T_entity_system_COUNT = 4

# def entity_system_init(entity_system: EntitySystemT):
#     entity_system[:] = [list() for _ in range(T_entity_system_COUNT)]

def entity_system_create() -> EntitySystemT:
    return EntitySystemT()

def entity_system_add_entity(entity_system: EntitySystemT, base_entity: BaseEntityT):
    entity_system.append(base_entity)

def entity_system_get(entity_system: EntitySystemT, entity_type: EntityE, target_occurence: int = 0) -> BaseEntityT | None:
    """
    returns i occurence of specified entity type
    """
    count = 0

    for entity in entity_system:
        if entity[T_BASE_ENTITY_TYPE] == entity_type:
            count += 1
            if count >= target_occurence:
                return entity

    return None

def entity_system_get_first(entity_system: EntitySystemT, entity_type: EntityE) -> BaseEntityT | None:
    """
    get first occurence of target entity
    """
    return entity_system_get(entity_system, entity_type, 0)

def entity_system_get_first_and_only(entity_system: EntitySystemT, entity_type: EntityE) -> BaseEntityT | None:
    """
    same as entity_system_get_first but logs error if there is more than one
    """
    if len(entity_system_get_all(entity_system, entity_type)) > 1:
        log_error(f"[entity_system_get_first_and_only] more than 1 {entity_type} entity found")

    return entity_system_get_first(entity_system, entity_type)

def entity_system_get_all(entity_system: EntitySystemT, entity_type: EntityE) -> list[BaseEntityT]:
    """
    get all occurences of a specific type of entity
    """
    ents = []

    for entity in entity_system:
        if entity[T_BASE_ENTITY_TYPE] == entity_type:
            ents.append(entity)

    return ents

def entity_system_get_all_where(entity_system: EntitySystemT, entity_type: EntityE, filter_fn) -> list[BaseEntityT]:
    """
    get all occurences of a specific type of entity where filter_fn(entity) is true
    """
    ents = []

    for entity in entity_system:
        if entity[T_BASE_ENTITY_TYPE] == entity_type and filter_fn(entity):
            ents.append(entity)

    return ents

def entity_system_get_all_types(entity_system: EntitySystemT, entity_types: set[EntityE]) -> list[BaseEntityT]:
    """
    same as entity_system_get_all but can pass multiple entity types
    """
    ents = []

    for entity_type in entity_types:
        ents += entity_system_get_all(entity_system, entity_type)

    return ents

def entity_system_remove(entity_system: EntitySystemT, entity_type: EntityE, target_occurence: int = 0):
    """
    removes i occurence of specified entity type
    """
    count = 0

    for i in range(len(entity_system)):
        entity = entity_system[i]
        if entity[T_BASE_ENTITY_TYPE] == entity_type:
            count += 1
            if count >= target_occurence:
                entity_system.pop(i)

def entity_system_remove_first(entity_system: EntitySystemT, entity_type: EntityE):
    """
    removes first occurence of target entity
    """
    return entity_system_remove(entity_system, entity_type, 0)

def entity_system_remove_first_and_only(entity_system: EntitySystemT, entity_type: EntityE) -> BaseEntityT | None:
    """
    same as entity_system_remove_first but logs error if there is more than one
    """
    if len(entity_system_get_all(entity_system, entity_type)) > 1:
        log_error(f"[entity_system_remove_first_and_only] more than 1 {entity_type} entity found")

    return entity_system_remove_first(entity_system, entity_type)

def entity_system_remove_all(entity_system: EntitySystemT, entity_type: EntityE) -> list[BaseEntityT]:
    """
    removes all occurences of a specific type of entity_system
    """
    count = len(entity_system)

    i = 0
    while i < count:
        base_entity = entity_system[i]
        if base_entity[T_BASE_ENTITY_TYPE] == entity_type:
            entity_system.pop(i)
            count -= 1
        else: # increment iterator index only if didnt remove item from list
            i += 1

def entity_system_remove_all_where(entity_system: EntitySystemT, entity_type: EntityE, filter_fn):
    count = len(entity_system)

    i = 0
    while i < count:
        base_entity = entity_system[i]
        # entity is correct type and filter_fn returned true
        if base_entity_is(base_entity, entity_type) and filter_fn(base_entity):
            log_debug(f"removing {base_entity[T_BASE_ENTITY_TYPE]} in room: {base_entity[T_BASE_ENTITY_ROOM_POS]}")
            entity_system.pop(i)
            count -= 1
        else: # increment iterator index only if didnt remove item from list
            i += 1

def entity_system_remove_entity(entity_system: EntitySystemT, target):
    for i in range(len(entity_system)):
        entity = entity_system[i]
        if entity == target:
            entity_system.pop(i)
            return

def entity_system_remove_in_room(entity_system: EntitySystemT, entity_type: EntityE, room_pos: RoomPosT):
    for i in range(len(entity_system)):
        entity = entity_system[i]
        if entity[T_BASE_ENTITY_TYPE] == entity_type and entity[T_BASE_ENTITY_ROOM_POS] == room_pos:
            entity_system.pop(i)

def entity_system_render(entity_system: EntitySystemT, assets: AssetsT):
    for base_entity in entity_system:
        if base_entity_is(base_entity, E_ENTITY_ADVENTURER):
            adventurer_render(base_entity, assets)
            adventurer_render_path(base_entity)
        elif base_entity_is(base_entity, E_ENTITY_DRAGON):
            dragon_render(base_entity, assets)
        elif base_entity_is(base_entity, E_ENTITY_TREASURE):
            treasure_render(base_entity, assets)
        elif base_entity_is(base_entity, E_ENTITY_STRONG_SWORD):
            strong_sword_render(base_entity, assets)
        elif base_entity_is(base_entity, E_ENTITY_CHAOS_SEAL):
            chaos_seal_render(base_entity, assets)
        else:
            log_warning(f"trying to render unknown entity (type: {base_entity[T_BASE_ENTITY_TYPE]}): {base_entity}")

    # adventurer = entity_system[T_entity_system_ADVENTURER]
    # dragons = entity_system[T_entity_system_DRAGONS]
    # treasure = entity_system[T_entity_system_TREASURE]
    # items: list = entity_system[T_entity_system_ITEMS]
    #
    # # render adventurer
    # if adventurer:
    #     log_debug_full(f"rendering adventurer: level: room_pos: {adventurer[T_BASE_ENTITY_ROOM_POS]} {adventurer[T_ENTITY_LEVEL]}")
    #     adventurer_render(adventurer, assets)
    #     adventurer_render_path(adventurer)
    #
    # # render dragons
    # if dragons:
    #     log_debug_full(f"rendering dragons: {dragons}")
    #     for dragon in dragons:
    #         dragon_render(dragon, assets)
    #
    # # render treasure
    # if treasure:
    #     log_debug_full(f"rendering treasure: {treasure}")
    #     treasure_render(treasure, assets)
    #
    # # items
    # if items:
    #     log_debug_full(f"rendering items: {items}")
    #     for item in items: # render each item accordingly depending on its type
    #         if item[T_ENTITY_ITEM_TYPE] == E_ENTITY_STRONG_SWORD:
    #             strong_sword_render(item[T_ENTITY_ITEM_DATA], assets)
