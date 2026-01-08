import json
from types import NoneType
from typing import Any

from src.config import *

from src.game.game_definitions import *

# import src.engine.game_logic as game_logic
from src.engine.structs.dungeon import *
from src.engine.structs.entity import *
from src.engine.structs.entities import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *

from src.utils.file_utils import path_exists


# dungeon rooms representations
ROOM_REPR4 = ("╬")
ROOM_REPR3 = ("╠", "╦", "╣", "╩")
ROOM_REPR2_ADJ = ("╚", "╔", "╗", "╝")
ROOM_REPR2_OPP = ("║", "═")
ROOM_REPR1 = ("╨", "╞", "╥","╡")
ROOM_REPS = set().union(ROOM_REPR4, ROOM_REPR3, ROOM_REPR2_ADJ, ROOM_REPR2_OPP, ROOM_REPR1)

_EntityTypeValueT = tuple[int, Any]

_SimpleGameCtxT = list[int | GameDataT]
_T_SIMPLE_GAME_CTX_GAME_STATE = 0
_T_SIMPLE_GAME_CTX_GAME_DATA = 1
_T_SIMPLE_GAME_CTX_ORIGINAL_GAME_DATA = 2
_T_SIMPLE_GAME_CTX_COUNT = 3


def dungeon_ascii_to_room(ascii_room: str) -> RoomT:
    """
    Converts an ASCII character from a dungeon file into a Room structure.

    Args:
        ascii_room (str): The character representing the room (e.g., '╬', '╠').

    Returns:
        RoomT: The corresponding room structure [BlockID, RotationCount].
    """

    log_debug_full(f"[dungeon_ascii_to_room] ascii room: {ascii_room}")

    room = dungeon_room_create()
    if ascii_room in ROOM_REPR4:
        room = dungeon_room_create(BLOCK_QUAD, 0)
    elif ascii_room in ROOM_REPR3:
        room = dungeon_room_create(BLOCK_TRIPLE, ROOM_REPR3.index(ascii_room))
    elif ascii_room in ROOM_REPR2_ADJ:
        room = dungeon_room_create(BLOCK_DOUBLE_ADJACENT, ROOM_REPR2_ADJ.index(ascii_room))
    elif ascii_room in ROOM_REPR2_OPP:
        room = dungeon_room_create(BLOCK_DOUBLE_OPPOSITE, ROOM_REPR2_OPP.index(ascii_room))
    elif ascii_room in ROOM_REPR1:
        room = dungeon_room_create(BLOCK_SINGLE, ROOM_REPR1.index(ascii_room))

    return room

# returns True if successfuly parsed file
def parse_dungeon(dungeon: DungeonT, dungeon_lines: list[str]) -> bool:
    """
    Parses a dungeon layout from a text file and populates the dungeon structure.
    """
    # ensure number of rows is not 0
    if len(dungeon_lines) == 0:
        log_release("[dungeon] invalid row count in dungeon: '{dungeon_file_path}'")
        return False

    # get dungeon dimensions
    row_count = len(dungeon_lines)
    col_count = len(dungeon_lines[0])

    # ensure each row is same size
    for col_list in dungeon_lines:
        curr_cols = len(col_list)
        if curr_cols != col_count:
            log_release("[dungeon] inconsistent column count ({cols} and {curr_cols}) in dungeon: '{dungeon_file_path}'")
            return False

    log_debug(f"[dungeon] rows, cols: ({row_count}, {col_count})")
    
    # init dungeon with empty values so we can index rows and cols
    dungeon_init(dungeon, row_count, col_count)
    log_debug("[dungeon] initialized empty dungeon")

    # parse each room and fill the dungeon
    for i, row in enumerate(dungeon_lines):
        for j, col in enumerate(row):
            dungeon[i][j] = dungeon_ascii_to_room(col)
            log_debug(f"[dungeon] set dungeon room to {dungeon[i][j]}")

    return True

def _entity_get_field(fields: list[str], field_idx: int) -> str | NoneType:
    if field_idx >= len(fields):
        log_error(f"failed to get field {field_idx} in fields: {fields}")
        return None

    return fields[field_idx]

