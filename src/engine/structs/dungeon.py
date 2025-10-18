from src.utils.file_utils import read_utf8_file

from src.engine.asset_manager import *


# first int corresponds to block index (inside asset_manager)
# second int corresponds to how many times we need to rotate it (clockwise)
RoomT = list[int]
DungeonT = list[list[RoomT]]

ROOM_BLOCK_IDX = 0
ROOM_ROTATION_COUNT = 0

def dungeon_room_init() -> RoomT:
    return [0, 0]

# initalizes dungeon in ``dungeon`` bcs its passed by reference
def dungeon_init(dungeon: DungeonT, rows: int, cols: int) -> NoneType:
    dungeon.clear()

    # init each line with col amount of empty rooms
    for _ in range(rows):
        dungeon.append([dungeon_room_init()] * cols)

def dungeon_ascii_to_room(ascii_room: str) -> RoomT:
    REPR4 = ("╬")
    REPR3 = ("╠", "╦", "╣", "╩")
    REPR2_ADJ = ("╚", "╔", "╗", "╝")
    REPR2_OPP = ("║", "═")
    REPR1 = ("╨", "╞", "╥","╡")

    ROOM = [0, 0]

    log_debug_full(f"[dungeon_ascii_to_room] ascii room: {ascii_room}")

    if ascii_room in REPR4:
        ROOM = [BLOCK_QUAD, 0]
    elif ascii_room in REPR3:
        ROOM = [BLOCK_TRIPLE, REPR3.index(ascii_room)]
    elif ascii_room in REPR2_ADJ:
        ROOM = [BLOCK_DOUBLE_ADJACENT, REPR2_ADJ.index(ascii_room)]
    elif ascii_room in REPR2_OPP:
        ROOM = [BLOCK_DOUBLE_OPPOSITE, REPR2_OPP.index(ascii_room)]
    elif ascii_room in REPR1:
        ROOM = [BLOCK_SINGLE, REPR1.index(ascii_room)]

    return ROOM

# returns True if successfuly parsed file
def dungeon_parse_file(dungeon_file_path: str, dungeon: DungeonT) -> bool:
    file_data: str = read_utf8_file(dungeon_file_path)
    if file_data == "":
        log_release(f"[dungeon] failed to read {dungeon_file_path}")
        return False

    row_list = file_data.split("\n")

    # ensure number of rows is not 0
    rows = len(row_list)
    if rows == 0:
        log_release("[dungeon] invalid row count in dungeon: '{dungeon_file_path}'")
        return False

    # ensure each row is same size
    cols = len(row_list[0])
    for col_list in row_list:
        curr_cols = len(col_list)
        if curr_cols != cols:
            log_release("[dungeon] inconsistent column count ({cols} and {curr_cols}) in dungeon: '{dungeon_file_path}'")
            return False

    log_debug(f"[dungeon] rows, cols: ({rows}, {cols})")
    
    dungeon_init(dungeon, rows, cols)
    log_debug("[dungeon] initialized empty dungeon")

    for i, row in enumerate(row_list):
        for j, col in enumerate(row):
            dungeon[i][j] = dungeon_ascii_to_room(col)
            log_debug(f"[dungeon] set dungeon room to {dungeon[i][j]}")

    return True

def dungeon_print_values(dungeon: DungeonT):
    for row in dungeon:
        print(row)

def dungeon_room_render(x: float, y: float, room: RoomT):
    fltk.image_memoire(x, y, asset_manager_get_block(room[0], room[1]), ancrage="nw")

def dungeon_render(dungeon: DungeonT):
    for i, row in enumerate(dungeon):
        for j, room in enumerate(row):
            x = j * BLOCK_SCALED_SIZE[0]
            y = i * BLOCK_SCALED_SIZE[1]
            dungeon_room_render(x, y, room)
