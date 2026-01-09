import random
from copy import deepcopy
from random import randrange

import src.engine.pathfinding as pathfinding
from src.engine.fps_manager import *
from src.engine.structs.dungeon import *
from src.engine.structs.entity import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *
from src.engine.structs.treasure import *
from src.engine.event_info import *
from src.engine.parsing import *
from src.engine.structs.entity import *
from src.engine.engine_config import *

from src.game.game_definitions import *
from src.game.state_manager import *

from src.utils.entity_utils import *


def load_game_data(game_context, game_data: GameDataT):
    game_context[T_GAME_CTX_GAME_DATA][:] = deepcopy(game_data)

    # save original game data also
    game_context[T_GAME_CTX_ORIGINAL_GAME_DATA][:] = deepcopy(game_data)

def reset_game_context(game_context):
    game_context[:] = game_context_create(assets=game_context[T_GAME_CTX_ASSETS],
                                          game_flags=GAME_FLAGS_STARTUP_FLAGS,
                                          event=game_event_create(),
                                          game_data=game_data_init(),
                                          original_game_data=game_data_init(),
                                          fps_manager=game_context[T_GAME_CTX_FPS_MANAGER])

def reset_game_data(game_context):
    # reset to originals by copying orignals, copy inplace
    game_context[T_GAME_CTX_GAME_DATA][:] = deepcopy(game_context[T_GAME_CTX_ORIGINAL_GAME_DATA])

def invalidate_adventurer_path(game_context):
    game_context[T_GAME_CTX_GAME_FLAGS] |= F_GAME_UPDATE_PATH

def validate_adventurer_path(game_context):
    game_context[T_GAME_CTX_GAME_FLAGS] &= ~F_GAME_UPDATE_PATH

def start_moving_adventurer(game_context):
    game_context[T_GAME_CTX_GAME_FLAGS] |= F_GAME_ADVENTURER_MOVING
    game_context[T_GAME_CTX_GAME_FLAGS] &= ~F_GAME_HANDLE_EVENTS

def stop_moving_adventurer(game_context):
    game_context[T_GAME_CTX_GAME_FLAGS] |= F_GAME_HANDLE_EVENTS

    # in extreme mode we can't stop moving the adventurer after the first round
    # if game is finished we can stop moving though
    game_finished = game_context[T_GAME_CTX_GAME_FLAGS] & F_GAME_GAME_FINISHED
    if past_first_round_extreme_mode(game_context) and not game_finished:
        # sleep a bit between rounds in extreme mode
        fps_manager_game_sleep(game_context[T_GAME_CTX_FPS_MANAGER], INTERVAL_BETWEEN_ROUNDS)
        return # dont reset moving flag

    game_context[T_GAME_CTX_GAME_FLAGS] &= ~F_GAME_ADVENTURER_MOVING

def past_first_round_extreme_mode(game_context):
    game_data = game_context[T_GAME_CTX_GAME_DATA]
    return game_data[T_GAME_DATA_GAME_MODE] == E_GAME_MODE_EXTREME and game_data[T_GAME_DATA_ROUND] > 1

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

def _finish_round(game_context: GameContextT):
    # move dragons randomly
    dungeon: DungeonT = game_context[T_GAME_CTX_GAME_DATA][T_GAME_DATA_DUNGEON]
    entity_system: EntitySystemT = game_context[T_GAME_CTX_GAME_DATA][T_GAME_DATA_ENTITY_SYSTEM]

    _move_dragons_randomly(dungeon, entity_system)
    do_collisions(game_context) # handle collisions bcs we moved dragons

    # increment round counter only if game still going on
    if not (game_context[T_GAME_CTX_GAME_FLAGS] & F_GAME_GAME_FINISHED):
        game_context[T_GAME_CTX_GAME_DATA][T_GAME_DATA_ROUND] += 1

    # reset flags to say that adventurer stopped moving
    stop_moving_adventurer(game_context)

    # update player path next frame
    invalidate_adventurer_path(game_context)

