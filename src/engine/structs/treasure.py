from src.engine.structs.dungeon import *
from src.engine.structs.entity import *

# BaseEntityT -> TreasureT
TreasureT = list[RoomPosT | int]
T_TREASURE_IMAGE_ID = T_BASE_ENTITY_COUNT # image id, for different images for treasure
T_TREASURE_COUNT = T_BASE_ENTITY_COUNT + 1

def treasure_create(room_pos: RoomPosT, image_id: int) -> TreasureT:
    treasure: list = [None] * T_TREASURE_COUNT

    treasure[T_BASE_ENTITY_ROOM_POS] = room_pos
    treasure[T_TREASURE_IMAGE_ID] = image_id

    return treasure

def treasure_is_valid(treasure) -> bool:
    return treasure != None and isinstance(treasure, list) and len(treasure) == T_TREASURE_COUNT

def treasure_render(treasure: TreasureT, assets: AssetsT):
    if not treasure_is_valid(treasure):
        return

    image_id = treasure[T_TREASURE_IMAGE_ID]
    image = assets[T_ASSETS_ITEMS][image_id]
    base_entity_render(treasure, image)
