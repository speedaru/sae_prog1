
from src.engine.structs.entity import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *
from src.engine.structs.dungeon import *



 #Anis
def find_closest_dragon(adventurer: AdventurerT, dragons: list[DragonT]) -> DragonT | None:
    """
    Trouve le dragon le plus proche.
    En cas d'égalité de distance, choisit le niveau le plus élevé.
    """
    if not dragons:
        return None
        
    adv_pos = adventurer[ENTITY_ROOM_POS]
    
    # Initialisation avec le premier dragon
    closest_dragon = dragons[0]
    min_dist = dungeon_get_room_distance(adv_pos, closest_dragon[ENTITY_ROOM_POS])
    
    # Parcours des autres dragons avec une boucle for simple 
    for i in range(1, len(dragons)):
        dragon = dragons[i]
        dist = dungeon_get_room_distance(adv_pos, dragon[ENTITY_ROOM_POS])
        
        # Si on trouve un dragon plus proche
        if dist < min_dist:
            min_dist = dist
            closest_dragon = dragon
        # Si distance égale, on privilégie le niveau le plus haut
        elif dist == min_dist:
            if dragon[ENTITY_LEVEL] > closest_dragon[ENTITY_LEVEL]:
                closest_dragon = dragon
                
    return closest_dragon

def find_path(dungeon: DungeonT, start_room: RoomPosT, target_room: RoomPosT) -> MovementPathT:
    
    #Calcule le chemin le plus court via un parcours en largeur 
    
    if start_room == target_room:
        return []
    queue = [(start_room, [])]
    
    # Ensemble des cases visitées pour ne pas tourner en rond
    visited = {start_room}

    while len(queue) > 0:
        current_pos, path = queue.pop(0)
    
        # Si arrivé
        if current_pos == target_room:
            return path
        
        # Exploration endroit valides 
        valid_neighbors = dungeon_get_valid_neighbor_rooms(dungeon, current_pos)
        for neighbor in valid_neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                # On ajoute le voisin et le nouveau chemin à la file
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))
                
    return []

def is_valid_path(dungeon: DungeonT, start_pos: RoomPosT, path: MovementPathT) -> bool:
    #Vérifie si le chemin est valide pas à pas.
    current = start_pos
    for step in path:
        if step not in dungeon_get_valid_neighbor_rooms(dungeon, current):
            return False
        current = step
    return True

def find_and_set_adventurer_path(dungeon: DungeonT, adventurer: AdventurerT, dragons: list[DragonT]):
    #Trouve le dragon cible et calcule le chemin vers lui.
    target_dragon = find_closest_dragon(adventurer, dragons)
    
    # Si une cible est trouvée, on calcule le chemin
    if target_dragon is not None:
        path = find_path(dungeon, adventurer[ENTITY_ROOM_POS], target_dragon[ENTITY_ROOM_POS])
        if path:
            adventurer[ADVENTURER_PATH] = path

def do_adventurer_path(adventurer: AdventurerT):
    #déplacement de l'aventurier.
    movement_path = adventurer[ADVENTURER_PATH]
    if isinstance(movement_path, list) and len(movement_path) > 0:
        adventurer[ENTITY_ROOM_POS] = movement_path[-1]