import libs.fltk as fltk

# engine stuff
from src.engine.structs.entity import *
from src.engine.asset_manager import *

# utils
import src.utils.geom as geom
from src.utils.logging import *


# types
MovementPathT = list[RoomPosT]
AdventurerT = list[RoomPosT | int | MovementPathT]

# enum for adventurer structure that inherits from entity
ADVENTURER_PATH = 2
ADVENTURER_COUNT = ENTITY_COUNT + 1


def adventurer_init(adventurer: AdventurerT, level: int = 1, room_pos: RoomPosT = (0, 0)):
    """
    Initializes the adventurer structure.
    
    Delegates the initialization to `entity_init` to set up the position and level.

    Args:
        adventurer (AdventurerT): The list representing the adventurer (modified in-place).
        level (int, optional): Starting level. Defaults to 1.
        room_pos (list[int], optional): Position [x, y] in the dungeon. Defaults to [0, 0].

    Doctest : 
    >>> adv = []
    >>> # Initialize adventurer
    >>> adventurer_init(adv, level=10, room_pos=[5, 3])
    >>> # Verify position (index 0)
    >>> adv[ADVENTURER_ROOM_POS]
    (5, 3)
    >>> # Verify level (index 1)
    >>> adv[ADVENTURER_LEVEL]
    10
    >>> # Check default initialization
    >>> adv_default = []
    >>> adventurer_init(adv_default)
    >>> adv_default
    [(0, 0), 1]
    """
    entity_init(adventurer, level, room_pos, ADVENTURER_COUNT)

def adventurer_render(adventurer: AdventurerT, assets: AssetsT):
    """
    Renders the adventurer on the screen.

    Retrieves the Knight image from the asset manager and draws it using `entity_render`.

    Args:
        adventurer (AdventurerT): The adventurer structure.
        assets (AssetsT): The loaded game assets.
    """
    knight_image = assets[ASSETS_CHARACTERS][CHARACTERS_ADVENTURER]

    entity_render(adventurer, knight_image)

def adventurer_render_path(adventurer: AdventurerT):
    PATH_LINE_COLOR = "red"
    PATH_LINE_THICKNESS = 2

    movement_path: MovementPathT = adventurer[ADVENTURER_PATH]
    if movement_path == None or len(movement_path) == 0:
        return

    # get center of adventurer pos to start drawing from there
    start_x, start_y = geom.get_room_center_screen_pos(adventurer[ENTITY_ROOM_POS])

    for room_pos in movement_path:
        end_x, end_y = geom.get_room_center_screen_pos(room_pos)
        fltk.ligne(start_x, start_y, end_x, end_y, couleur=PATH_LINE_COLOR, epaisseur=PATH_LINE_THICKNESS)
        start_x, start_y = end_x, end_y

