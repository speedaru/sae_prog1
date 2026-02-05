import random
from copy import deepcopy
from random import randrange

import src.engine.pathfinding as pathfinding
from src.engine.fps_manager import *
from src.engine.game_event_system import *
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

from src.game.game_events.chaos_seal import *

from src.utils.entity_utils import *


# -------------------- private functions

def _get_clicked_room(event_info: InputEventInfoT, dungeon: DungeonT) -> RoomPosT | NoneType:
    ev: FltkEvent = event_info[INPUT_EVENT_INFO_EV]
    click_postion = fltk_ext.position_souris(ev)

    # get cliked room, and check if its None (clciked outside of dungeon)
    clicked_room = dungeon_get_room_pos_from_screen_pos(dungeon, click_postion)
    if clicked_room == None:
        return

    clicked_room_pos: RoomPosT = clicked_room

    # if cursor outside of dungeon do nothing
    if not dungeon_room_pos_in_bounds(dungeon, clicked_room_pos):
        return None

    return clicked_room_pos

def _move_dragons_randomly(game_context: GameContextT):
    """
    Moves each dragon one step in a randomly chosen accessible direction,
    and updates its position in the game state.
    """
    game_data = game_context[T_GAME_CTX_GAME_DATA]
    dungeon: DungeonT = game_data[T_DUNGEON_DATA_DUNGEON]
    entity_system: EntitySystemT = game_data[T_DUNGEON_DATA_ENTITY_SYSTEM]

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

# -------------------- public functions

def game_sleep(game_context: GameContextT, duration: float):
    fps_manager: FpsManagerT = game_context[T_GAME_CTX_FPS_MANAGER]
    es: GameEventSystemT = game_context[T_GAME_CTX_GAME_DATA][T_GAME_DATA_EVENT_SYSTEM]

    fps_manager_game_sleep(fps_manager, duration)
    game_systems_handle_pause(es, pause=True)

def load_game_data(game_context, game_data: GameDataT):
    """
    function to load a new game
    """
    # just in case, reset event system so we dont deep copy it
    game_data[T_GAME_DATA_EVENT_SYSTEM] = game_event_system_create()

    # if game_data is not litterally game_context[T_GAME_CTX_GAME_DATA]
    if not game_context[T_GAME_CTX_GAME_DATA] is game_data:
        game_context[T_GAME_CTX_GAME_DATA][:] = deepcopy(game_data)

    # init game systems
    game_systems_setup(game_context)

    # save original game data
    # purposefully dont copy game_event_system bcs then we cant deepcopy it
    game_context[T_GAME_CTX_ORIGINAL_GAME_DATA][:] = deepcopy(game_data)

def reset_game_context(game_context):
    # recreate new game context from scratch basicly
    game_context[:] = game_context_create(assets=game_context[T_GAME_CTX_ASSETS],
                                          game_flags=GAME_FLAGS_STARTUP,
                                          active_window=E_WINDOW_START,
                                          event=input_event_create(),
                                          game_data=game_data_init(),
                                          original_game_data=game_data_init(),
                                          fps_manager=game_context[T_GAME_CTX_FPS_MANAGER])

def reset_game_data(game_context):
    # reset to originals by copying orignals, copy inplace
    game_context[T_GAME_CTX_GAME_DATA][:] = deepcopy(game_context[T_GAME_CTX_ORIGINAL_GAME_DATA])

    # setup again game event system manually, bcs cant deepcopy it
    game_systems_setup(game_context)

def invalidate_adventurer_path(game_context):
    game_context[T_GAME_CTX_GAME_FLAGS] |= F_GAME_UPDATE_PATH

def validate_adventurer_path(game_context):
    game_context[T_GAME_CTX_GAME_FLAGS] &= ~F_GAME_UPDATE_PATH

def start_moving_adventurer(game_context):
    # add moving flag
    game_context[T_GAME_CTX_GAME_FLAGS] |= F_GAME_ADVENTURER_MOVING

def single_turn_mode_past_first_round(game_context):
    game_data = game_context[T_GAME_CTX_GAME_DATA]
    return game_data[T_DUNGEON_DATA_GAME_MODE] == E_GAME_MODE_SINGLE_TURN and game_data[T_GAME_DATA_ROUND] > 1

