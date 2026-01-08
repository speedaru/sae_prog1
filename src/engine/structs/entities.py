from src.engine.structs.entity import *

# other classes to render
from src.engine.structs.item import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *
from src.engine.structs.treasure import *
from src.engine.structs.strong_sword import *

from src.game.entity_definitions import *


# entity list
EntitiesT = list[EntityT | list[EntityT]]
T_ENTITIES_ADVENTURER = 0
T_ENTITIES_DRAGONS = 1
T_ENTITIES_TREASURE = 2
T_ENTITIES_ITEMS = 3 # list of items that we can pickup and stuff
T_ENTITIES_COUNT = 4

def entities_init(entities: EntitiesT):
    entities[:] = [list() for _ in range(T_ENTITIES_COUNT)]

def entities_render(entities: EntitiesT, assets: AssetsT):
    adventurer = entities[T_ENTITIES_ADVENTURER]
    dragons = entities[T_ENTITIES_DRAGONS]
    treasure = entities[T_ENTITIES_TREASURE]
    items: list = entities[T_ENTITIES_ITEMS]

    # render adventurer
    if adventurer:
        log_debug_full(f"rendering adventurer: level: room_pos: {adventurer[T_BASE_ENTITY_ROOM_POS]} {adventurer[T_ENTITY_LEVEL]}")
        adventurer_render(adventurer, assets)
        adventurer_render_path(adventurer)

    # render dragons
    if dragons:
        log_debug_full(f"rendering dragons: {dragons}")
        for dragon in dragons:
            dragon_render(dragon, assets)

    # render treasure
    if treasure:
        log_debug_full(f"rendering treasure: {treasure}")
        treasure_render(treasure, assets)

    # items
    if items:
        log_debug_full(f"rendering items: {items}")
        for item in items: # render each item accordingly depending on its type
            if item[T_ENTITY_ITEM_TYPE] == E_ENTITY_STRONG_SWORD:
                strong_sword_render(item[T_ENTITY_ITEM_DATA], assets)
