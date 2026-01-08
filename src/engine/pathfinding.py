from src.engine.structs.entity import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *
from src.engine.structs.dungeon import *
from src.engine.structs.treasure import *

from src.game.game_definitions import *

from src.utils.entity_utils import *


# def find_closest_dragon(adventurer: AdventurerT, dragons: list[DragonT]) -> DragonT | None:
#     """
#     Finds the closest dragon.
#     In case of distance tie, chooses the highest level.
#     """
#     if not dragons:
#         return None
#         
#     adv_pos = adventurer[T_BASE_ENTITY_ROOM_POS]
#     
#     # Initialization with the first dragon
#     closest_dragon = dragons[0]
#     min_dist = dungeon_get_room_distance(adv_pos, closest_dragon[T_BASE_ENTITY_ROOM_POS])
#     
#     # Iterate through other dragons with a simple for loop 
#     for i in range(1, len(dragons)):
#         dragon = dragons[i]
#         dist = dungeon_get_room_distance(adv_pos, dragon[T_BASE_ENTITY_ROOM_POS])
#         
#         # If a closer dragon is found
#         if dist < min_dist:
#             min_dist = dist
#             closest_dragon = dragon
#         # If distance is equal, prioritize the highest level
#         elif dist == min_dist:
#             if dragon[T_ENTITY_LEVEL] > closest_dragon[ENTITY_LEVEL]:
#                 closest_dragon = dragon
#                 
#     return closest_dragon

def find_path(dungeon: DungeonT, start_room: RoomPosT, target_room: RoomPosT) -> MovementPathT:
    """
    Calculates the shortest path via Breadth-First Search (BFS)
    """
    if start_room == target_room:
        return []

    queue = [(start_room, [])]
    
    # Set of visited rooms to avoid going in circles
    visited = {start_room}

    while len(queue) > 0:
        current_pos, path = queue.pop(0)
    
        # If arrived
        if current_pos == target_room:
            return path
        
        # Exploration of valid locations 
        valid_neighbors = dungeon_get_valid_neighbor_rooms(dungeon, current_pos)
        for neighbor in valid_neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                # Add the neighbor and the new path to the queue
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))
                
    return []

def is_valid_path(dungeon: DungeonT, start_pos: RoomPosT, path: MovementPathT) -> bool:
    # Checks if the path is valid step by step.
    current = start_pos
    for step in path:
        if step not in dungeon_get_valid_neighbor_rooms(dungeon, current):
            return False
        current = step
    return True

def room_is_accessible(dungeon: DungeonT, adventurer: AdventurerT, target_room: RoomPosT):
    path = find_path(dungeon, adventurer[T_BASE_ENTITY_ROOM_POS], target_room)
    return len(path) != 0

def find_meanest_dragon(dungeon: DungeonT, adventurer: AdventurerT, dragons: list[DragonT]) -> DragonT:
    """
    returns: DragonT dragon with the highest level
    """
    meanest_dragon = dragons[0] 

    for dragon in dragons : 
        # skip unacessible dragons
        if not room_is_accessible(dungeon, adventurer, dragon[T_BASE_ENTITY_ROOM_POS]): 
            continue

        if meanest_dragon[T_ENTITY_LEVEL] < dragon[T_ENTITY_LEVEL] :
            meanest_dragon = dragon 
            
    return meanest_dragon

def path_stop_at_collision(entities: EntitiesT, path: MovementPathT) -> MovementPathT:
    """
    returns: path stopped after first collisions with entity
    """
    entities_positions: set = get_collision_entities_positions(entities)

    new_path = []
    for room_pos in path:
        new_path.append(room_pos)

        # if entity somewhere on path, then stop path there
        if room_pos in entities_positions:
            return new_path

    return new_path

def find_and_set_adventurer_path(game_data: GameDataT):
    dungeon = game_data[T_GAME_DATA_DUNGEON]
    adventurer = game_data[T_GAME_DATA_ENTITIES][T_ENTITIES_ADVENTURER]
    dragons = game_data[T_GAME_DATA_ENTITIES][T_ENTITIES_DRAGONS]
    treasure = game_data[T_GAME_DATA_ENTITIES][T_ENTITIES_TREASURE]

    target_room = None

    # if treasure is in dungeon and accesible, then go to treasure
    if treasure_is_valid(treasure) and room_is_accessible(dungeon, adventurer, treasure[T_BASE_ENTITY_ROOM_POS]):
        target_room = treasure[T_BASE_ENTITY_ROOM_POS]
    # otherwise go to dragon
    else : 
        target_dragon = find_meanest_dragon(dungeon, adventurer, dragons)
        target_room = target_dragon[T_BASE_ENTITY_ROOM_POS]    
        
    # If a target is found, calculate the path
    if target_room != None:
        path = find_path(dungeon, adventurer[T_BASE_ENTITY_ROOM_POS], target_room)

        # if another entity on path, stop path there
        path = path_stop_at_collision(game_data[T_GAME_DATA_ENTITIES], path)

        # set new calculated path in adventurer
        if path:
            adventurer[T_ADVENTURER_PATH] = path
            return 

    # if dragon not found, or path not found, empty path
    adventurer[T_ADVENTURER_PATH] = MovementPathT()

def pickup_items(items: list[EntityItemT], adventurer: AdventurerT, room_pos: RoomPosT):
    """
    if any items is in room_poos then it will pick it up and place it in inventory
    """
    picked_up_item_idxs: list[int] = list()

    for i in range(len(items)):
        item: list = items[i]
        if item[T_ENTITY_ITEM_DATA][T_BASE_ENTITY_ROOM_POS] == room_pos:
            log_debug_full(f"found item in current room: {room_pos}")
            
            # no data for now, we just know that we have that item, no item specific info
            inventory_item = inventory_item_create(item[T_ENTITY_ITEM_TYPE], None)

            # add item to inventory
            adventurer_inventory_add_item(adventurer, inventory_item)

            # remove it from items
            picked_up_item_idxs.append(i)

    # remove picked up items from items list
    for i in picked_up_item_idxs:
        items.pop(i)

def do_adventurer_path(adventurer: AdventurerT, entities: EntitiesT):
    # Adventurer movement.
    movement_path: list = adventurer[T_ADVENTURER_PATH]
    if not movement_path_is_valid(movement_path):
        return

    for current_room_pos in movement_path:
        # pick up items if there are any in current room
        pickup_items(entities[T_ENTITIES_ITEMS], adventurer, current_room_pos)

        adventurer[T_BASE_ENTITY_ROOM_POS] = current_room_pos