def _move_dragons_randomly(dungeon: DungeonT, entity_system: EntitySystemT):
    """
    Moves each dragon one step in a randomly chosen accessible direction,
    and updates its position in the game state.
    """
    adventurer: AdventurerT = entity_system_get_first_and_only(entity_system, E_ENTITY_ADVENTURER)
    dragons: list = entity_system_get_all(entity_system, E_ENTITY_DRAGON)
    
    entities_positions = get_all_entity_positions(entity_system)

    # remove adventure pos bcs dragon can move towards the adventurer
    entities_positions.remove(adventurer[T_BASE_ENTITY_ROOM_POS])

    for dragon in dragons:
        dragon_pos: RoomPosT = dragon[T_BASE_ENTITY_ROOM_POS]
        
        # get list of all valid, connected rooms the dragon can move to
        available_moves = dungeon_get_valid_neighbor_rooms(dungeon, dragon_pos)

        # remove rooms that already have entities
        filter_func = lambda room: not room in entities_positions
        available_moves = list(filter(filter_func, available_moves))

        # pick a random move if any are available
        if available_moves:
            # random_available_move_i = randrange(0, len(available_moves))
            # new_pos = available_moves[random_available_move_i]
            new_pos = random.choice(available_moves)

            # update entities_positions to update dragon position so dragons dont overlap
            entities_positions.remove(dragon[T_BASE_ENTITY_ROOM_POS])
            entities_positions.add(new_pos)

            dragon[T_BASE_ENTITY_ROOM_POS] = new_pos

def _do_dragon_collisions(entity_system: EntitySystemT) -> GameFlags | NoneType:
    adventurer = entity_system_get_first_and_only(entity_system, E_ENTITY_ADVENTURER)
    dragons: list = entity_system_get_all(entity_system, E_ENTITY_DRAGON)

    adventurer_room_pos: RoomPosT = adventurer[T_BASE_ENTITY_ROOM_POS]
    adventurer_level: int = adventurer[T_ENTITY_LEVEL]

    # segregate dragons
    strong_dragons: list[DragonT] = []
    weak_dragons: list[DragonT] = []
    for dragon in dragons:
        # player loses against dragons who have a STRICTLY BIGGER level
        if dragon[T_ENTITY_LEVEL] > adventurer_level:
            strong_dragons.append(dragon)
        # player wins against dragons who have a LOWER OR EQUAL level
        else:
            weak_dragons.append(dragon)

    log_debug_full(f"dungeon has {len(weak_dragons)} weak dragons")

    # check dragon collisions
    for dragon in dragons:
        # ignore dragons not in same room
        if adventurer_room_pos != dragon[T_BASE_ENTITY_ROOM_POS]:
            continue

        # refresh each time cuz we can use it
        adventurer_has_strong_sword = inventory_has_item(adventurer[T_ADVENTURER_INVENTORY], E_INVENTORY_ITEM_STRONG_SWORD)
        beat_stronger_dragon = dragon in strong_dragons and adventurer_has_strong_sword

        # regular weak dragon
        # or stronger dragon, but player has strong sword
        if dragon in weak_dragons or beat_stronger_dragon:
            log_debug("dragon slained")

            # remove dragon from dragons list
            # dragons.remove(dragon)
            entity_system_remove_entity(entity_system, dragon)

            # add 1 to player level
            adventurer[T_ENTITY_LEVEL] += 1

            # if used stronger sword then consume it (remove it from inventory)
            if beat_stronger_dragon:
                inventory_remove_item(adventurer[T_ADVENTURER_INVENTORY], E_INVENTORY_ITEM_STRONG_SWORD)
        elif dragon in strong_dragons: # player loses against stronger dragon (doesnt have strong sword)
            # finish game
            return F_GAME_GAME_FINISHED | F_GAME_GAME_LOST

    # handle game win if last dragon slain
    if len(dragons) == 0:
        return F_GAME_GAME_FINISHED | F_GAME_GAME_WON

    return None

def _do_treasure_collisions(entity_system: EntitySystemT):
    adventurer = entity_system_get_first_and_only(entity_system, E_ENTITY_ADVENTURER)

    treasure = entity_system_get_first_and_only(entity_system, E_ENTITY_TREASURE)
    if not treasure_is_valid(treasure):
        return
    
    # remove treasure if collided with player
    if adventurer[T_BASE_ENTITY_ROOM_POS] == treasure[T_BASE_ENTITY_ROOM_POS]:
        entity_system_remove_first_and_only(entity_system, E_ENTITY_TREASURE)

