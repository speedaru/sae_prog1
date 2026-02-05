from src.engine.structs.dungeon import *
from src.engine.structs.entity import *

StrongSwordT = BaseEntityT
T_STRONG_SWORD_COUNT = T_BASE_ENTITY_COUNT

def strong_sword_create(room_pos: RoomPosT) -> StrongSwordT:
    return base_entity_create(entity_type=E_ENTITY_STRONG_SWORD, room_pos=room_pos)

def strong_sword_is_valid(strong_sword) -> bool:
    return strong_sword != None and isinstance(strong_sword, list) and len(strong_sword) == T_STRONG_SWORD_COUNT

def strong_sword_render(dungeon, strong_sword: StrongSwordT, assets: AssetsT):
    if not strong_sword_is_valid(strong_sword):
        return

    image = assets[T_ASSETS_ITEMS][T_ITEMS_STRONG_SWORD]
    base_entity_render(dungeon, strong_sword, image, ITEM_SIZES)