# def can_remove_moving_flag(game_context):
#     """
#     returns True if game finished
#         or: path finished AND not in single_turn mode
#     """
#     # game finished
#     game_flags: int = game_context[T_GAME_CTX_GAME_FLAGS]
#     if game_flags & F_GAME_GAME_FINISHED:
#         return True
#
#     # path not finished
#     entity_system: EntitySystemT = game_context[T_GAME_CTX_GAME_DATA][T_GAME_DATA_ENTITY_SYSTEM]
#     adventurer: AdventurerT = entity_system_get_first_and_only(entity_system, E_ENTITY_ADVENTURER)
#     if movement_path_is_valid(adventurer[T_ADVENTURER_PATH]):
#         return False
#
#     # cant remove moving flag in single_turn mode (if game not finished)
#     game_data = game_context[T_GAME_CTX_GAME_DATA]
#     if game_data[T_GAME_DATA_GAME_MODE] == E_GAME_MODE_single_turn:
#         return False
#     
#     # not in single_turn mode
#     return True

def should_finish_round(game_context: GameContextT) -> bool:
    """
    round should finish when:
        adventurer reached end of path
        and adventurer moving flag has not been removed yet
    """
    entity_system: EntitySystemT = game_context[T_GAME_CTX_GAME_DATA][T_DUNGEON_DATA_ENTITY_SYSTEM]
    adventurer: AdventurerT = entity_system_get_first_and_only(entity_system, E_ENTITY_ADVENTURER)
    game_flags: int = game_context[T_GAME_CTX_GAME_FLAGS]

    return not movement_path_is_valid(adventurer[T_ADVENTURER_PATH]) and game_flags & F_GAME_ADVENTURER_MOVING


# -------------------- do stuff

def rotate_room(event_info: InputEventInfoT, game_context: GameContextT) -> bool:
    game_data = game_context[T_GAME_CTX_GAME_DATA]
    dungeon: DungeonT = game_data[T_DUNGEON_DATA_DUNGEON]

    # cant rotate room in single_turn mode past round 1
    if single_turn_mode_past_first_round(game_context):
        return False

    clicked_room: RoomPosT | NoneType = _get_clicked_room(event_info, dungeon)

    # clicked invalid room
    if clicked_room == None:
        return False

    # rotate room and invalidate adventurer path
    dungeon_rotate_room(dungeon, row=clicked_room[ROOM_POS_ROW], col=clicked_room[ROOM_POS_COL])
    return True

def place_treasure(event_info: InputEventInfoT, game_context: GameContextT) -> bool:
    """
    room_pos: room position in which to place the treasure
    """
    game_data = game_context[T_GAME_CTX_GAME_DATA]
    dungeon: DungeonT = game_data[T_DUNGEON_DATA_DUNGEON]
    entity_system: EntitySystemT = game_data[T_DUNGEON_DATA_ENTITY_SYSTEM]

    # cant place treasure in single_turn mode past round 1
    if single_turn_mode_past_first_round(game_context):
        return False

    # skip if no more treasures left
    treasure_count: int = game_data[T_DUNGEON_DATA_TREASURE_COUNT]
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
    game_data[T_DUNGEON_DATA_TREASURE_COUNT] -= 1
    return True

def manually_update_player_path(event_info: InputEventInfoT, game_context: GameContextT):
    ev: FltkEvent = event_info[INPUT_EVENT_INFO_EV]
    click_postion = fltk_ext.position_souris(ev)

    # get room at click positons
    clicked_room_row: int = click_postion[1] // BLOCK_SCALED_SIZE[1]
    clicked_room_col: int = click_postion[0] // BLOCK_SCALED_SIZE[0]
    clicked_room_pos: RoomPosT = (clicked_room_col, clicked_room_row)

    # if cursor outside of dungeon do nothing
    dungeon: DungeonT = game_context[T_GAME_CTX_GAME_DATA][T_DUNGEON_DATA_DUNGEON]
    if clicked_room_row >= dungeon_get_width(dungeon) or clicked_room_col >= dungeon_get_height(dungeon):
        return

    adventurer: AdventurerT = game_context[T_GAME_CTX_GAME_DATA][T_DUNGEON_DATA_ENTITY_SYSTEM][T_ENTITIES_ADVENTURER]

    # init adventurer path if its None
    if adventurer[T_ADVENTURER_PATH] == None:
        adventurer[T_ADVENTURER_PATH] = MovementPathT()

    # ensure previous room adjacent and connected to clicked pos
    dungeon: DungeonT = game_context[T_GAME_CTX_GAME_DATA][T_DUNGEON_DATA_DUNGEON]
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
    """
    recalculates adventurer path
    """
    # update path 
    pathfinding.find_and_set_adventurer_path(game_context[T_GAME_CTX_GAME_DATA])

