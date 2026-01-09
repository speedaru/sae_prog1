# from typing import Any
#
# from src.game.game_definitions import *
# from src.engine.structs.base_entity import *
#
#
# # entity type (strong sword) + actual entity struct
# EntityItemT = list[int | Any]
#
# T_ENTITY_ITEM_TYPE = 0 # the entity type, like strong sword or wtv
# T_ENTITY_ITEM_DATA = 1 # the entity struct itself
# T_ENTITY_ITEM_COUNT = 2
#
# def entity_item_create(entity_item_type: int, entity):
#     entity_item: Any = [None] * T_ENTITY_ITEM_COUNT
#
#     entity_item[T_ENTITY_ITEM_TYPE] = entity_item_type
#     entity_item[T_ENTITY_ITEM_DATA] = entity
#
#     return entity_item
