from copy import deepcopy
from random import randrange

import src.engine.pathfinding as pathfinding
from src.engine.structs.dungeon import *
from src.engine.structs.entity import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *
from src.engine.structs.treasure import *
from src.engine.event_info import *
from src.engine.parsing import *
from src.engine.structs.entity import *

from src.game.game_definitions import *
from src.game.state_manager import *


def load_game_data(game_context, game_data: GameDataT):
    game_context[GAME_CONTEXT_GAME_DATA][:] = deepcopy(game_data)

    # save original game data also
    game_context[GAME_CONTEXT_ORIGINAL_GAME_DATA][:] = deepcopy(game_data)

def reset_game_data(game_context):
    # reset to originals by copying orignals, copy inplace
    game_context[GAME_CONTEXT_GAME_DATA][:] = deepcopy(game_context[GAME_CONTEXT_ORIGINAL_GAME_DATA])

def _get_clicked_room(event_info: EventInfoT, dungeon: DungeonT) -> RoomPosT | NoneType:
    ev: FltkEvent = event_info[EVENT_INFO_EV]
    click_postion = fltk_ext.position_souris(ev)

    # rotate room at click positons
    clicked_room_col = click_postion[0] // BLOCK_SCALED_SIZE[0] # x
    clicked_room_row = click_postion[1] // BLOCK_SCALED_SIZE[1] # y
    clicked_room: RoomPosT = room_pos_create(col=clicked_room_col, row=clicked_room_row)

    # if cursor outside of dungeon do nothing
    if not dungeon_room_pos_in_bounds(dungeon, clicked_room):
        return None

    return clicked_room

def _get_entities_positions(entities: EntitiesT):
    entities_positions = [dragon[ENTITY_ROOM_POS] for dragon in entities[ENTITIES_DRAGONS]]
    entities_positions.append(entities[ENTITIES_ADVENTURER][ENTITY_ROOM_POS]) # adventurer

    treasure = entities[ENTITIES_TREASURE]
    if treasure_is_valid(treasure):
        entities_positions.append(treasure[TREASURE_ROOM_POS]) # treasure

    return entities_positions

def rotate_room(event_info: EventInfoT, game_context: GameContextT):
    dungeon: DungeonT = game_context[GAME_CONTEXT_GAME_DATA][GAME_DATA_DUNGEON]

    clicked_room: RoomPosT | NoneType = _get_clicked_room(event_info, dungeon)
    if clicked_room != None:
        dungeon_rotate_room(dungeon, row=clicked_room[ROOM_POS_ROW], col=clicked_room[ROOM_POS_COL])

def place_treasure(event_info: EventInfoT, dungeon: DungeonT, entities: EntitiesT) -> bool:
    """
    room_pos: room position in which to place the treasure
    """
    # check if there is already a treasure on the map
    existing_treasure = entities[ENTITIES_TREASURE]
    if existing_treasure != None and len(existing_treasure) == TREASURE_COUNT:
        log_error(f"cant place treasure, a treasure is already in the dungeon: {existing_treasure}")
        return False

    # get clicked room pos
    room_pos: RoomPosT | NoneType = _get_clicked_room(event_info, dungeon)
    if room_pos == None:
        log_error("failed to place treasure, invalid room clicked")
        return False

    # check if there is already an entity in that room
    entities_positions = _get_entities_positions(entities)
    if room_pos in entities_positions:
        log_error("can't place treasure, there is already an entity in that room")
        return False

    random_image_id = randrange(TREASURES_IMAGE_COUNT)
    treasure: TreasureT = treasure_create(room_pos=room_pos, image_id=random_image_id)

    entities[ENTITIES_TREASURE] = treasure
    return True

def manually_update_player_path(event_info: EventInfoT, game_context: GameContextT):
    ev: FltkEvent = event_info[EVENT_INFO_EV]
    click_postion = fltk_ext.position_souris(ev)

    # get room at click positons
    clicked_room_row: int = click_postion[1] // BLOCK_SCALED_SIZE[1]
    clicked_room_col: int = click_postion[0] // BLOCK_SCALED_SIZE[0]
    clicked_room_pos: RoomPosT = (clicked_room_col, clicked_room_row)

    # if cursor outside of dungeon do nothing
    dungeon: DungeonT = game_context[GAME_CONTEXT_GAME_DATA][GAME_DATA_DUNGEON]
    if clicked_room_row >= dungeon_get_width(dungeon) or clicked_room_col >= dungeon_get_height(dungeon):
        return

    adventurer: AdventurerT = game_context[GAME_CONTEXT_GAME_DATA][GAME_DATA_ENTITIES][ENTITIES_ADVENTURER]

    # init adventurer path if its None
    if adventurer[ADVENTURER_PATH] == None:
        adventurer[ADVENTURER_PATH] = MovementPathT()

    # ensure previous room adjacent and connected to clicked pos
    dungeon: DungeonT = game_context[GAME_CONTEXT_GAME_DATA][GAME_DATA_DUNGEON]
    movement_path: MovementPathT = adventurer[ADVENTURER_PATH]
    previous_clicked_room_pos: RoomPosT = adventurer[ENTITY_ROOM_POS] # set last click room to player pos if 0 clicks
    if len(movement_path) > 0: # if not first click then set previous click room to last click pos
        # get previous clicked room positon
        previous_clicked_room_pos = movement_path[-1]

    # get room representations from dungeon: [BLOCK_ID, ROTATION_COUNT]
    clicked_room: RoomT = dungeon[clicked_room_pos[1]][clicked_room_pos[0]]
    previous_clicked_room: RoomT = dungeon[previous_clicked_room_pos[1]][previous_clicked_room_pos[0]] # room block repr

    # if clicked room not adjacent to previously clicked room then dont add it to path
    if not dungeon_rooms_connected(clicked_room, clicked_room_pos, previous_clicked_room, previous_clicked_room_pos):
        return

    # clicked room is valid, add it to path
    movement_path.append(clicked_room_pos)

