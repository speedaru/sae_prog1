from tkinter import PhotoImage

import libs.fltk as fltk
from libs.fltk import FltkEvent

from src.config import *
from src.utils.logging import log_release, log_debug, log_debug_full

import src.engine.engine_config as engine_config
from src.engine.asset_manager import *
# import src.engine.fps_manager as fps_manager
from src.engine.structs.dungeon import *

import src.game.game_config as game_config
import src.game.gui as gui
import src.game.start_menu as start_menu
import src.game.event_handler as event_handler
from src.game.


def render_start_menu(current_dungeon: DungeonT):
    selected_dungeon: DungeonT | NoneType = start_menu.render()
    print(f"selected dungeon type: {type(selected_dungeon)}")

    # if no dungeon selected
    if isinstance(selected_dungeon, NoneType):
        return

    # set dungeon that was selected (clicked)
    print("seted dungeon")
    current_dungeon = selected_dungeon

def render_dungeon(dungeon: DungeonT):
    # don't render if NoneType or no rows
    if isinstance(dungeon, NoneType) or len(dungeon) == 0:
        return
    
    dungeon_render(dungeon)

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


def render(current_dungeon: DungeonT):
    # if no dungeon selected then render the start_menu, otherwise render the dungeon
    if isinstance(current_dungeon, NoneType):
        render_start_menu(current_dungeon)
    else:
        render_dungeon(current_dungeon)


def main_loop():
    # globals
    blocks: list[BlockT] | list[NoneType] = list()
    current_dungeon: DungeonT = DungeonT()
    game_state = STATE_

    # init stuff
    window_title = "Wall Is You"
    window_icon_file: str = os.path.join(ASSETS_DIR, "game_icon.ico")
    gui.create_window(window_title, window_icon_file)

    if not asset_manager_initialized(blocks):
        asset_manager_init(blocks)

    input_event: FltkEvent | NoneType = None
    while True:
        gui.start_render()
        render(current_dungeon)
        gui.render()

        input_event = fltk.attend_ev()

        # exit game
        if fltk.touche_pressee(game_config.EXIT_KEY):
            return

        # event_handler.handle_input(input_event)
