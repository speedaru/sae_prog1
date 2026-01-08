from typing import Any

import libs.fltk as fltk

# engine stuff
from src.engine.structs.entity import *
from src.engine.asset_manager import *

from src.game.entity_definitions import *

# utils
import src.utils.geom as geom
from src.utils.logging import *


# player path, basicly a chain of room positions
MovementPathT = list[RoomPosT]

# BaseEntityT -> EntityT -> AdventurerT
AdventurerT = list[RoomPosT | int | MovementPathT | Any]

# enum for adventurer structure that inherits from entity
T_ADVENTURER_PATH = T_ENTITY_COUNT
T_ADVENTURER_INVENTORY = T_ENTITY_COUNT + 1
T_ADVENTURER_COUNT = T_ENTITY_COUNT + 2

# inventory item descriptor struct
InventoryItemE = int
InventoryItemT = list[InventoryItemE | Any]
InventoryT = list[InventoryItemT]

# enum of every item an entity can have in its inventory
E_INVENTORY_ITEM_STRONG_SWORD = E_ENTITY_STRONG_SWORD

T_INVENTORY_ITEM_TYPE = 0 # the item type, like strong sword or wtv
T_INVENTORY_ITEM_DATA = 1 # the item struct itself
T_INVENTORY_ITEM_COUNT = 2


def movement_path_is_valid(movement_path: MovementPathT) -> bool:
    # is a list and has at least 1 room_pos in list
    return isinstance(movement_path, list) and len(movement_path) > 0

def inventory_item_create(item_type: InventoryItemE, item_data: Any) -> InventoryItemT:
    item: InventoryItemT = [None] * T_INVENTORY_ITEM_COUNT

    item[T_INVENTORY_ITEM_TYPE] = item_type
    item[T_INVENTORY_ITEM_DATA] = item_data

    return item

def adventurer_init(adventurer: AdventurerT, level: int = 1, room_pos: RoomPosT = (0, 0)):
    """
    Initializes the adventurer structure.
    
    Delegates the initialization to `entity_init` to set up the position and level.

    Args:
        adventurer (AdventurerT): The list representing the adventurer (modified in-place).
        level (int, optional): Starting level. Defaults to 1.
        room_pos (list[int], optional): Position [x, y] in the dungeon. Defaults to [0, 0].
    """
    entity_init(adventurer, level, room_pos, T_ADVENTURER_COUNT)

    # create invetory
    adventurer[T_ADVENTURER_INVENTORY] = InventoryT()
    log_debug_full(f"created adventurer inventory: {adventurer[T_ADVENTURER_INVENTORY]}")

def adventurer_render(adventurer: AdventurerT, assets: AssetsT):
    """
    Renders the adventurer on the screen.

    Retrieves the Knight image from the asset manager and draws it using `entity_render`.

    Args:
        adventurer (AdventurerT): The adventurer structure.
        assets (AssetsT): The loaded game assets.
    """
    knight_image = assets[T_ASSETS_CHARACTERS][CHARACTERS_ADVENTURER]

    entity_render(adventurer, knight_image)

def adventurer_render_path(adventurer: AdventurerT):
    PATH_LINE_COLOR = "red"
    PATH_LINE_THICKNESS = 2

    movement_path: MovementPathT = adventurer[T_ADVENTURER_PATH]
    if movement_path == None or len(movement_path) == 0:
        return

    # get center of adventurer pos to start drawing from there
    start_x, start_y = geom.get_room_center_screen_pos(adventurer[T_BASE_ENTITY_ROOM_POS])

    for room_pos in movement_path:
        end_x, end_y = geom.get_room_center_screen_pos(room_pos)
        fltk.ligne(start_x, start_y, end_x, end_y, couleur=PATH_LINE_COLOR, epaisseur=PATH_LINE_THICKNESS)
        start_x, start_y = end_x, end_y

def adventurer_inventory_add_item(adventurer: AdventurerT, item: InventoryItemT):
    inventory: list | NoneType = adventurer[T_ADVENTURER_INVENTORY]
    if inventory == None:
        log_error("[adventurer_inventory_add_item] player inventory is None")
        return

    inventory.append(item)
    log_debug_full(f"added item to inventory: {item[T_INVENTORY_ITEM_TYPE]}")

def adventurer_inventory_remove_item(adventurer: AdventurerT, item_type: InventoryItemE):
    """
    removes first occurence of specific item type in inventory
    """
    inventory: list | NoneType = adventurer[T_ADVENTURER_INVENTORY]
    if inventory == None:
        log_error("[adventurer_inventory_remove_item] player inventory is None")
        return

    # use range so we dont modify inventory while iterating over it directly
    for i in range(len(inventory)):
        item = inventory[i]
        if item[T_INVENTORY_ITEM_TYPE] == item_type:
            inventory.pop(i)
            log_debug_full(f"removed item from inventory: {item[T_INVENTORY_ITEM_TYPE]}")
            break

def adventurer_inventory_has_item(adventurer: AdventurerT, item_type: InventoryItemE) -> bool:
    inventory: list | NoneType = adventurer[T_ADVENTURER_INVENTORY]
    if inventory == None:
        log_error("[adventurer_inventory_has_item] player inventory is None")
        return False

    for item in inventory:
        if item[T_INVENTORY_ITEM_TYPE] == item_type:
            return True

    return False

def adventurer_inventory_item_type_to_str(item_type: InventoryItemE):
    if item_type == E_INVENTORY_ITEM_STRONG_SWORD:
        return "epee magique"

    return ""

def adventurer_inventory_get_item_counts(adventurer: AdventurerT) -> dict[str, int]:
    inventory: list | NoneType = adventurer[T_ADVENTURER_INVENTORY]
    if inventory == None:
        log_error("[inventory_get_item_counts] player inventory is None")
        return dict()

    dic = dict()
    for item in inventory:
        str_rep = adventurer_inventory_item_type_to_str(item[T_INVENTORY_ITEM_TYPE])
        if str_rep == "":
            continue

        if str_rep in dic:
            dic[str_rep] += 1
        else:
            dic[str_rep] = 1

    return dic
