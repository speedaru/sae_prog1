from random import randrange

# engine stuff
from src.engine.structs.dungeon import *
from src.engine.asset_manager import *
from src.engine.structs.entity import *

# utils
import src.utils.fltk_extensions as fltk_ext
from src.utils.logging import *


# types
DragonT = list[RoomPosT | int]

# enum for dragon structure that inherits from entity
DRAGON_COUNT = ENTITY_COUNT


def dragon_init(dragon: DragonT, level: int = 1, room_pos: list[int] = [0, 0]):
    """
    Initializes a dragon structure with a specific level and position.

    Args:
        dragon (DragonT): The list representing the dragon (modified in place).
        level (int, optional): The level of the dragon. Defaults to 1.
        room_pos (list[int], optional): The [x, y] position in the dungeon. Defaults to [0, 0].

    Doctest:

    >>> d = []
    >>> # Standard initialization
    >>> dragon_init(d, level=5, room_pos=[1, 1])
    >>> d
    [[1, 1], 5]
    
    >>> # Verifying indices using constants
    >>> d[DRAGON_LEVEL]
    5
    """
    # room_pos = [randrange(0, 6), randrange(0, 6)]
    entity_init(dragon, level, room_pos, DRAGON_COUNT)

def dragon_render(dragon: DragonT, assets: AssetsT):
    """
    Renders the dragon on the screen.
    
    Retrieves the dragon image from the asset manager and uses `entity_render`
    to draw it at the correct position relative to the room.
    """
    dragon_image = assets[ASSETS_CHARACTERS][CHARACTERS_DRAGONS]

    entity_render(dragon, dragon_image)

# if no count set it will automatically calculate number of dragons
def dragon_create_dragons(dragons: list[DragonT], dungeon_size: tuple[int, int], count: int | NoneType = None):
    """
    Generates and appends multiple dragons to the list, with random positions.
    
    If `count` is not specified, the number of dragons is calculated automatically
    based on the dungeon size (using a 1/12 ratio).

    Args:
        dragons (list[DragonT]): The main list of dragons in the game.
        dungeon_size (tuple[int, int]): The dimensions of the dungeon (width, height).
        count (int | NoneType, optional): A fixed number of dragons to create.
    
    Doctest :    

    >>> # Initialize an empty list
    >>> dragons_list = []
    >>> # Create 5 dragons for a 10x10 dungeon
    >>> dragon_create_dragons(dragons_list, (10, 10), count=5)
    >>> # Verify that exactly 5 dragons were added
    >>> len(dragons_list)
    5
    """
    DRAGON_TO_ROOM_RATIO = 1 / 12

    if count == None:
        area = dungeon_size[0] * dungeon_size[1]
        count = round(DRAGON_TO_ROOM_RATIO * area)
        count = max(count, 1) # at least 1 dragon

    assert(not isinstance(count, NoneType)) # count not none
    assert(count > 0) # at least 1 dragon

    for _ in range(count):
        d = DragonT()
        random_room = [randrange(0, dungeon_size[0]), randrange(0, dungeon_size[1])]
        log_debug_full(f"random room ({dungeon_size[0], dungeon_size[1]}): {random_room}")
        dragon_init(d, room_pos=random_room)
        dragons.append(d)
