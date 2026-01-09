from typing import Any

from src.game.entity_definitions import *

from src.utils.logging import *


# inventory item descriptor struct
InventoryItemE = int
InventoryItemT = list[InventoryItemE | Any]
InventoryT = list[InventoryItemT]

# enum of every item an entity can have in its inventory
E_INVENTORY_ITEM_STRONG_SWORD = E_ENTITY_STRONG_SWORD

T_INVENTORY_ITEM_TYPE = 0 # the item type, like strong sword or wtv
T_INVENTORY_ITEM_DATA = 1 # the item struct itself
T_INVENTORY_ITEM_COUNT = 2


def inventory_item_create(item_type: InventoryItemE, item_data: Any) -> InventoryItemT:
    item: InventoryItemT = [None] * T_INVENTORY_ITEM_COUNT

    item[T_INVENTORY_ITEM_TYPE] = item_type
    item[T_INVENTORY_ITEM_DATA] = item_data

    return item

def inventory_add_item(inventory: InventoryT, item: InventoryItemT):
    inventory.append(item)
    log_debug_full(f"added item to inventory: {item[T_INVENTORY_ITEM_TYPE]}")

def inventory_remove_item(inventory: InventoryT, item_type: InventoryItemE):
    """
    removes first occurence of specific item type in inventory
    """
    # use range so we dont modify inventory while iterating over it directly
    for i in range(len(inventory)):
        item = inventory[i]
        if item[T_INVENTORY_ITEM_TYPE] == item_type:
            inventory.pop(i)
            log_debug_full(f"removed item from inventory: {item[T_INVENTORY_ITEM_TYPE]}")
            break

def inventory_has_item(inventory: InventoryT, item_type: InventoryItemE) -> bool:
    for item in inventory:
        if item[T_INVENTORY_ITEM_TYPE] == item_type:
            return True

    return False

# TO REFACTOR BCS UGLY
def inventory_item_type_to_str(item_type: InventoryItemE):
    if item_type == E_INVENTORY_ITEM_STRONG_SWORD:
        return "epee magique"

    return ""

# TO REFACTOR BCS UGLY
def inventory_get_item_counts(inventory: InventoryT) -> dict[str, int]:
    """
    returns: dict of inventory items (string representation) and the amount we have
    """
    dic = dict()
    for item in inventory:
        str_rep = inventory_item_type_to_str(item[T_INVENTORY_ITEM_TYPE])
        if str_rep == "":
            continue

        if str_rep in dic:
            dic[str_rep] += 1
        else:
            dic[str_rep] = 1

    return dic
