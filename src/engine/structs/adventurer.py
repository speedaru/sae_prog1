import libs.fltk as fltk

# engine stuff
from src.engine.asset_manager import *
from src.engine.structs.entity import *
from src.engine.structs.inventory import *

# utils
import src.utils.geom as geom
from src.utils.logging import *


# player path, basicly a chain of room positions
MovementPathT = list[RoomPosT]

# BaseEntityT -> EntityT -> AdventurerT
AdventurerT = list[RoomPosT | int | MovementPathT | InventoryT]

# enum for adventurer structure that inherits from entity
T_ADVENTURER_PATH = T_ENTITY_COUNT
T_ADVENTURER_INVENTORY = T_ENTITY_COUNT + 1
T_ADVENTURER_COUNT = T_ENTITY_COUNT + 2


def movement_path_is_valid(movement_path: MovementPathT) -> bool:
    # is a list and has at least 1 room_pos in list
    return isinstance(movement_path, list) and len(movement_path) > 0

# def adventurer_init(adventurer: AdventurerT, level: int = 1, room_pos: RoomPosT = (0, 0)):
#     """
#     Initializes the adventurer structure.
#     
#     Delegates the initialization to `entity_init` to set up the position and level.
#
#     Args:
#         adventurer (AdventurerT): The list representing the adventurer (modified in-place).
#         level (int, optional): Starting level. Defaults to 1.
#         room_pos (list[int], optional): Position [x, y] in the dungeon. Defaults to [0, 0].
#     """
#     entity_init(adventurer, level, room_pos, T_ADVENTURER_COUNT)
#
#     # create invetory
#     adventurer[T_ADVENTURER_INVENTORY] = InventoryT()
#     log_debug_full(f"created adventurer inventory: {adventurer[T_ADVENTURER_INVENTORY]}")

def adventurer_create(room_pos: RoomPosT = room_pos_create(0, 0), level: int = 1) -> AdventurerT:
    adventurer: list = \
        entity_create(entity_type=E_ENTITY_ADVENTURER, room_pos=room_pos, level=level, entity_size=T_ADVENTURER_COUNT)

    # create inventory
    adventurer[T_ADVENTURER_INVENTORY] = InventoryT()
    log_debug_full(f"created adventurer inventory: {adventurer[T_ADVENTURER_INVENTORY]}")

    return adventurer

def adventurer_render(dungeon, adventurer: AdventurerT, assets: AssetsT):
    """
    Renders the adventurer on the screen.

    Retrieves the Knight image from the asset manager and draws it using `entity_render`.

    Args:
        adventurer (AdventurerT): The adventurer structure.
        assets (AssetsT): The loaded game assets.
    """
    knight_image = assets[T_ASSETS_CHARACTERS][CHARACTERS_ADVENTURER]

    entity_render(dungeon, adventurer, knight_image)

def adventurer_render_path(dungeon, adventurer: AdventurerT):
    PATH_LINE_COLOR = "red"
    PATH_LINE_THICKNESS = 2

    movement_path: MovementPathT = adventurer[T_ADVENTURER_PATH]
    if movement_path == None or len(movement_path) == 0:
        return

    # start at adventurer posititon, then it becomes previous one
    adventurer_pos = adventurer[T_BASE_ENTITY_ROOM_POS]
    # start_x, start_y = geom.get_room_sreen_pos_center(dungeon_get_room_screen_coords(dungeon, adventurer_pos))
    start_x, start_y = dungeon_get_room_screen_coords_center(dungeon, adventurer_pos)

    for room_pos in movement_path:
        end_x, end_y = dungeon_get_room_screen_coords_center(dungeon, room_pos)

        fltk.ligne(start_x, start_y, end_x, end_y, couleur=PATH_LINE_COLOR, epaisseur=PATH_LINE_THICKNESS)

        # set next room start to current room end
        start_x, start_y = end_x, end_y

