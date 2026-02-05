from src.engine.structs.base_entity import *


# ChaosSealT -> BaseEntityT
ChaosSealT = BaseEntityT

T_CHAOS_SEAL_COUNT = T_BASE_ENTITY_COUNT


def chaos_seal_create(room_pos: RoomPosT) -> ChaosSealT:
    return base_entity_create(entity_type=E_ENTITY_CHAOS_SEAL, room_pos=room_pos)

def chaos_seal_is_valid(chaos_seal) -> bool:
    return chaos_seal != None and isinstance(chaos_seal, list) and len(chaos_seal) == T_CHAOS_SEAL_COUNT

def chaos_seal_render(dungeon, chaos_seal: ChaosSealT, assets: AssetsT):
    if not chaos_seal_is_valid(chaos_seal):
        return

    image = assets[T_ASSETS_ITEMS][T_ITEMS_CHAOS_SEAL]
    base_entity_render(dungeon, chaos_seal, image, ITEM_SIZES)