def update_player_path(game_event: GameEventT):
    """
    GAME EVENT
    calls auto_update_player_path but performs checks to see if we need to recalculate it
    """
    game_context: GameContextT = game_event[T_GAME_EVENT_GAME_CTX]
    game_flags: int = game_context[T_GAME_CTX_GAME_FLAGS]
    window: WindowE = game_context[T_GAME_CTX_ACTIVE_WINDOW]

    # not in game
    if window != E_WINDOW_GAME:
        return

    entity_system: EntitySystemT = game_context[T_GAME_CTX_GAME_DATA][T_DUNGEON_DATA_ENTITY_SYSTEM]
    adventurer: AdventurerT = entity_system_get_first_and_only(entity_system, E_ENTITY_ADVENTURER)

    # UPDATE_PATH is set so we need to recalculate the path
    if bool(game_flags & F_GAME_UPDATE_PATH):
        auto_update_player_path(game_context)
        validate_adventurer_path(game_context)
    # invalidate adventurer path if its not set
    elif not movement_path_is_valid(adventurer[T_ADVENTURER_PATH]):
        invalidate_adventurer_path(game_context)

def do_collisions(game_context: GameContextT):
    """
    GAME EVENT
    """
    entity_system: EntitySystemT = game_context[T_GAME_CTX_GAME_DATA][T_DUNGEON_DATA_ENTITY_SYSTEM]

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

    # # handle treasure collisions
    # _do_treasure_collisions(entity_system)

def move_adventurer_along_path(game_event: GameEventT):
    """
    GAME EVENT
    continue moving the adventurer to the next room
    """
    game_ctx: GameContextT = game_event[T_GAME_EVENT_GAME_CTX]

    entity_system: EntitySystemT = game_ctx[T_GAME_CTX_GAME_DATA][T_DUNGEON_DATA_ENTITY_SYSTEM]
    adventurer: AdventurerT = entity_system_get_first_and_only(entity_system, E_ENTITY_ADVENTURER)

    # if in single turn mode and cant move then lost
    adventurer_path = adventurer[T_ADVENTURER_PATH]
    if not movement_path_is_valid(adventurer_path) and single_turn_mode_past_first_round(game_ctx):
        game_ctx[T_GAME_CTX_GAME_FLAGS] |= F_GAME_GAME_FINISHED | F_GAME_GAME_LOST
        game_ctx[T_GAME_CTX_GAME_FLAGS] &= ~F_GAME_ADVENTURER_MOVING
        log_debug("finished")
        return

    # dont move adventurer if:
    #   ADVENTURER_MOVING flag is not set
    #   or path is empty
    game_flags: int = game_ctx[T_GAME_CTX_GAME_FLAGS]
    if not (game_flags & F_GAME_ADVENTURER_MOVING) or not movement_path_is_valid(adventurer[T_ADVENTURER_PATH]):
        return

    # move adventurer to next room
    pathfinding.do_adventurer_path(adventurer, entity_system)

def adventurer_sleep_between_steps(game_event: GameEventT):
    """
    GAME EVENT
    sleep in between each adventurer step, but dont sleep if round finished
    """
    game_context: GameContextT = game_event[T_GAME_EVENT_GAME_CTX]
    entity_system: EntitySystemT = game_context[T_GAME_CTX_GAME_DATA][T_DUNGEON_DATA_ENTITY_SYSTEM]
    adventurer: AdventurerT = entity_system_get_first_and_only(entity_system, E_ENTITY_ADVENTURER)

    # dont sleep if:
    #   ADVENTURER_MOVING flag is not set
    #   or adventurer path is empty
    game_flags: int = game_context[T_GAME_CTX_GAME_FLAGS]
    if not (game_flags & F_GAME_ADVENTURER_MOVING) or not movement_path_is_valid(adventurer[T_ADVENTURER_PATH]):
        return

    # sleep if there are still moves left
    game_sleep(game_context, INTERVAL_BETWEEN_PATH_STEPS)

