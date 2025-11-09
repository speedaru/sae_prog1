from tkinter import PhotoImage

import libs.fltk as fltk
from libs.fltk import FltkEvent

from src.config import *
from src.utils.logging import log_release, log_debug, log_debug_full

import src.engine.engine_config as engine_config
from src.engine.asset_manager import *
# import src.engine.fps_manager as fps_manager
from src.engine.structs.dungeon import *

import src.game.gui as gui
import src.game.start_menu as start_menu
import src.game.event_handler as event_handler
from src.game.state_manager import *
from src.game.game_config import *


def render_start_menu(game_context: GameContextT):
    selected_dungeon: DungeonT | NoneType = start_menu.render()

    # if no dungeon selected
    if isinstance(selected_dungeon, NoneType):
        return

    # set dungeon that was selected (clicked)
    print("seted dungeon")
    game_context[GAME_CONTEXT_DUNGEON] = selected_dungeon
    game_context[GAME_CONTEXT_GAME_STATE] = STATE_GAME_DUNGEON

def render_dungeon(game_context: GameContextT):
    blocks: BlockListT = game_context[GAME_CONTEXT_BLOCKS]
    dungeon: DungeonT = game_context[GAME_CONTEXT_DUNGEON]

    # don't render if NoneType or no rows
    if isinstance(dungeon, NoneType) or dungeon_get_height(dungeon) == 0:
        return
    
    print("rendering dungeon: {dungeon_get_width(dungeon)}x{dungeon_get_height(dungeon)}")
    dungeon_render(blocks, dungeon)

    # # rotate rooms
    # click_postion = fltk.click_gauche()
    # if click_postion == (-1, -1):
    #     return
    #
    # # rotate room at click positons
    # clicked_room_col = click_postion[0] // BLOCK_SCALED_SIZE[0]
    # clicked_room_row = click_postion[1] // BLOCK_SCALED_SIZE[1]
    #
    # # if cursor outside of dungeon do nothing
    # if clicked_room_col >= dungeon_get_width(dungeon) or clicked_room_row >= dungeon_get_height(dungeon):
    #     return False
    # 
    # dungeon_rotate_room(dungeon, clicked_room_row, clicked_room_col)


def render(game_context: GameContextT):
    game_state = game_context[GAME_CONTEXT_GAME_STATE]
    print(f"[render] gamestate: {game_state}")

    # if no dungeon selected then render the start_menu, otherwise render the dungeon
    if game_state == STATE_MENU_START:
        render_start_menu(game_context)
    elif game_state == STATE_GAME_DUNGEON:
        render_dungeon(game_context)


def main_loop():
    # globals
    blocks: list[BlockT] | list[NoneType] = list()
    current_dungeon: DungeonT = DungeonT()
    game_state = STATE_MENU_START
    game_context: GameContextT = [None] * GAME_CONTEXT_COUNT
    print(f"game context size: {len(game_context)}")

    # init stuff
    window_title = "Wall Is You"
    window_icon_file: str = os.path.join(ASSETS_DIR, "game_icon.ico")
    gui.create_window(window_title, window_icon_file)

    if not asset_manager_initialized(blocks):
        blocks = asset_manager_init()

    # init game context
    game_context[GAME_CONTEXT_BLOCKS] = blocks
    game_context[GAME_CONTEXT_GAME_STATE] = game_state
    game_context[GAME_CONTEXT_DUNGEON] = current_dungeon

    input_event: FltkEvent | NoneType = None
    while True:
        gui.start_render()
        render(game_context)
        gui.render()

        input_event = fltk.donne_ev()

        # exit game
        if fltk.touche_pressee(EXIT_KEY):
            return

        event_handler.handle_input(input_event, game_context)
