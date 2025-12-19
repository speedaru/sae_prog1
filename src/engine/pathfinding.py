from src.engine.structs.entity import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *
from src.engine.structs.dungeon import *


# def find_closest_dragon(adventurer: AdventurerT, dragons: list[DragonT]) -> DragonT | None:
#     """
#     Finds the closest dragon.
#     In case of distance tie, chooses the highest level.
#     """
#     if not dragons:
#         return None
#         
#     adv_pos = adventurer[ENTITY_ROOM_POS]
#     
#     # Initialization with the first dragon
#     closest_dragon = dragons[0]
#     min_dist = dungeon_get_room_distance(adv_pos, closest_dragon[ENTITY_ROOM_POS])
#     
#     # Iterate through other dragons with a simple for loop 
#     for i in range(1, len(dragons)):
#         dragon = dragons[i]
#         dist = dungeon_get_room_distance(adv_pos, dragon[ENTITY_ROOM_POS])
#         
#         # If a closer dragon is found
#         if dist < min_dist:
#             min_dist = dist
#             closest_dragon = dragon
#         # If distance is equal, prioritize the highest level
#         elif dist == min_dist:
#             if dragon[ENTITY_LEVEL] > closest_dragon[ENTITY_LEVEL]:
#                 closest_dragon = dragon
#                 
#     return closest_dragon

def find_meanest_dragon(dragons: list[DragonT]) -> DragonT:
    """
    returns: DragonT dragon with the highest level
    """
    return dragons[0]

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

def find_and_set_adventurer_path(dungeon: DungeonT, adventurer: AdventurerT, dragons: list[DragonT]):
    # Finds the target dragon and calculates the path to it.
    # target_dragon = find_closest_dragon(adventurer, dragons)
    target_dragon = find_meanest_dragon(dragons)
    
    # If a target is found, calculate the path
    if target_dragon != None:
        path = find_path(dungeon, adventurer[ENTITY_ROOM_POS], target_dragon[ENTITY_ROOM_POS])
        if path:
            adventurer[ADVENTURER_PATH] = path
            return

    # if dragon not found, or path not found, empty path
    adventurer[ADVENTURER_PATH] = MovementPathT()

def do_adventurer_path(adventurer: AdventurerT):
    # Adventurer movement.
    movement_path = adventurer[ADVENTURER_PATH]
    if isinstance(movement_path, list) and len(movement_path) > 0:
        adventurer[ENTITY_ROOM_POS] = movement_path[-1]
