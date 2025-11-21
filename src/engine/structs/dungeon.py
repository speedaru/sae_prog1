import libs.fltk as fltk

from src.utils.file_utils import read_utf8_file
import src.utils.fltk_extensions as fltk_ext

from src.engine.asset_manager import *


# first int corresponds to block index (inside asset_manager)
# second int corresponds to how many times we need to rotate it (clockwise)
RoomT = list[int]
RoomConnectionsT = tuple[bool, bool, bool, bool]
DungeonT = list[list[RoomT]] # nxn matrix of rooms

ROOM_BLOCK_ID = 0
ROOM_ROTATION_COUNT = 1


# ---------- MANIPULATION FUNCTIONS ----------

def dungeon_room_init() -> RoomT:
    """src/engine/structs/dungeon.py
    Initializes an empty room structure.

    Returns:
        RoomT: A list representing a room, initialized to block ID 0 (Solid) and 0 rotations.

    Doctest :

    >>> dungeon_room_init()
    [0, 0]
    """
    return [0, 0]

# initalizes dungeon in ``dungeon`` bcs its passed by reference
def dungeon_init(dungeon: DungeonT, rows: int, cols: int) -> NoneType:
    """
    Initializes the dungeon grid with empty rooms.
    
    The dungeon list is modified in-place.

    Args:
        dungeon (DungeonT): The dungeon list to initialize.
        rows (int): Number of rows.
        cols (int): Number of columns.
    
    Doctest :

    >>> d = []
    >>> dungeon_init(d, 2, 3)
    >>> # Check dimensions (2 rows, 3 cols)
    >>> len(d)
    2
    >>> len(d[0])
    3
    >>> # Check first room content
    >>> d[0][0]
    [0, 0]
    """
    dungeon.clear()

    # init each line with col amount of empty rooms
    for _ in range(rows):
        dungeon.append([dungeon_room_init()] * cols)

def dungeon_room_get_connections(room: RoomT) -> RoomConnectionsT:
    """
    Calculates the open connections (doors) of a room based on its block type and rotation.

    Args:
        room (RoomT): The room structure [BlockID, RotationCount].

    Returns:
        RoomConnectionsT: A tuple of 4 booleans (Up, Right, Down, Left) indicating open paths.

    Doctest :

    >>> # BLOCK_SINGLE (1 connection Up by default)
    >>> # With 0 rotation: Up=True
    >>> dungeon_room_get_connections([BLOCK_SINGLE, 0])
    (True, False, False, False)

    >>> # With 1 rotation (90 deg clockwise): Right=True
    >>> dungeon_room_get_connections([BLOCK_SINGLE, 1])
    (False, True, False, False)

    >>> # BLOCK_DOUBLE_ADJACENT (Up and Right by default)
    >>> dungeon_room_get_connections([BLOCK_DOUBLE_ADJACENT, 0])
    (True, True, False, False)
        
    >>> # BLOCK_QUAD (All sides open), rotation doesn't change connectivity
    >>> dungeon_room_get_connections([BLOCK_QUAD, 1])
    (True, True, True, True)
    """
    DOOR_COUNT = 4

    # init room connections that we will change and convert to tuple at end
    room_connections: list[bool] = [False] * DOOR_COUNT

    # check if room is invalid
    if room[ROOM_BLOCK_ID] >= BLOCK_COUNT:
        return tuple(room_connections) # invalid room_id

    # get room basic door setup
    room_id = room[ROOM_BLOCK_ID]

    if room_id == BLOCK_SINGLE:
        room_connections = [True, False, False, False]
    elif room_id == BLOCK_DOUBLE_ADJACENT:
        room_connections = [True, True, False, False]
    elif room_id == BLOCK_DOUBLE_OPPOSITE:
        room_connections = [True, False, True, False]
    elif room_id == BLOCK_TRIPLE:
        room_connections = [True, True, True, False]
    elif room_id == BLOCK_QUAD:
        room_connections = [True, True, True, True]

    # rotate room
    room_rotations = room[ROOM_ROTATION_COUNT]
    rotated_room_connections = [False] * DOOR_COUNT

    # move door open state forward room_rotations % DOOR_COUNT times
    for i in range(DOOR_COUNT):
        rotated_i = (i + room_rotations) % DOOR_COUNT
        rotated_room_connections[rotated_i] = room_connections[i]

    return tuple(rotated_room_connections)

def dungeon_room_pos_in_bounds(dungeon: DungeonT, row: int, col: int) -> bool:
    return col < dungeon_get_width(dungeon) and row < dungeon_get_height(dungeon)

# returns nonetype if out of bounds
def dungeon_get_room_from_pos(dungeon: DungeonT, pos: tuple[int, int]) -> tuple[int, int] | NoneType:
    room_col: int = pos[0] // BLOCK_SCALED_SIZE[0]
    room_row: int = pos[1] // BLOCK_SCALED_SIZE[1]

    # invalid selection, out of bounds
    if not dungeon_room_pos_in_bounds(dungeon, room_row, room_col):
        return None

    return (room_row, room_col)

