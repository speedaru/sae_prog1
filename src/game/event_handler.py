from types import NoneType

import libs.fltk as fltk
from libs.fltk import FltkEvent, TkEvent

import src.engine.game_logic as game_logic
from src.engine.structs.dungeon import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *
from src.engine.event_info import *

from src.game.game_config import *
from src.game.state_manager import *
from src.game.keys import *

import src.utils.fltk_extensions as fltk_ext
from src.utils.logging import *


# -------------------- FUNCTIONS --------------------
def handle_room_rotation(ev: FltkEvent, dungeon: DungeonT):
    # rotate rooms
    click_postion: tuple[int, int] = fltk_ext.position_souris(ev)

    clicked_room = dungeon_get_room_from_pos(dungeon, click_postion)
    if clicked_room == None:
        log_debug("room selected is OOB")
        return

    # rotate room at click positons
    dungeon_rotate_room(dungeon, clicked_room[0], clicked_room[1])


# -------------------- GENERAL EVENT HANDLERS --------------------
def handle_start_menu_event(game_event: GameEventT, game_context: GameContextT):
    """
    Handles events occurring while in the Start Menu state.
    
    Specifically, it listens for a Left Click (KEY_X1) that carries a selected 
    dungeon in its data payload. If a dungeon is selected, it updates the 
    game context to transition to the playing state.

    Args:
        game_event (GameEventT): The event structure containing type and data.
        game_context (GameContextT): The global game context to update.
    """
    event_info = event_get_info(game_event)
    if event_info[EVENT_INFO_TYPE] == None:
        return None

    if event_info[EVENT_INFO_TYPE] == KEY_X1:
        selected_dungeon: DungeonT | NoneType = game_event[GAME_EVENT_DATA]

        # if no dungeon selected ignore event
        if selected_dungeon == None:
            return

        game_context[GAME_CONTEXT_DUNGEON] = selected_dungeon
        game_context[GAME_CONTEXT_GAME_STATE] = STATE_GAME_TURN_DUNGEON
        log_event_trace(f"seted dungeon: {game_context[GAME_CONTEXT_DUNGEON]}")

def handle_game_dungeon_event(game_event: GameEventT, game_context: GameContextT):
    """
    Handles events occurring during the Dungeons's Turn (player controls dungeon).
    
    Processes:
    - Left Clicks: To rotate rooms in the dungeon.
    - Keyboard 'R': To restart or debug (depends on implementation).
    - Keyboard 'Space': To end turn.

    Args:
        game_event (GameEventT): The current game event.
        game_context (GameContextT): The game context containing the dungeon.
    """
    log_event_trace("game event, player turn !")

    dungeon: DungeonT = game_context[GAME_CONTEXT_DUNGEON]

    event_info = event_get_info(game_event)
    if event_info[EVENT_INFO_TYPE] == None:
        return None

    log_debug_full(f"key pressed: {event_info[EVENT_INFO_KEY_PRESSED]}")
    # rotate room
    if event_info[EVENT_INFO_TYPE] == KEY_X1:
        game_logic.rotate_room(event_info, game_context)
    # player finish turn
    elif event_info[EVENT_INFO_IS_KEY] and event_info[EVENT_INFO_KEY_PRESSED] == KEY_SPACE:
        game_context[GAME_CONTEXT_GAME_STATE] = STATE_GAME_TURN_DUNGEON
    # restart dungeon
    elif event_info[EVENT_INFO_IS_KEY] and event_info[EVENT_INFO_KEY_PRESSED] == KEY_R:
        log_debug("'R' presse")

def handle_game_player_event(game_event: GameEventT, game_context: GameContextT):
    event_info = event_get_info(game_event)
    if event_info[EVENT_INFO_TYPE] == None:
        return None

    # draw player movement manually
    if event_info[EVENT_INFO_TYPE] == KEY_X1:
        game_logic.manually_update_player_path(event_info, game_context)
    # finish dungeon turn
    elif event_info[EVENT_INFO_IS_KEY] and event_info[EVENT_INFO_KEY_PRESSED] == KEY_SPACE:
        game_logic.do_dungeon_turn(game_context)
        game_context[GAME_CONTEXT_GAME_STATE] = STATE_GAME_TURN_PLAYER

def handle_event(game_event: GameEventT, game_context: GameContextT):
    """
    Main event dispatcher.
    
    Routes the event to the specific handler function based on the current
    game state stored in `game_context`.

    Args:
        game_event (GameEventT): The event to handle.
        game_context (GameContextT): The state of the game.
    """
    game_state = game_context[GAME_CONTEXT_GAME_STATE]

    if fltk.touche_pressee(EXIT_KEY):
        game_context[GAME_CONTEXT_GAME_STATE] = STATE_EXIT
        return

    log_debug_full(f"game state: {game_state}")
    if game_state == STATE_MENU_START:
        handle_start_menu_event(game_event, game_context)
    elif game_state == STATE_GAME_TURN_PLAYER:
        handle_game_player_event(game_event, game_context)
    elif game_state == STATE_GAME_TURN_DUNGEON:
        handle_game_dungeon_event(game_event, game_context)