def rotate_room(event_info: EventInfoT, game_context: GameContextT) -> bool:
    game_data = game_context[T_GAME_CTX_GAME_DATA]
    dungeon: DungeonT = game_data[T_GAME_DATA_DUNGEON]

    # cant rotate room in extreme mode past round 1
    if past_first_round_extreme_mode(game_context):
        return False

    clicked_room: RoomPosT | NoneType = _get_clicked_room(event_info, dungeon)

    # clicked invalid room
    if clicked_room == None:
        return False

    # rotate room and invalidate adventurer path
    dungeon_rotate_room(dungeon, row=clicked_room[ROOM_POS_ROW], col=clicked_room[ROOM_POS_COL])
    return True

def place_treasure(event_info: EventInfoT, game_context: GameContextT) -> bool:
    """
    room_pos: room position in which to place the treasure
    """
    game_data = game_context[T_GAME_CTX_GAME_DATA]
    dungeon: DungeonT = game_data[T_GAME_DATA_DUNGEON]
    entity_system: EntitySystemT = game_data[T_GAME_DATA_ENTITY_SYSTEM]

    # cant place treasure in extreme mode past round 1
    if past_first_round_extreme_mode(game_context):
        return False

    # skip if no more treasures left
    treasure_count: int = game_data[T_GAME_DATA_TREASURE_COUNT]
    if treasure_count <= 0:
        return False

    # check if there is already a treasure placed in the dungeon
    existing_treasure = entity_system_get_first_and_only(entity_system, E_ENTITY_TREASURE)
    log_debug_full(f"existing treasure: {existing_treasure}")
    if treasure_is_valid(existing_treasure):
        log_error(f"cant place treasure, a treasure is already in the dungeon: {existing_treasure}")
        return False

    # get clicked room pos
    room_pos: RoomPosT | NoneType = _get_clicked_room(event_info, dungeon)
    if room_pos == None: # clicked outside of dungeon
        log_error("failed to place treasure, invalid room clicked")
        return False

    # check if there is already an entity in that room
    entities_positions = get_all_entity_positions(entity_system)
    if room_pos in entities_positions: # clicked room already contains an entity
        log_error("can't place treasure, there is already an entity in that room")
        return False

    # create treasure entity
    treasure: TreasureT = treasure_create(room_pos=room_pos, image_id=randrange(T_TREASURES_IMAGE_COUNT))
    entity_system_add_entity(entity_system, treasure)

    # decrease treasure count since we placed a treasure
    game_data[T_GAME_DATA_TREASURE_COUNT] -= 1
    return True

def manually_update_player_path(event_info: EventInfoT, game_context: GameContextT):
    ev: FltkEvent = event_info[EVENT_INFO_EV]
    click_postion = fltk_ext.position_souris(ev)

    # get room at click positons
    clicked_room_row: int = click_postion[1] // BLOCK_SCALED_SIZE[1]
    clicked_room_col: int = click_postion[0] // BLOCK_SCALED_SIZE[0]
    clicked_room_pos: RoomPosT = (clicked_room_col, clicked_room_row)

    # if cursor outside of dungeon do nothing
    dungeon: DungeonT = game_context[T_GAME_CTX_GAME_DATA][T_GAME_DATA_DUNGEON]
    if clicked_room_row >= dungeon_get_width(dungeon) or clicked_room_col >= dungeon_get_height(dungeon):
        return

    adventurer: AdventurerT = game_context[T_GAME_CTX_GAME_DATA][T_GAME_DATA_ENTITY_SYSTEM][T_ENTITIES_ADVENTURER]

    # init adventurer path if its None
    if adventurer[T_ADVENTURER_PATH] == None:
        adventurer[T_ADVENTURER_PATH] = MovementPathT()

    # ensure previous room adjacent and connected to clicked pos
    dungeon: DungeonT = game_context[T_GAME_CTX_GAME_DATA][T_GAME_DATA_DUNGEON]
    movement_path: MovementPathT = adventurer[T_ADVENTURER_PATH]
    previous_clicked_room_pos: RoomPosT = adventurer[T_BASE_ENTITY_ROOM_POS] # set last click room to player pos if 0 clicks
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
    pathfinding.find_and_set_adventurer_path(game_context[T_GAME_CTX_GAME_DATA])

