from types import NoneType

import libs.fltk as fltk
from libs.fltk import FltkEvent

from src.engine.structs.dungeon import *

from src.game.game_config import *
from src.game.state_manager import *
from src.game.keys import *

import src.utils.fltk_extensions as fltk_ext
from src.utils.logging import *


def handle_start_menu_event(game_event: GameEventT, game_context: GameContextT):
    ev = game_event[GAME_EVENT_TYPE]

    
    if fltk.type_ev(ev) == KEY_X1:
        selected_dungeon: DungeonT | NoneType = game_event[GAME_EVENT_DATA]

        # if no dungeon selected ignore event
        if selected_dungeon == None:
            return

        game_context[GAME_CONTEXT_DUNGEON] = selected_dungeon
        game_context[GAME_CONTEXT_GAME_STATE] = STATE_GAME_TURN_PLAYER
        log_event_trace(f"seted dungeon: {game_context[GAME_CONTEXT_DUNGEON]}")

def handle_normal_game_event(game_event: GameEventT, game_context: GameContextT):
    log_event_trace("game event !")

    ev = game_event[GAME_EVENT_TYPE]
    ev_type: str | NoneType = fltk.type_ev(ev)
    if ev_type == None:
        return

    ev_is_key = ev_type.lower() == "touche"
    key_pressed = None
    if ev_is_key:
        key_pressed = ev[fltk_ext.FLTK_EVENT_TK_EVENT].keysym.lower()

    log_debug(f"key pressed: {key_pressed}")
    if ev_type == KEY_X1:
        # rotate rooms
        click_postion = fltk_ext.position_souris(ev)

        # rotate room at click positons
        clicked_room_col = click_postion[0] // BLOCK_SCALED_SIZE[0]
        clicked_room_row = click_postion[1] // BLOCK_SCALED_SIZE[1]

        # if cursor outside of dungeon do nothing
        dungeon: DungeonT = game_context[GAME_CONTEXT_DUNGEON]
        if clicked_room_col >= dungeon_get_width(dungeon) or clicked_room_row >= dungeon_get_height(dungeon):
            return False

        dungeon_rotate_room(dungeon, clicked_room_row, clicked_room_col)
    elif ev_is_key and key_pressed == KEY_SPACE:
        log_debug("espace presse")
    elif ev_is_key and key_pressed == KEY_R:
        log_debug("'R' presse")

def handle_event(game_event: GameEventT, game_context: GameContextT):
    game_state = game_context[GAME_CONTEXT_GAME_STATE]

    log_debug_full(f"game state: {game_state}")
    if game_state == STATE_MENU_START:
        handle_start_menu_event(game_event, game_context)
    elif game_state == STATE_GAME_TURN_PLAYER:
        handle_normal_game_event(game_event, game_context)
