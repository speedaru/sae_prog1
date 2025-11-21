from src.engine.structs.entity import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *
from src.engine.structs.dungeon import *


def find_closest_dragon(dragons: list[DragonT]) -> DragonT | NoneType:
    if len(dragons) == 0:
        return None

    return dragons[randrange(0, len(dragons))]

def find_path(adventurer: AdventurerT, target_room: RoomPosT) -> MovementPathT:
    return [target_room]

def is_valid_path(path: MovementPathT) -> bool:
    return True

def find_and_set_adventurer_path(adventurer: AdventurerT, dragons: list[DragonT]):
    # find closest dragon with highest level
    target_dragon = find_closest_dragon(dragons)
    if target_dragon == None:
        return

    dragon_pos: RoomPosT = target_dragon[ENTITY_ROOM_POS]
    adventurer[ADVENTURER_PATH] = find_path(adventurer, dragon_pos)

def do_adventurer_path(adventurer: AdventurerT):
    movement_path = adventurer[ADVENTURER_PATH]

    # if no path
    if not isinstance(movement_path, list) or len(movement_path) == 0:
        return

    adventurer[ENTITY_ROOM_POS] = movement_path[-1]

