import libs.fltk as fltk

from src.utils.file_utils import read_utf8_file
import src.utils.fltk_extensions as fltk_ext

from src.engine.asset_manager import *


# first int corresponds to block index (inside asset_manager)
# second int corresponds to how many times we need to rotate it (clockwise)
RoomT = tuple[int, int]
ROOM_BLOCK_ID = 0
ROOM_ROTATION_COUNT = 1
ROOM_COUNT = 2

DungeonT = list[list[RoomT]] # n x n matrix of rooms

RoomConnectionsT = tuple[bool, bool, bool, bool]
ROOM_CONNECTION_UP = 0
ROOM_CONNECTION_RIGHT = 1
ROOM_CONNECTION_DOWN = 2
ROOM_CONNECTION_LEFT = 3

RoomPosT = tuple[int, int]
ROOM_POS_COL = 0
ROOM_POS_ROW = 1
ROOM_POS_COUNT = 2

DungeonSizeT = RoomPosT # alias cuz also cols x rows
DUNGEON_SIZE_COL = ROOM_POS_COL
DUNGEON_SIZE_ROW = ROOM_POS_ROW

# ---------- MANIPULATION FUNCTIONS ----------

def room_pos_create(col: int, row: int) -> RoomPosT:
    """
    create a room pos depending on row col or col or row system

    Doctest:
    >>> ROOM_POS_COL = 0
    >>> ROOM_POS_ROW = 1
    >>> room_pos_create(col=5, row=6)
    (5, 6)
    """
    room_pos = [0] * ROOM_POS_COUNT
    room_pos[ROOM_POS_COL] = col
    room_pos[ROOM_POS_ROW] = row

    return RoomPosT(room_pos)

def dugeon_size_create(cols: int, rows: int):
    return room_pos_create(col=cols, row=rows)