def auto_update_player_path(game_context: GameContextT):
    # update path
    dungeon: DungeonT = game_context[GAME_CONTEXT_GAME_DATA][GAME_DATA_DUNGEON]
    adventurer = game_context[GAME_CONTEXT_GAME_DATA][GAME_DATA_ENTITIES][ENTITIES_ADVENTURER]
    dragons = game_context[GAME_CONTEXT_GAME_DATA][GAME_DATA_ENTITIES][ENTITIES_DRAGONS]

    pathfinding.find_and_set_adventurer_path(dungeon, adventurer, dragons)

def do_dragon_collisions(adventurer: AdventurerT, dragons: list[DragonT]) -> GameStateT | NoneType:
    adventurer_room_pos: RoomPosT = adventurer[ENTITY_ROOM_POS]
    adventurer_level: int = adventurer[ENTITY_LEVEL]

    # segregate dragons
    strong_dragons: list[DragonT] = []
    weak_dragons: list[DragonT] = []
    for dragon in dragons:
        # player loses against dragons who have a STRICTLY BIGGER level
        if dragon[ENTITY_LEVEL] > adventurer_level:
            strong_dragons.append(dragon)
        # player wins against dragons who have a LOWER OR EQUAL level
        else:
            weak_dragons.append(dragon)

    log_debug_full(f"dungeon has {len(weak_dragons)} weak dragons")

    # check dragon collisions
    for dragon in dragons:
        # ignore dragons not in same room
        if adventurer_room_pos != dragon[ENTITY_ROOM_POS]:
            continue

        if dragon in weak_dragons: # player eats weak dragon
            log_debug_full("dragon slained")
            # remove dragon from dragons list
            dragons.remove(dragon)

            # add 1 to player level
            adventurer[ENTITY_LEVEL] += 1
        elif dragon in strong_dragons: # player loses against stronger dragon
            # finish game
            return STATE_GAME_DONE_LOST

    # handle game win if last dragon slain
    if len(dragons) == 0:
        return STATE_GAME_DONE_WON

    return None

def do_treasure_collisions(adventurer: AdventurerT, entities):
    treasure: TreasureT | NoneType = entities[ENTITIES_TREASURE]
    if not treasure_is_valid(treasure):
        return

    # remove treasure if collided with player
    if adventurer[ENTITY_ROOM_POS] == treasure[TREASURE_ROOM_POS]:
        entities[ENTITIES_TREASURE] = None

def do_collisions(game_context: GameContextT):
    # adventurer or dragons not initialized
    adventurer = game_context[GAME_CONTEXT_GAME_DATA][GAME_DATA_ENTITIES][ENTITIES_ADVENTURER]
    dragons: list = game_context[GAME_CONTEXT_GAME_DATA][GAME_DATA_ENTITIES][ENTITIES_DRAGONS]
    if adventurer == None or dragons == None:
        return

    # handle dragon collisions
    new_state = do_dragon_collisions(adventurer, dragons)
    if new_state != None:
        game_context[GAME_CONTEXT_GAME_STATE] = new_state
        return

    # handle treasure collisions
    do_treasure_collisions(adventurer, game_context[GAME_CONTEXT_GAME_DATA][GAME_DATA_ENTITIES])
    

def do_dungeon_turn(game_context: GameContextT):
    adventurer: AdventurerT = game_context[GAME_CONTEXT_GAME_DATA][GAME_DATA_ENTITIES][ENTITIES_ADVENTURER]

    # move adventurer along path
    # pathfinding.find_and_set_adventurer_path(adventurer, dragons)
    pathfinding.do_adventurer_path(adventurer)
    adventurer[ADVENTURER_PATH] = None

    # handle collisions between adventurer and dragons
    do_collisions(game_context)

def move_dragons_randomly(dungeon: DungeonT, entities: EntitiesT):
    """
    Moves each dragon one step in a randomly chosen accessible direction,
    and updates its position in the game state.
    """
    dragons: list = entities[ENTITIES_DRAGONS]
    entities_positions = _get_entities_positions(entities)

    # remove adventure bcs adventurer needs to fight dragon
    entities_positions.remove(entities[ENTITIES_ADVENTURER][ENTITY_ROOM_POS])

    for dragon in dragons:
        dragon_pos: RoomPosT = dragon[ENTITY_ROOM_POS]
        
        # get list of all valid, connected rooms the dragon can move to
        available_moves = dungeon_get_valid_neighbor_rooms(dungeon, dragon_pos)

        # remove rooms that already have entities
        filter_func = lambda room: not room in entities_positions
        available_moves = list(filter(filter_func, available_moves))

        # pick a random move if any are available
        if available_moves:
            random_available_move_i = randrange(0, len(available_moves))
            new_pos = available_moves[random_available_move_i]

            # update entities_positions to change dragon position so dragons dont overlap
            idx = entities_positions.index(dragon[ENTITY_ROOM_POS])
            entities_positions[idx] = new_pos

            dragon[ENTITY_ROOM_POS] = new_pos

