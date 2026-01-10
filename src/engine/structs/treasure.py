from src.engine.structs.dungeon import *
from src.engine.structs.entity import *

# BaseEntityT -> TreasureT
TreasureT = BaseEntityT | list[int]
T_TREASURE_IMAGE_ID = T_BASE_ENTITY_COUNT # image id, for different images for treasure
T_TREASURE_COUNT = T_BASE_ENTITY_COUNT + 1

def treasure_create(room_pos: RoomPosT, image_id: int) -> TreasureT:
    treasure: TreasureT = base_entity_create(entity_type=E_ENTITY_TREASURE, room_pos=room_pos, size=T_TREASURE_COUNT)

    treasure[T_TREASURE_IMAGE_ID] = image_id

    return treasure

def treasure_is_valid(treasure) -> bool:
    return treasure != None and isinstance(treasure, list) and len(treasure) == T_TREASURE_COUNT

def treasure_render(treasure: TreasureT, assets: AssetsT):
    if not treasure_is_valid(treasure):
        return

    image_id = treasure[T_TREASURE_IMAGE_ID]
    image = assets[T_ASSETS_ITEMS][image_id]
    base_entity_render(treasure, image, ITEM_SIZES)
