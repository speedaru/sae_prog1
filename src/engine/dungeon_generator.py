from dataclasses import dataclass
from random import choice

import src.engine.pathfinding as pathfinding
from src.engine.structs.dungeon import *
from src.engine.entity_system import *

from src.game.game_definitions import *

import src.utils.entity_utils as entity_utils


class SettingT:
    def __init__(self, label, val, minVal, maxVal):
        self.label: str = label
        self.val = val
        self.min = minVal
        self.max = maxVal

@dataclass
class DungeonSettingsT:
    dungeon_size: SettingT
    dragon_count: SettingT
    treasure_count: SettingT
    strong_sword_count: SettingT
    chaos_seal_count: SettingT

def _random_room_pos(max_room_idx: int, entity_system) -> RoomPosT:
    used_rooms = entity_utils.get_all_entity_positions(entity_system)
    
    random_row: int = choice([row for row in range(max_room_idx)])

    # pick a random col so that the random is not in used rooms
    random_col: int = choice([col for col in range(max_room_idx) if not room_pos_create(col=col, row=random_row) in used_rooms])

    return room_pos_create(col=random_col, row=random_row)

def _generate_adventurer(dungeon_data, settings: DungeonSettingsT):
    es = dungeon_data[T_DUNGEON_DATA_ENTITY_SYSTEM]

    random_room = _random_room_pos(settings.dungeon_size.val.width - 1, es)

    entity_system_add_entity(es, adventurer_create(random_room))

def _generate_dragons(dungeon_data, settings: DungeonSettingsT):
    es = dungeon_data[T_DUNGEON_DATA_ENTITY_SYSTEM]

    max_room_idx = settings.dungeon_size.val.width - 1

    # generate dragons from level 1 -> dragon_count
    for i in range(settings.dragon_count.val):
        random_room = _random_room_pos(max_room_idx, es)
        entity_system_add_entity(es, dragon_create(random_room, i + 1))

def _mark_required_doors(pos_a, pos_b, requirements):
    if pos_a not in requirements: requirements[pos_a] = set()
    if pos_b not in requirements: requirements[pos_b] = set()
    
    dx = pos_b[0] - pos_a[0]
    dy = pos_b[1] - pos_a[1]
    
    if dy == -1: # B is UP from A
        requirements[pos_a].add(ROOM_CONNECTION_UP)
        requirements[pos_b].add(ROOM_CONNECTION_DOWN)
    elif dx == 1: # B is RIGHT from A
        requirements[pos_a].add(ROOM_CONNECTION_RIGHT)
        requirements[pos_b].add(ROOM_CONNECTION_LEFT)
    elif dy == 1: # B is DOWN from A
        requirements[pos_a].add(ROOM_CONNECTION_DOWN)
        requirements[pos_b].add(ROOM_CONNECTION_UP)
    elif dx == -1: # B is LEFT from A
        requirements[pos_a].add(ROOM_CONNECTION_LEFT)
        requirements[pos_b].add(ROOM_CONNECTION_RIGHT)

def _get_neighbor_constraints(dungeon, r, c) -> set[int]:
    constraints = set()
    
    # Check room ABOVE (North)
    if r > 0:
        north_room = dungeon[r-1][c]
        north_connections = dungeon_room_get_connections(north_room)
        if north_connections[ROOM_CONNECTION_DOWN]: # If he has a door down
            constraints.add(ROOM_CONNECTION_UP)     # We should have a door up
            
    # Check room to the LEFT (West)
    if c > 0:
        west_room = dungeon[r][c-1]
        west_connections = dungeon_room_get_connections(west_room)
        if west_connections[ROOM_CONNECTION_RIGHT]: # If he has a door right
            constraints.add(ROOM_CONNECTION_LEFT)    # We should have a door left
            
    return constraints

def _generate_dungeon_layout(dungeon_data, settings: DungeonSettingsT):
    es = dungeon_data[T_DUNGEON_DATA_ENTITY_SYSTEM]

    dungeon = dungeon_data[T_DUNGEON_DATA_DUNGEON]
    adventurer = entity_system_get_first_and_only(es, E_ENTITY_ADVENTURER)
    dragons = entity_system_get_all(es, E_ENTITY_DRAGON)

    # create ghost dungeon where all rooms are open
    # for pathfinding to find any possible route
    width = dungeon_get_width(dungeon)
    height = dungeon_get_height(dungeon)
    ghost_dungeon = []
    dungeon_init(ghost_dungeon, height, width)
    for r in range(height):
        for c in range(width):
            ghost_dungeon[r][c] = dungeon_room_create(BLOCK_QUAD, 0)

    # track which doors are needed for each room
    # dictionary: (col, row) -> set of required directions (UP, RIGHT, DOWN, LEFT)
    required_connections = {}

    for dragon in dragons:
        path = pathfinding.find_random_path_to_dragon(ghost_dungeon, adventurer, dragon)
        
        # Add the start position to the path logic
        full_path = [adventurer[T_BASE_ENTITY_ROOM_POS]] + path

        # determine doors needed to travel this path
        for i in range(len(full_path) - 1):
            curr = full_path[i]
            nxt = full_path[i + 1]
            
            # Determine direction from curr to nxt
            # This fills the 'required_connections' for both rooms
            _mark_required_doors(curr, nxt, required_connections)

    # We iterate and pick rooms that match neighbors
    for r in range(height):
        for c in range(width):
            room_pos = room_pos_create(row=r, col=c)
            must_have = required_connections.get(room_pos, set())
            
            # Neighbor connection matching (Natural Flow)
            if r > 0:
                n_conn = dungeon_room_get_connections(dungeon[r-1][c])
                if n_conn[ROOM_CONNECTION_DOWN]: must_have.add(ROOM_CONNECTION_UP)
            if c > 0:
                w_conn = dungeon_room_get_connections(dungeon[r][c-1])
                if w_conn[ROOM_CONNECTION_RIGHT]: must_have.add(ROOM_CONNECTION_LEFT)
            
            # Apply your playability rules
            dungeon[r][c] = dungeon_pick_refined_room(dungeon, r, c, must_have)

def _generate_items(dungeon_data, settings: DungeonSettingsT):
    es = dungeon_data[T_DUNGEON_DATA_ENTITY_SYSTEM]

    entity_create_callback_table = [
            (settings.strong_sword_count.val, strong_sword_create),
            (settings.chaos_seal_count.val, chaos_seal_create),
    ]

    max_room_idx = settings.dungeon_size.val.width - 1
    for count, creation_callback in entity_create_callback_table:
        for i in range(count):
            room_pos = _random_room_pos(max_room_idx, es)
            entity_system_add_entity(es, creation_callback(room_pos))

def generate_dungeon_data(settings: DungeonSettingsT):
    dungeon_data = dungeon_data_init()

    dungeon: DungeonT = dungeon_data[T_DUNGEON_DATA_DUNGEON]
    dungeon_init(dungeon, settings.dungeon_size.val.width, settings.dungeon_size.val.height)

    _generate_adventurer(dungeon_data, settings)
    _generate_dragons(dungeon_data, settings)
    _generate_dungeon_layout(dungeon_data, settings)
    _generate_items(dungeon_data, settings)

    dungeon_data[T_DUNGEON_DATA_TREASURE_COUNT] = settings.treasure_count.val

    return dungeon_data
