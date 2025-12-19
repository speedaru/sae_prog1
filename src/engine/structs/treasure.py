from src.engine.structs.dungeon import *
from src.engine.structs.entity import *

TreasureT = tuple[RoomPosT, int]
TREASURE_ROOM_POS = 0 # room position where treasure is
TREASURE_IMAGE_ID = 1 # image id
TREASURE_COUNT = 2

def treasure_create(room_pos: RoomPosT, image_id: int) -> TreasureT:
    return (room_pos, image_id)

def treasure_is_valid(treasure) -> bool:
    return treasure != None and isinstance(treasure, tuple) and len(treasure) == TREASURE_COUNT

def treasure_render(treasure: TreasureT, assets: AssetsT):
    if not treasure_is_valid(treasure):
        return

    image_id = treasure[TREASURE_IMAGE_ID]
    image = assets[ASSETS_TREASURES][image_id]
    entity_base_render(treasure[TREASURE_ROOM_POS], image)
