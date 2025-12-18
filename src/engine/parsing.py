from types import NoneType
from typing import Any

from src.game.game_config import *
from src.engine.structs.dungeon import *
from src.engine.structs.entity import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *

import src.engine.game_logic as game_logic


# entity enums
ENTITY_UNKNOWN = 0xffff
ENTITY_ADVENTURER = 0
ENTITY_DRAGON = 1
ENTITY_TREASURE = 2
ENTITY_COUNT = 3

ENTITY_CHARS = { "A": ENTITY_ADVENTURER, "D": ENTITY_DRAGON, "T": ENTITY_TREASURE }

# dungeon rooms representations
ROOM_REPR4 = ("╬")
ROOM_REPR3 = ("╠", "╦", "╣", "╩")
ROOM_REPR2_ADJ = ("╚", "╔", "╗", "╝")
ROOM_REPR2_OPP = ("║", "═")
ROOM_REPR1 = ("╨", "╞", "╥","╡")
ROOM_REPS = set().union(ROOM_REPR4, ROOM_REPR3, ROOM_REPR2_ADJ, ROOM_REPR2_OPP, ROOM_REPR1)

_EntityTypeValueT = tuple[int, Any]

# dungeon, player, dragons, etc...
GameDataT = list[DungeonT | EntitiesT]
GAME_DATA_DUNGEON = 0
GAME_DATA_ENTITIES = 1
GAME_DATA_COUNT = 2

def game_data_init() -> GameDataT:
    game_data = [list() for _ in range(GAME_DATA_COUNT)]
    entities_init(game_data[GAME_DATA_ENTITIES])
    return game_data

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

def parse_entity(entity_fields: list[str]) -> _EntityTypeValueT:
    FIELD_ENTITY_TYPE = 0
    entity_type_ch: str | NoneType = _entity_get_field(entity_fields, FIELD_ENTITY_TYPE)
    if entity_type_ch == None:
        return (ENTITY_UNKNOWN, None)

    if not entity_type_ch in ENTITY_CHARS:
        log_error("unrecognized entity type: {entity_type}")
        return (ENTITY_UNKNOWN, None)

    entity_type = ENTITY_CHARS[entity_type_ch]
    # handle adventurer and dragon together at first
    if entity_type == ENTITY_ADVENTURER or entity_type == ENTITY_DRAGON:
        FIELD_POS_ROW = 1
        FIELD_POS_COL = 2
        row, col = _entity_get_field(entity_fields, FIELD_POS_ROW), _entity_get_field(entity_fields, FIELD_POS_COL)
        if isinstance(row, NoneType) or isinstance(col, NoneType):
            log_error(f"Adventurer parsing: failed to get room position from fields: {entity_fields}")
            return (ENTITY_UNKNOWN, None)

        # convert fields to int
        row, col = int(row), int(col)

        # now handle adventurer and dragon separatly
        if entity_type == ENTITY_ADVENTURER:
            # create adventurer
            adventurer: AdventurerT = AdventurerT()
            adventurer_init(adventurer, room_pos=room_pos_create(row=row, col=col))
            return (entity_type, adventurer)
        elif entity_type == ENTITY_DRAGON:
            FIELD_LEVEL = 3
            level = _entity_get_field(entity_fields, FIELD_LEVEL)
            if isinstance(level, NoneType):
                log_error(f"Dragon parsing: failed to get level from fields: {entity_fields}")
                return (ENTITY_UNKNOWN, None)

            # convert fields to int
            level = int(level)

            # create dragon
            dragon: DragonT = DragonT()
            dragon_init(dragon, level=level, room_pos=room_pos_create(row=row, col=col))
            return (entity_type, dragon)
    elif entity_type == ENTITY_TREASURE:
        pass

    return (ENTITY_UNKNOWN, None)

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
        # line starts with ╬
        if line[0] in ROOM_REPS:
            dungeon_lines.append(line)
        # line starts with A, D, T, ...
        elif line[0] in ENTITY_CHARS:
            entities_lines.append(line)
        else:
            log_error(f"failed to parse file, unrecognized line: {line}")

    dungeon: DungeonT = game_data[GAME_DATA_DUNGEON]
    # adventurer: AdventurerT = game_context[GAME_CONTEXT_ADVENTURER]
    # dragons: list[DragonT] = game_context[GAME_CONTEXT_DRAGONS]
    # dragons[:] = [] # reset dragons list

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
        if entity_type == ENTITY_UNKNOWN or entity == None:
            log_error(f"unrecognized entity: {entity_data}")
            continue

        if entity_type == ENTITY_ADVENTURER:
            game_data[GAME_DATA_ENTITIES][ENTITIES_ADVENTURER] = entity
            log_debug_full(f"loaded adventurer: {game_data[GAME_DATA_ENTITIES][ENTITIES_ADVENTURER]}")
        elif entity_type == ENTITY_DRAGON:
            dragons.append(entity)

    # game_logic.load_dragons(game_data, dragons)
    game_data[GAME_DATA_ENTITIES][ENTITIES_DRAGONS] = dragons

    log_debug_full(f"loaded dungeon: {game_data[GAME_DATA_DUNGEON]}")
    return True
