# engine stuff
from src.engine.asset_manager import *
from src.engine.structs.entity import *

# utils
from src.utils.logging import *


# types
AdventurerT = list[list[int] | int | list[tuple[int, int]]]

# enum for adventurer structure
ADVENTURER_ROOM_POS = 0
ADVENTURER_LEVEL = 1
ADVENTURER_PATH = 2
ADVENTURER_COUNT = 3


def adventurer_init(adventurer: AdventurerT, level: int = 1, room_pos: list[int] = [0, 0]):
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
    [5, 3]
    >>> # Verify level (index 1)
    >>> adv[ADVENTURER_LEVEL]
    10
    >>> # Check default initialization
    >>> adv_default = []
    >>> adventurer_init(adv_default)
    >>> adv_default
    [[0, 0], 1]
    """
    entity_init(adventurer, level, room_pos)

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