# returns True if successfuly rotated room
def dungeon_rotate_room(dungeon: DungeonT, row: int, col: int) -> bool:
    """
    Rotates a specific room in the dungeon by 90 degrees clockwise.

    Args:
        dungeon (DungeonT): The dungeon structure.
        row (int): Row index of the room.
        col (int): Column index of the room.

    Returns:
        bool: True if rotation was successful, False if coordinates are out of bounds.

    Doctest :

    >>> d = []
    >>> dungeon_init(d, 1, 1)
    >>> # Initial state: rotation 0
    >>> d[0][0]
    [0, 0]
    >>> # Rotate room at (0, 0)
    >>> dungeon_rotate_room(d, 0, 0)
    True
    >>> # New state: rotation 1
    >>> d[0][0]
    [0, 1]
    >>> # Try to rotate out of bounds
    >>> dungeon_rotate_room(d, 5, 5)
    False
    """
    # check if room in bounds
    if not dungeon_room_pos_in_bounds(dungeon, row, col):
        return False

    dungeon[row][col][ROOM_ROTATION_COUNT] += 1

    return True

# returns number of rooms horizontally
def dungeon_get_width(dungeon: DungeonT) -> int:
    """
    Gets the width (number of columns) of the dungeon.

    Doctest :

    >>> d = []
    >>> dungeon_init(d, 5, 3) # 5 rows, 3 cols
    >>> dungeon_get_width(d)
    3
    >>> dungeon_get_width([])
    0
    """
    # dungeon empty
    if len(dungeon) == 0:
        return 0
    
    # each room is same size so return size of first column
    return len(dungeon[0])

# returns number of rooms vertically
def dungeon_get_height(dungeon: DungeonT) -> int:
    """
    Gets the height (number of rows) of the dungeon.

    Doctest :

    >>> d = []
    >>> dungeon_init(d, 5, 3)
    >>> dungeon_get_height(d)
    5
    >>> dungeon_get_height([])
    0
    """
    return len(dungeon)

# ---------- PARSING ----------

def dungeon_ascii_to_room(ascii_room: str) -> RoomT:
    """
    Converts an ASCII character from a dungeon file into a Room structure.

    Args:
        ascii_room (str): The character representing the room (e.g., '╬', '╠').

    Returns:
        RoomT: The corresponding room structure [BlockID, RotationCount].
    """
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
def dungeon_parse_file(dungeon: DungeonT, dungeon_file_path: str) -> bool:
    """
    Parses a dungeon layout from a text file and populates the dungeon structure.
    """
    # read file
    file_data: str = read_utf8_file(dungeon_file_path)
    if file_data == "":
        log_release(f"[dungeon] failed to read {dungeon_file_path}")
        return False

    # get dungeon rows
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
    
    # init dungeon with empty values so we can index rows and cols without oob error
    dungeon_init(dungeon, rows, cols)
    log_debug("[dungeon] initialized empty dungeon")

    # parse each room and fill the dungeon
    for i, row in enumerate(row_list):
        for j, col in enumerate(row):
            dungeon[i][j] = dungeon_ascii_to_room(col)
            log_debug(f"[dungeon] set dungeon room to {dungeon[i][j]}")

    return True

def dungeon_print_values(dungeon: DungeonT):
    """
    Prints the raw values of the dungeon structure to the console for debugging.
    """
    for row in dungeon:
        print(row)


# ---------- RENDERING ----------

def dungeon_room_render(room: RoomT, assets: AssetsT, x: float, y: float):
    """
    Renders a single room at the specified coordinates.
    
    Draws the background first, then the room block on top.
    """
    # draw wall background for block
    wall_background_image = asset_manager_get_block(assets, BLOCK_WALL_BACKGROUND, 0)
    fltk_ext.image_memoire(x, y, wall_background_image, ancrage="nw")

    # draw room block on top of wall background
    block_image = asset_manager_get_block(assets, room[ROOM_BLOCK_ID], room[ROOM_ROTATION_COUNT])
    fltk_ext.image_memoire(x, y, block_image, ancrage="nw")

def dungeon_render(dungeon: DungeonT, assets: AssetsT):
    """
    Iterates through the entire dungeon grid and renders each room.
    """
    # don't render dungeon if NoneType or no rows
    if isinstance(dungeon, NoneType) or dungeon_get_height(dungeon) == 0:
        return

    for i, row in enumerate(dungeon): # draw rows
        for j, room in enumerate(row): # draw each individual room
            # get room coordinates
            x = j * BLOCK_SCALED_SIZE[0]
            y = i * BLOCK_SCALED_SIZE[1]

            # draw room
            dungeon_room_render(room, assets, x, y)
