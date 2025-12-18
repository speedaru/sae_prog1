from types import NoneType

import libs.fltk as fltk
from libs.fltk import FltkEvent, TkEvent

import src.engine.game_logic as game_logic
from src.engine.structs.dungeon import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *
from src.engine.event_info import *
from src.engine.parsing import *

from src.game.game_config import *
from src.game.state_manager import *
from src.game.keys import *

import src.utils.fltk_extensions as fltk_ext
from src.utils.logging import *



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
        # if no dungeon selected ignore event
        if game_event[GAME_EVENT_DATA] == None:
            return

        loaded_game: GameDataT = game_event[GAME_EVENT_DATA]
        game_logic.load_dungeon(game_context, loaded_game[GAME_DATA_DUNGEON])
        game_logic.load_adventurer(game_context, loaded_game[GAME_DATA_ENTITIES][ENTITIES_ADVENTURER])
        game_logic.load_dragons(game_context, loaded_game[GAME_DATA_ENTITIES][ENTITIES_DRAGONS])

        game_context[GAME_CONTEXT_GAME_STATE] = STATE_GAME_TURN_DUNGEON


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
    log_trace("game event, player turn !")

    dungeon: DungeonT = game_context[GAME_CONTEXT_DUNGEON]

    event_info = event_get_info(game_event)
    if event_info[EVENT_INFO_TYPE] == None:
        return None

    log_debug_full(f"key pressed: {event_info[EVENT_INFO_KEY_PRESSED]}")
    # rotate room
    if event_info[EVENT_INFO_TYPE] == KEY_X1:
        game_logic.rotate_room(event_info, game_context)
    # restart dungeon
    elif event_info[EVENT_INFO_IS_KEY] and event_info[EVENT_INFO_KEY_PRESSED] == KEY_R:
        game_logic.reset_game_context(game_context)
    # player finish turn
    elif event_info[EVENT_INFO_IS_KEY] and event_info[EVENT_INFO_KEY_PRESSED] == KEY_SPACE:
        game_context[GAME_CONTEXT_GAME_STATE] = STATE_GAME_TURN_PLAYER

def handle_game_player_event(game_event: GameEventT, game_context: GameContextT):
    event_info = event_get_info(game_event)
    if event_info[EVENT_INFO_TYPE] == None:
        return None

    # draw player movement manually
    if event_info[EVENT_INFO_TYPE] == KEY_X1:
        game_logic.manually_update_player_path(event_info, game_context)
    # restart dungeon
    elif event_info[EVENT_INFO_IS_KEY] and event_info[EVENT_INFO_KEY_PRESSED] == KEY_R:
        game_logic.reset_game_context(game_context)
    # finish dungeon turn
    elif event_info[EVENT_INFO_IS_KEY] and event_info[EVENT_INFO_KEY_PRESSED] == KEY_SPACE:
        game_context[GAME_CONTEXT_GAME_STATE] = STATE_GAME_TURN_DUNGEON
        game_logic.do_dungeon_turn(game_context)

        dungeon: DungeonT = game_context[GAME_CONTEXT_DUNGEON]
        dragons: list[DragonT] = game_context[GAME_CONTEXT_DRAGONS]
        game_logic.move_dragons_randomly(dungeon, dragons)

def handle_game_finish(game_context: GameContextT):
    fltk.attend_ev()
    game_context[GAME_CONTEXT_GAME_STATE] = STATE_EXIT

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

    log_trace(f"game state: {game_state}")

    # start menu
    if game_state == STATE_MENU_START:
        handle_start_menu_event(game_event, game_context)
    elif game_state == STATE_GAME_TURN_PLAYER:
        handle_game_player_event(game_event, game_context)
    elif game_state == STATE_GAME_TURN_DUNGEON:
        handle_game_dungeon_event(game_event, game_context)
    elif game_state == STATE_GAME_DONE_LOST or game_state == STATE_GAME_DONE_WON:
        handle_game_finish(game_context)