def _fields_get_room_pos(fields: list[str]) -> RoomPosT | NoneType:
    FIELD_POS_ROW = 1
    FIELD_POS_COL = 2
    row, col = _entity_get_field(fields, FIELD_POS_ROW), _entity_get_field(fields, FIELD_POS_COL)
    if not row or not col:
        log_error(f"fields get room pos parsing: failed to get room position from fields: {fields}")
        return None

    # convert fields to int
    row, col = int(row), int(col)
    return room_pos_create(row=row, col=col)

def parse_entity(entity_fields: list[str]) -> _EntityTypeValueT:
    unknown_ent = (E_ENTITY_UNKNOWN, None)

    FIELD_ENTITY_TYPE = 0
    entity_type_ch: str | NoneType = _entity_get_field(entity_fields, FIELD_ENTITY_TYPE)
    if entity_type_ch == None:
        return unknown_ent

    if not entity_type_ch in ENTITY_CHARS:
        log_error("unrecognized entity type: {entity_type}")
        return unknown_ent

    entity_type = ENTITY_CHARS[entity_type_ch]
    if entity_type == E_ENTITY_ADVENTURER:
        room_pos_res: RoomPosT | NoneType = _fields_get_room_pos(entity_fields)
        if not room_pos_res:
            return unknown_ent

        # create adventurer
        adventurer: AdventurerT = AdventurerT()
        adventurer_init(adventurer, room_pos=room_pos_res)
        return (entity_type, adventurer)
    elif entity_type == E_ENTITY_DRAGON:
        # get room pos
        room_pos_res: RoomPosT | NoneType = _fields_get_room_pos(entity_fields)
        if not room_pos_res:
            return unknown_ent

        # get level
        FIELD_LEVEL = 3
        level = _entity_get_field(entity_fields, FIELD_LEVEL)
        if not level:
            return unknown_ent

        # convert fields to int
        level = int(level)

        # create dragon
        dragon: DragonT = DragonT()
        dragon_init(dragon, level=level, room_pos=room_pos_res)
        return (entity_type, dragon)
    elif entity_type == E_ENTITY_TREASURE:
        FIELD_TREASURE_COUNT = 1
        count = _entity_get_field(entity_fields, FIELD_TREASURE_COUNT)
        if isinstance(count, NoneType):
            log_error("Treasure parse: failed to get number of treasures in dungeon from fields: {entity_fields}")
            return unknown_ent

        return (entity_type, int(count))
    elif entity_type == E_ENTITY_STRONG_SWORD:
        room_pos_res: RoomPosT | NoneType = _fields_get_room_pos(entity_fields)
        if not room_pos_res:
            return unknown_ent

        # create strong sword
        return (entity_type, strong_sword_create(room_pos_res))

    return (E_ENTITY_UNKNOWN, None)