def do_collisions(game_context: GameContextT):
    entity_system: EntitySystemT = game_context[T_GAME_CTX_GAME_DATA][T_GAME_DATA_ENTITY_SYSTEM]

    adventurer = entity_system_get_first_and_only(entity_system, E_ENTITY_ADVENTURER)
    dragons: list = entity_system_get_all(entity_system, E_ENTITY_DRAGON)

    # adventurer or dragons not initialized
    if adventurer == None or dragons == None:
        return

    # handle dragon collisions
    new_flags_to_add = _do_dragon_collisions(entity_system)
    if new_flags_to_add != None:
        game_context[T_GAME_CTX_GAME_FLAGS] |= new_flags_to_add
        return

    # handle treasure collisions
    _do_treasure_collisions(entity_system)

def move_adventurer_along_path(game_context: GameContextT):
    entity_system: EntitySystemT = game_context[T_GAME_CTX_GAME_DATA][T_GAME_DATA_ENTITY_SYSTEM]
    adventurer: AdventurerT = entity_system_get_first_and_only(entity_system, E_ENTITY_ADVENTURER)

    # move adventurer along path
    finished_moving = pathfinding.do_adventurer_path(adventurer, entity_system)

    # handle collisions
    do_collisions(game_context)

    # exit early if game finished
    if game_context[T_GAME_CTX_GAME_FLAGS] & F_GAME_GAME_FINISHED:
        stop_moving_adventurer(game_context)
        return

    # wait a bit between each step to make it smoother
    fps_manager_game_sleep(game_context[T_GAME_CTX_FPS_MANAGER], INTERVAL_BETWEEN_PATH_STEPS)

    # finished last step
    if finished_moving:
        _finish_round(game_context)
        return

# def handle_sleep(game_context: GameContextT) -> bool:
#     """
#     returns: True if can continue doing game logic
#     """
#     fps_manager: FpsManagerT = game_context[T_GAME_CTX_FPS_MANAGER]
#     game_flags: GameFlags = game_context[T_GAME_CTX_GAME_FLAGS]
#
#     sleep_tag = game_flags & F_GAME_SLEEPING
#     slept_enough = fps_manager_slept_enough(fps_manager)
#
#     # sleeping and not finished
#     if sleep_tag and not slept_enough:
#         return False
#     # sleeping but finished
#     elif sleep_tag and slept_enough:
#         # remove sleep flag
#         game_context[T_GAME_CTX_GAME_FLAGS] &= ~F_GAME_SLEEPING
#
#     return True

def handle_game_logic_unsleepable(game_context: GameContextT):
    """
    game logic that we CAN'T do when we are sleeping
    """
    game_flags: GameFlags = game_context[T_GAME_CTX_GAME_FLAGS]

    # move adventurer
    if game_flags & F_GAME_ADVENTURER_MOVING:
        move_adventurer_along_path(game_context)

def handle_game_logic_sleepable(game_context: GameContextT):
    """
    game logic that we CAN even when we are sleeping
    """
    game_flags: GameFlags = game_context[T_GAME_CTX_GAME_FLAGS]

    # update path bcs invalidated
    if game_flags & F_GAME_UPDATE_PATH:
        auto_update_player_path(game_context)
        validate_adventurer_path(game_context)
        log_debug_full("updated path")

def handle_game_logic(game_context: GameContextT):
    fps_manager: FpsManagerT = game_context[T_GAME_CTX_FPS_MANAGER]

    # handle stuff that we can do when sleepign
    handle_game_logic_sleepable(game_context)

    # handle sleeping
    if fps_manager_is_sleeping(fps_manager) and not fps_manager_slept_enough(fps_manager):
        return

    # handle stuff that we can only do when not sleepign
    handle_game_logic_unsleepable(game_context)

    # mark frame as handled
    fps_manager_handled_frame(fps_manager)

def handle_logic(game_context: GameContextT):
    game_flags: GameFlags = game_context[T_GAME_CTX_GAME_FLAGS]

    if game_flags & F_GAME_GAME:
        handle_game_logic(game_context)
