from types import NoneType

import libs.fltk as fltk
from libs.fltk import FltkEvent, TkEvent

import src.game.logic as logic
import src.engine.parsing as parsing
from src.engine.entity_system import *
from src.engine.structs.dungeon import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *
from src.engine.event_info import *
# from src.engine.parsing import *

from src.game.game_definitions import *
from src.game.state_manager import *
from src.game.keys import *

import src.utils.fltk_extensions as fltk_ext
from src.utils.logging import *



# -------------------- GENERAL EVENT HANDLERS --------------------
def handle_exit_key(input_event: InputEventT, game_context):
    game_flags = game_context[T_GAME_CTX_GAME_FLAGS]

    event_info = input_event_get_info(input_event)
    if event_info[INPUT_EVENT_INFO_TYPE] == None:
        return None

    exit_key_pressed = event_info[INPUT_EVENT_INFO_IS_KEY] and event_info[INPUT_EVENT_INFO_KEY_PRESSED] == EXIT_KEY.lower()

    # start menu -> exit game
    if exit_key_pressed and game_flags & F_GAME_MENU:
        game_context[T_GAME_CTX_GAME_FLAGS] |= F_GAME_EXIT_PROGRAM
    # game screen -> go back to start menu
    elif exit_key_pressed and game_flags & F_GAME_GAME:
        # reset game context to startup value
        logic.reset_game_context(game_context)

def handle_event_start_menu(input_event: InputEventT, game_context: GameContextT):
    """
    Handles events occurring while in the Start Menu state.
    
    Specifically, it listens for a Left Click (KEY_X1) that carries a selected 
    dungeon in its data payload. If a dungeon is selected, it updates the 
    game context to transition to the playing state.
    """
    event_info = input_event_get_info(input_event)
    if event_info[INPUT_EVENT_INFO_TYPE] == None:
        return None

    # switch to game screen
    if event_info[INPUT_EVENT_INFO_TYPE] == KEY_X1:
        # if no dungeon selected ignore event
        if input_event[T_INPUT_EVENT_DATA] == None:
            return

        loaded_game: GameDataT = input_event[T_INPUT_EVENT_DATA]
        # log_trace(f"loaded game, dungeon: {loaded_game[T_GAME_DATA_DUNGEON]=}")
        # log_trace(f"loaded game, adve: {loaded_game[T_GAME_DATA_ENTITY_SYSTEM][T_ENTITIES_ADVENTURER]=}")
        # log_trace(f"loaded game, dragons: {loaded_game[T_GAME_DATA_ENTITY_SYSTEM][T_ENTITIES_DRAGONS]=}")
        logic.load_game_data(game_context, loaded_game)

        game_context[T_GAME_CTX_GAME_FLAGS] = GAME_FLAGS_GAME_START

def handle_event_game(input_event: InputEventT, game_context: GameContextT):
    event_info = input_event_get_info(input_event)
    if event_info[INPUT_EVENT_INFO_TYPE] == None:
        return None

    # reset dungeon
    if event_info[INPUT_EVENT_INFO_IS_KEY] and event_info[INPUT_EVENT_INFO_KEY_PRESSED] == KEY_R:
        logic.reset_game_data(game_context)

        # reset all game flags
        game_context[T_GAME_CTX_GAME_FLAGS] = GAME_FLAGS_GAME_START
    # save game
    elif event_info[INPUT_EVENT_INFO_IS_KEY] and event_info[INPUT_EVENT_INFO_KEY_PRESSED] == KEY_S:
        parsing.save_game(game_context)
    # load saved game
    elif event_info[INPUT_EVENT_INFO_IS_KEY] and event_info[INPUT_EVENT_INFO_KEY_PRESSED] == KEY_I:
        parsing.load_saved_game(game_context)

def handle_event_game_dungeon(input_event: InputEventT, game_context: GameContextT):
    """
    Handles events occurring during the Dungeons's Turn (player controls dungeon).
    """
    log_trace("game event, player turn !")

    event_info = input_event_get_info(input_event)
    if event_info[INPUT_EVENT_INFO_TYPE] == None:
        return None

    # dont handle events if adventurer is currently moving
    if bool(game_context[T_GAME_CTX_GAME_FLAGS] & F_GAME_ADVENTURER_MOVING):
        log_debug(f"[handle_event_game_dungeon] dont handle game events bcs adventurer moving")
        return

    log_debug_full(f"key pressed: {event_info[INPUT_EVENT_INFO_KEY_PRESSED]}")
    # rotate room
    if event_info[INPUT_EVENT_INFO_TYPE] == KEY_X1:
        success = logic.rotate_room(event_info, game_context)
        if success:
            logic.invalidate_adventurer_path(game_context)
    # place treasure
    elif event_info[INPUT_EVENT_INFO_TYPE] == KEY_X2:
        success = logic.place_treasure(event_info, game_context)
        if success:
            logic.invalidate_adventurer_path(game_context)
    # finished turning rooms and stuff
    elif event_info[INPUT_EVENT_INFO_IS_KEY] and event_info[INPUT_EVENT_INFO_KEY_PRESSED] == KEY_SPACE:
        logic.start_moving_adventurer(game_context)

def handle_event_game_player(input_event: InputEventT, game_context: GameContextT):
    """
    only used to manually update player path
    now obsolete
    """
    event_info = input_event_get_info(input_event)
    if event_info[INPUT_EVENT_INFO_TYPE] == None:
        return None

    # draw player movement manually
    if event_info[INPUT_EVENT_INFO_TYPE] == KEY_X1:
        # game_logic.manually_update_player_path(event_info, game_context)
        pass
    # finish dungeon turn
    elif event_info[INPUT_EVENT_INFO_IS_KEY] and event_info[INPUT_EVENT_INFO_KEY_PRESSED] == KEY_SPACE:
        pass

def handle_game_finish(game_context: GameContextT):
    fltk.attend_ev()
    game_context[T_GAME_CTX_GAME_FLAGS] |= F_GAME_EXIT_PROGRAM

def handle_event(game_context: GameContextT):
    """
    Main event dispatcher.
    
    Routes the event to the specific handler function based on the current
    game state stored in `game_context`.
    """
    game_flags: int = game_context[T_GAME_CTX_GAME_FLAGS]

    input_event: InputEventT = game_context[T_GAME_CTX_EVENT]
    event_captured = input_event[T_INPUT_EVENT_TYPE] != None or input_event[T_INPUT_EVENT_DATA] != None

    handle_exit_key(input_event, game_context)

    # check if theres nothing to handle
    # or HANDLE_EVENTS flag is not set
    if not event_captured or not (game_flags & F_GAME_HANDLE_EVENTS):
        return

    log_trace(f"game state: {game_flags}")

    # start menu
    if game_flags & F_GAME_MENU:
        handle_event_start_menu(input_event, game_context)
    # general game event
    if game_flags & F_GAME_GAME:
        handle_event_game(input_event, game_context)
    # dungeon turn event
    if game_flags & F_GAME_TURN_DUNGEON:
        handle_event_game_dungeon(input_event, game_context)
    # game finished event
    if game_flags & F_GAME_GAME_FINISHED:
        handle_game_finish(game_context)
