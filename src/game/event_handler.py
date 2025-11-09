from types import NoneType

import libs.fltk as fltk
from libs.fltk import FltkEvent

from src.engine.structs.dungeon import *

from src.game.game_config import *
from src.game.state_manager import *

from src.utils.logging import *


def handle_start_menu_event(game_event: GameEventT, game_context: GameContextT):
    ev = game_event[GAME_EVENT_TYPE]

    
    if fltk.type_ev(ev) == "ClicGauche":
        selected_dungeon: DungeonT = game_event[GAME_EVENT_DATA]
        game_context[GAME_CONTEXT_DUNGEON] = selected_dungeon
        game_context[GAME_CONTEXT_GAME_STATE] = STATE_GAME_DUNGEON
        log_event_trace(f"seted dungeon: {game_context[GAME_CONTEXT_DUNGEON]}")

def handle_normal_game_event(game_event: GameEventT, game_context: GameContextT):
    log_event_trace("game event !")

    ev = game_event[GAME_EVENT_TYPE]

    if fltk.type_ev(ev) == "ClicGauche":
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

def handle_event(game_event: GameEventT, game_context: GameContextT):
    game_state = game_context[GAME_CONTEXT_GAME_STATE]

    log_debug_full(f"game state: {game_state}")
    if game_state == STATE_MENU_START:
        handle_start_menu_event(game_event, game_context)
    elif game_state == STATE_GAME_DUNGEON:
        handle_normal_game_event(game_event, game_context)