def dungeon_room_create(block_id: int = 0, rotation_count: int = 0) -> RoomT:
    """src/engine/structs/dungeon.py
    Initializes an empty room structure.

    Returns:
        RoomT: A list representing a room, initialized to block ID 0 (Solid) and 0 rotations.

    Doctest :

    >>> dungeon_room_create()
    (0, 0)
    """
    room = [0] * ROOM_COUNT
    room[ROOM_BLOCK_ID] = block_id
    room[ROOM_ROTATION_COUNT] = rotation_count

    return RoomT(room)

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
    (0, 0)
    """
    dungeon.clear()

    # init each line with col amount of empty rooms
    for _ in range(rows):
        dungeon.append([dungeon_room_create()] * cols)

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
    room_connections: RoomConnectionsT = RoomConnectionsT()

    # check if room is invalid
    if room[ROOM_BLOCK_ID] >= BLOCK_COUNT:
        return room_connections # invalid room_id

    # get room basic door setup
    room_id = room[ROOM_BLOCK_ID]

    if room_id == BLOCK_SINGLE:
        room_connections = (True, False, False, False)
    elif room_id == BLOCK_DOUBLE_ADJACENT:
        room_connections = (True, True, False, False)
    elif room_id == BLOCK_DOUBLE_OPPOSITE:
        room_connections = (True, False, True, False)
    elif room_id == BLOCK_TRIPLE:
        room_connections = (True, True, True, False)
    elif room_id == BLOCK_QUAD:
        room_connections = (True, True, True, True)

    # rotate room
    room_rotations = room[ROOM_ROTATION_COUNT]
    rotated_room_connections = [False] * DOOR_COUNT

    # move door open state forward room_rotations % DOOR_COUNT times
    for i in range(DOOR_COUNT):
        rotated_i = (i + room_rotations) % DOOR_COUNT
        rotated_room_connections[rotated_i] = room_connections[i]

    return RoomConnectionsT(rotated_room_connections)

def dungeon_get_room_distance(room1: RoomPosT, room2: RoomPosT) -> int:
    """
    get distance between 2 rooms

    >>> dungeon_get_room_distance((1, 1), (2, 2))
    2
    >>> dungeon_get_room_distance((1, 1), (1, 2))
    1
    >>> dungeon_get_room_distance(None, (1, 2))
    """
    # invalid input
    if not isinstance(room1, tuple) or len(room1) != 2 or not isinstance(room2, tuple) or len(room2) != 2:
        return None

    # dx is col difference dy is row difference
    dx = abs(room1[ROOM_POS_COL] - room2[ROOM_POS_COL])
    dy = abs(room1[ROOM_POS_ROW] - room2[ROOM_POS_ROW])

    # return sum of delta
    return dx + dy

def dungeon_rooms_connected(room1: RoomT, room1_pos: RoomPosT, room2: RoomT, room2_pos: RoomPosT):
    """
    roomx: room rotation and connections representation
    roox_pos: room location in dungeon

    check to see if 2 rooms are connected:
        - rooms have a distance of 1
        - rooms have connecting doors

    Doctest:

    >>> # Set up constants for doctests (mimicking user's environment)
    >>> QUAD = [BLOCK_QUAD, 0] # (T, T, T, T)
    >>> VERTICAL_OPPOSITE = [BLOCK_DOUBLE_OPPOSITE, 0] # '║' (T, F, T, F)
    >>> HORIZONTAL_OPPOSITE = [BLOCK_DOUBLE_OPPOSITE, 1] # '═' (F, T, F, T)

    >>> # CASE 1: Connected - QUAD at (1, 1) next to VERTICAL_OPPOSITE at (1, 2) (Below)
    >>> # Room1 (1, 1) -> Down is T. Room2 (1, 2) -> Up is T. Connected.
    >>> dungeon_rooms_connected(QUAD, (1, 1), VERTICAL_OPPOSITE, (1, 2))
    True

    >>> # CASE 2: Connected - QUAD at (1, 1) next to HORIZONTAL_OPPOSITE at (2, 1) (Right)
    >>> # Room1 (1, 1) -> Right is T. Room2 (2, 1) -> Left is T. Connected.
    >>> dungeon_rooms_connected(QUAD, (1, 1), HORIZONTAL_OPPOSITE, (2, 1))
    True

    >>> # CASE 3: Not connected - Doors not aligned (Horizontal next to Horizontal)
    >>> # Room1: HORIZONTAL_OPPOSITE ('═') at (1, 1). Connections: (F, T, F, T)
    >>> # Room2: HORIZONTAL_OPPOSITE ('═') at (2, 1) (Right). Connections: (F, T, F, T)
    >>> # Room1 Right is T. Room2 Left is T. Connected. (Original doctest was flawed, fixed here)
    >>> dungeon_rooms_connected(HORIZONTAL_OPPOSITE, (1, 1), HORIZONTAL_OPPOSITE, (2, 1))
    True

    >>> # CASE 4: Not connected - Distance > 1
    >>> dungeon_rooms_connected(QUAD, (1, 1), QUAD, (3, 3))
    False
    
    >>> # CASE 5: Not connected - Doors closed (Horizontal next to Vertical)
    >>> # Room1: HORIZONTAL_OPPOSITE ('═') at (1, 1) -> Down is F (Index 2).
    >>> # Room2: VERTICAL_OPPOSITE ('║') at (1, 2) (Below) -> Up is T (Index 0).
    >>> # Room1 needs Down exit, but only has Left/Right.
    >>> dungeon_rooms_connected(HORIZONTAL_OPPOSITE, (1, 1), VERTICAL_OPPOSITE, (1, 2))
    False
    """
    # adjacent rooms must have a distance of 1
    distance = dungeon_get_room_distance(room1_pos, room2_pos)
    if distance != 1:
        return False

    # get up, right, down, left connections
    room1_connections = dungeon_room_get_connections(room1)
    room2_connections = dungeon_room_get_connections(room2)

    # calculate relative position
    # dx = col difference, dy = row difference
    dx = room2_pos[ROOM_POS_COL] - room1_pos[ROOM_POS_COL]
    dy = room2_pos[ROOM_POS_ROW] - room1_pos[ROOM_POS_ROW]

    # check aligned doors based on rel pos
    if dy == 1 and dx == 0:
        return room1_connections[2] and room2_connections[0]
    elif dy == -1 and dx == 0:
        return room1_connections[0] and room2_connections[2]
    elif dx == 1 and dy == 0:
        return room1_connections[1] and room2_connections[3]
    elif dx == -1 and dy == 0:
        return room1_connections[3] and room2_connections[1]

def dungeon_room_pos_in_bounds(dungeon: DungeonT, room_pos: RoomPosT) -> bool:
    # check if negative values
    if room_pos[ROOM_POS_COL] < 0 or room_pos[ROOM_POS_ROW] < 0:
        return False

    return room_pos[ROOM_POS_COL] < dungeon_get_width(dungeon) and room_pos[ROOM_POS_ROW] < dungeon_get_height(dungeon)

def dungeon_get_room_from_pos(dungeon: DungeonT, pos: tuple[int, int]) -> RoomPosT | NoneType:
    """
    returns nonetype if out of bounds
    """
    room_col: int = pos[0] // BLOCK_SCALED_SIZE[0]
    room_row: int = pos[1] // BLOCK_SCALED_SIZE[1]

    # invalid selection, out of bounds
    if not dungeon_room_pos_in_bounds(dungeon, room_row, room_col):
        return None

    return room_pos_create(col=room_col, row=room_row)

def dungeon_get_valid_neighbor_rooms(dungeon: DungeonT, current_room_pos: RoomPosT) -> list[RoomPosT]:
    """
    Retourne la liste des positions de salles voisines immédiatement adjacentes 
    et connectées à la salle actuelle (validé par les portes).

    Args:
        dungeon: La structure complète du donjon.
        current_room_pos: La position actuelle de la salle (col, row).

    Returns:
        list[RoomPosT]: Liste des positions des salles voisines connectées.

    Doctest:
    >>> # Setup a 2x2 dungeon: All QUAD rooms (all connections possible)
    >>> D = [[[BLOCK_QUAD, 0], [BLOCK_QUAD, 0]], [[BLOCK_QUAD, 0], [BLOCK_QUAD, 0]]]
    >>> # CASE 1: Center room (1, 0) should connect to (0, 0) Left, (1, 1) Down
    >>> # (0, 0) is Row 0, Col 0. (1, 0) is Row 0, Col 1.
    >>> dungeon_get_valid_neighbor_rooms(D, room_pos_create(col=0, row=0))
    [(1, 0), (0, 1)]
    
    >>> # CASE 2: Edge room (1, 1) should connect to (0, 1) Left, (1, 0) Up
    >>> # (1, 1) is Row 1, Col 1.
    >>> dungeon_get_valid_neighbor_rooms(D, room_pos_create(col=1, row=1))
    [(1, 0), (0, 1)]
    
    >>> # CASE 3: Restrictive Room. Room at (0, 0) has only UP connection open.
    >>> # Neighbor at (1, 0) is Quad (all open).
    >>> D2 = [[[BLOCK_SINGLE, 0], [BLOCK_QUAD, 0]], [[BLOCK_QUAD, 0], [BLOCK_QUAD, 0]]]
    >>> # Room at (0, 0) only allows UP. Neighbor above is OOB.
    >>> dungeon_get_valid_neighbor_rooms(D2, room_pos_create(col=0, row=0))
    []
    """
    current_col = current_room_pos[ROOM_POS_COL]
    current_row = current_room_pos[ROOM_POS_ROW]
    
    current_room = dungeon[current_row][current_col]
    valid_neighbors = []

    possible_deltas = [
        (0, -1, ROOM_CONNECTION_UP),
        (1, 0, ROOM_CONNECTION_RIGHT),
        (0, 1, ROOM_CONNECTION_DOWN),
        (-1, 0, ROOM_CONNECTION_LEFT)
    ]

    for d_col, d_row, conn_index in possible_deltas:
        new_col = current_col + d_col
        new_row = current_row + d_row
        new_pos = room_pos_create(new_col, new_row)
        
        # check dungeon limits
        if not dungeon_room_pos_in_bounds(dungeon, room_pos_create(col=new_col, row=new_row)):
            continue
            
        neighbor_room = dungeon[new_row][new_col]

        # check if rooms are adjacent and doors connected
        if dungeon_rooms_connected(current_room, current_room_pos, neighbor_room, new_pos):
            valid_neighbors.append(new_pos)
            
    return valid_neighbors

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
    (0, 0)
    >>> # Rotate room at (0, 0)
    >>> dungeon_rotate_room(d, 0, 0)
    True
    >>> # New state: rotation 1
    >>> d[0][0]
    (0, 1)
    >>> # Try to rotate out of bounds
    >>> dungeon_rotate_room(d, 5, 5)
    False
    """
    # check if room in bounds
    if not dungeon_room_pos_in_bounds(dungeon, room_pos_create(col=col, row=row)):
        return False

    room: RoomT = dungeon[row][col]
    dungeon[row][col] = dungeon_room_create(room[ROOM_BLOCK_ID], room[ROOM_ROTATION_COUNT] + 1)
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