def adventurer_sleep_between_rounds(game_event: GameEventT):
    """
    GAME EVENT
    sleep in between each (for single_turn mode since its on autoplay)
    """
    game_context: GameContextT = game_event[T_GAME_EVENT_GAME_CTX]
    game_data = game_context[T_GAME_CTX_GAME_DATA]

    # adventurer moving flag is not set
    game_flags: int = game_context[T_GAME_CTX_GAME_FLAGS]
    if not (game_flags & F_GAME_ADVENTURER_MOVING):
        return

    # not in single_turn mode
    if game_data[T_DUNGEON_DATA_GAME_MODE] != E_GAME_MODE_SINGLE_TURN:
        return

    # sleep
    game_sleep(game_context, INTERVAL_BETWEEN_ROUNDS)

def pickup_items(game_event: GameEventT):
    """
    GAME EVENT
    if any items is in room_poos then it will pick it up and place it in inventory
    """
    game_data = game_event[T_GAME_EVENT_GAME_CTX][T_GAME_CTX_GAME_DATA]
    entity_system: EntitySystemT = game_data[T_DUNGEON_DATA_ENTITY_SYSTEM]
    adventurer: AdventurerT = entity_system_get_first_and_only(entity_system, E_ENTITY_ADVENTURER)

    entity_items = entity_system_get_all_types(entity_system, ENTITY_ITEMS)

    for i in range(len(entity_items)):
        base_entity: list = entity_items[i]
        if base_entity[T_BASE_ENTITY_ROOM_POS] == adventurer[T_BASE_ENTITY_ROOM_POS]:
            log_debug_full(f"found item in current room: {adventurer[T_BASE_ENTITY_ROOM_POS]}")

            # get consume callback for item
            consume_callback = None
            entity_type = base_entity[T_BASE_ENTITY_TYPE]
            if entity_type == E_ENTITY_CHAOS_SEAL:
                consume_callback = chaos_seal_event_register
            
            # no data for now, we just know that we have that item, no item specific info
            inventory_item = inventory_item_create(item_type=base_entity[T_BASE_ENTITY_TYPE],
                                                   item_data=None,
                                                   consume_callback=consume_callback)

            # add item to inventory
            inventory_add_item(adventurer[T_ADVENTURER_INVENTORY], inventory_item)

            # remove picked up items from entities
            entity_system_remove_entity(entity_system, base_entity)
            break

def instaconsume_items(game_event: GameEventT):
    """
    GAME EVENT
    insta consume any item inventory that is in ENTITY_ITEMS_INSTACONSUME
    """
    game_ctx = game_event[T_GAME_EVENT_GAME_CTX]
    game_data = game_ctx[T_GAME_CTX_GAME_DATA]
    entity_system: EntitySystemT = game_data[T_DUNGEON_DATA_ENTITY_SYSTEM]
    adventurer: AdventurerT = entity_system_get_first_and_only(entity_system, E_ENTITY_ADVENTURER)

    inventory: InventoryT = adventurer[T_ADVENTURER_INVENTORY]

    for inventory_item in inventory:
        # check if is instanconsume item
        if inventory_item[T_INVENTORY_ITEM_TYPE] in ENTITY_ITEMS_INSTACONSUME:
            inventory_consume_item(inventory, inventory_item, callback_param=game_ctx)

    invalidate_adventurer_path(game_ctx)

def stop_moving_adventurer(game_event: GameEventT):
    """
    GAME EVENT
    """
    game_context: GameContextT = game_event[T_GAME_EVENT_GAME_CTX]

    # remove moving flag
    game_context[T_GAME_CTX_GAME_FLAGS] &= ~F_GAME_ADVENTURER_MOVING

def foo_do_collisions(game_event: GameEventT):
    game_context: GameContextT = game_event[T_GAME_EVENT_GAME_CTX]

    do_collisions(game_context)

def move_dragons_randomly(game_event: GameEventT):
    """
    GAME EVENT
    """
    game_context: GameContextT = game_event[T_GAME_EVENT_GAME_CTX]

    # dont move dragons if game finished
    if bool(game_context[T_GAME_CTX_GAME_FLAGS] & F_GAME_GAME_FINISHED):
        return

    # dont move dragons if player moving
    if game_context[T_GAME_CTX_GAME_FLAGS] & F_GAME_ADVENTURER_MOVING:
        return

    log_debug("[event system] moving dragons")
    _move_dragons_randomly(game_context)
    game_sleep(game_context, 1)

def single_turn_mode_autoplay_adventurer(game_event: GameEventT):
    """
    GAME EVENT
    if past first round then start moving adventurer
    """
    game_ctx = game_event[T_GAME_EVENT_GAME_CTX]

    # if after round 1 in single turn mode and ADVENTURER_MOVING flag not set
    if single_turn_mode_past_first_round(game_ctx) and not bool(game_ctx[T_GAME_CTX_GAME_FLAGS] & F_GAME_ADVENTURER_MOVING):
        start_moving_adventurer(game_ctx)