def game_data_parse_file(game_data: GameDataT, game_save_file_path: str) -> bool:
    # read file
    file_data: str = read_utf8_file(game_save_file_path)
    if file_data == "":
        log_release(f"[dungeon] failed to read {game_save_file_path}")
        return False

    # separate dungeon, entities
    dungeon_lines: list[str] = []
    entities_lines: list[str] = []
    for line in file_data.split("\n"):
        if line == "":
            continue

        # line starts with ╬
        if line[0] in ROOM_REPS:
            dungeon_lines.append(line)
        # line starts with A, D, T, ...
        elif line[0] in ENTITY_CHARS:
            entities_lines.append(line)
        else:
            log_error(f"failed to parse file, unrecognized line: {line}")

    dungeon: DungeonT = game_data[T_GAME_DATA_DUNGEON]

    log_debug(f"dungeon lines: {dungeon_lines=}")
    log_debug(f"entity lines: {entities_lines=}")

    # parse dungeon
    parse_dungeon(dungeon, dungeon_lines)

    # parse entities
    dragons: list[DragonT] = []
    for entity_data in entities_lines:
        # "A 0 1" -> ["A", "0", "1"]
        entity_fields = entity_data.split(" ")

        entity_type, entity = parse_entity(entity_fields)
        if entity_type == E_ENTITY_UNKNOWN or entity == None:
            log_error(f"unrecognized entity: {entity_data}")
            continue

        if entity_type == E_ENTITY_ADVENTURER:
            game_data[T_GAME_DATA_ENTITIES][T_ENTITIES_ADVENTURER] = entity
            log_debug_full(f"loaded adventurer: {game_data[T_GAME_DATA_ENTITIES][T_ENTITIES_ADVENTURER]}")
        elif entity_type == E_ENTITY_DRAGON:
            dragons.append(entity)
        elif entity_type == E_ENTITY_TREASURE:
            log_debug_full(f"found treasure count: {entity}")
            game_data[T_GAME_DATA_TREASURE_COUNT] = entity
        elif entity_type in E_ENTITY_ITEMS: # any entity item
            entity_item = entity_item_create(entity_type, entity)
            game_data[T_GAME_DATA_ENTITIES][T_ENTITIES_ITEMS].append(entity_item)
            log_debug_full(f"loaded entity item: {entity_type}")

    # game_logic.load_dragons(game_data, dragons)
    game_data[T_GAME_DATA_ENTITIES][T_ENTITIES_DRAGONS] = dragons

    log_debug_full(f"loaded dungeon: {game_data[T_GAME_DATA_DUNGEON]}")
    return True

def _to_json_safe(obj) -> str:
    if isinstance(obj, tuple):
        return {"__tuple__": [_to_json_safe(x) for x in obj]}
    elif isinstance(obj, list):
        return [_to_json_safe(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: _to_json_safe(v) for k, v in obj.items()}
    else:
        # int, float, str, bool, None
        return obj

def _from_json_safe(obj):
    if isinstance(obj, dict):
        if "__tuple__" in obj:
            return tuple(_from_json_safe(x) for x in obj["__tuple__"])
        return {k: _from_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_from_json_safe(x) for x in obj]
    else:
        return obj

def serialize_game_context(game_context: GameContextT) -> str:
    simple_game_context: list = [_SimpleGameCtxT()] * _T_SIMPLE_GAME_CTX_COUNT
    simple_game_context[_T_SIMPLE_GAME_CTX_GAME_STATE] = game_context[T_GAME_CONTEXT_GAME_STATE]
    simple_game_context[_T_SIMPLE_GAME_CTX_GAME_DATA] = game_context[T_GAME_CONTEXT_GAME_DATA]
    simple_game_context[_T_SIMPLE_GAME_CTX_ORIGINAL_GAME_DATA] = game_context[T_GAME_CONTEXT_ORIGINAL_GAME_DATA]

    ret = _to_json_safe(simple_game_context)
    log_debug_full(f"serialized:\n{ret}")

    return json.dumps(ret)

def deserialize_game_context(game_context: GameContextT, serialized_data: str):
    deserialized_simple_game_context = _from_json_safe(json.loads(serialized_data))

    game_context[T_GAME_CONTEXT_GAME_STATE] = deserialized_simple_game_context[_T_SIMPLE_GAME_CTX_GAME_STATE]
    game_context[T_GAME_CONTEXT_GAME_DATA][:] = deserialized_simple_game_context[_T_SIMPLE_GAME_CTX_GAME_DATA]
    game_context[T_GAME_CONTEXT_ORIGINAL_GAME_DATA][:] = deserialized_simple_game_context[_T_SIMPLE_GAME_CTX_ORIGINAL_GAME_DATA]

def save_game(game_context: GameContextT):
    """
    saves game context to a file
    """
    serialized_data: str = serialize_game_context(game_context)

    with open(GAME_SAVE_FILE_PATH, "w") as f:
        f.write(serialized_data)

def load_saved_game(game_context):
    """
    reaload game context from file
    """
    # if save file doesnt exist do nothing
    if not path_exists(GAME_SAVE_FILE_PATH):
        return

    serialized_data = ""

    with open(GAME_SAVE_FILE_PATH, "r") as f:
        serialized_data = f.read()

    # reload game_context
    deserialize_game_context(game_context, serialized_data)