def game_systems_setup(game_context: GameContextT):
    es: GameEventSystemT = game_context[T_GAME_CTX_GAME_DATA][T_GAME_DATA_EVENT_SYSTEM]

    dragon_update_frequency = "on_frame" if game_context[T_GAME_CTX_GAME_DATA][T_DUNGEON_DATA_GAME_MODE] == E_GAME_MODE_EXTREME else "on_round_end"

    systems = {
        # path calculation and other logic
        E_PHASE_PRE_LOGIC: [
            { "on_frame": update_player_path }, # update player path if needed
        ],
        # do adventurer movement
        E_PHASE_ADVENTURER: [
            { "on_frame": single_turn_mode_autoplay_adventurer }, # in extreme start moving adventurer automatically
            { "on_frame": move_adventurer_along_path }, # move adventurer to next room
        ],
        # path calculation and other special items logic
        E_PHASE_POST_ADVENTURER: [
            { "on_frame": foo_do_collisions }, # collision check #1 after adventurer moves
            { "on_frame": pickup_items }, # pickup entity items in current room
            { "on_frame": instaconsume_items }, # insta consume items in inventory
        ],
        # do dragons movement (move dragons randomly)
        E_PHASE_DRAGONS: [
            { dragon_update_frequency: move_dragons_randomly },
        ],
        # logic that happens after dragons moved, like collision checks
        E_PHASE_POST_DRAGONS: [
            { "on_round_end": foo_do_collisions }, # handle collisions on_round_end one time per round after dragons moved
        ],
        E_PHASE_CLEANUP: [ # stuff do after did everything else so it doesnt interupt the rest
            { "on_frame": adventurer_sleep_between_steps },
            { "on_round_end": adventurer_sleep_between_rounds },
            { "on_round_end": stop_moving_adventurer }, # remove ADVENTURER_MOVING flag when round ended
        ],
    }

    # register events
    for phase, phase_event_list in systems.items():
        for event in phase_event_list:
            on_frame = event["on_frame"] if "on_frame" in event else None
            on_round_end = event["on_round_end"] if "on_round_end" in event else None
            duration = EVENT_DURATION_PERPERTUAL

            game_event_register(es, phase, duration, on_frame=on_frame, on_round_end=on_round_end, game_ctx=game_context)
        

def game_systems_handle_pause(event_system: GameEventSystemT, pause: bool):
    PHASES_TO_PAUSE = [E_PHASE_ADVENTURER, E_PHASE_DRAGONS]

    if pause:
        for phase in PHASES_TO_PAUSE:
            game_event_system_pause_phase(event_system, phase)
    else:
        for phase in PHASES_TO_PAUSE:
            game_event_system_unpause_phase(event_system, phase)

def handle_game_systems(game_context: GameContextT):
    fps_manager: FpsManagerT = game_context[T_GAME_CTX_FPS_MANAGER]
    event_system: GameEventSystemT = game_context[T_GAME_CTX_GAME_DATA][T_GAME_DATA_EVENT_SYSTEM]

    # unpause game events if finished sleeping
    slept_enough = fps_manager_slept_enough(fps_manager)
    if slept_enough:
        game_systems_handle_pause(event_system, pause=False)

    # run every frame
    game_event_system_frame_tick(event_system)

    # run only when round finished
    if should_finish_round(game_context):
        game_event_system_round_tick(event_system)

        # increment round counter (except if game finished)
        if not game_context[T_GAME_CTX_GAME_FLAGS] & F_GAME_GAME_FINISHED:
            game_context[T_GAME_CTX_GAME_DATA][T_GAME_DATA_ROUND] += 1

def handle_logic(game_context: GameContextT):
    fps_manager: FpsManagerT = game_context[T_GAME_CTX_FPS_MANAGER]
    window: WindowE = game_context[T_GAME_CTX_ACTIVE_WINDOW]

    # dont do game logic if game finihsed
    game_finished = bool(game_context[T_GAME_CTX_GAME_FLAGS] & F_GAME_GAME_FINISHED)
    if game_finished:
        return

    if window == E_WINDOW_GAME:
        # handle_game_logic(game_context)
        handle_game_systems(game_context)

    # mark frame as handled only if not sleeping
    if not fps_manager_is_sleeping(fps_manager):
        fps_manager_handled_frame(fps_manager)

