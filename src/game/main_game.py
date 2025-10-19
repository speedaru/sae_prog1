import time

from src.config import *
import libs.fltk as fltk
from src.utils.logging import log_release, log_debug, log_debug_full

from src.engine.asset_manager import *
import src.engine.engine_config as engine_config
import src.engine.fps_manager as fps_manager
from src.engine.structs.dungeon import *

import src.game.game_config as game_config
import src.game.gui as gui
import src.game.start_menu as start_menu


current_dungeon: DungeonT | NoneType = None


def render_start_menu():
    global current_dungeon

    selected_dungeon: DungeonT | NoneType = start_menu.render()

    # if no dungeon selected
    if selected_dungeon == None:
        return

    # set dungeon that was selected (clicked)
    current_dungeon = selected_dungeon

def render_dungeon(dungeon: DungeonT):
    # only render if not NoneType and at least 1 row
    if not isinstance(dungeon, NoneType) and len(dungeon) > 0:
        dungeon_render(dungeon)

def render():
    global current_dungeon

    if not asset_manager_initialized():
        asset_manager_init()

    # if no dungeon selected then render the start_menu, otherwise render the dungeon
    if isinstance(current_dungeon, NoneType):
        render_start_menu()
    else:
        render_dungeon(current_dungeon)


def main_loop():
    last_frame_start: float = 0

    fps_interval_s: float = fps_manager.get_target_fps_interval_ms(engine_config.TARGET_FPS) / 1000
    log_debug_full(f"target fps interval ms: {fps_interval_s}")

    # dungeon: DungeonT = DungeonT()
    #
    # # dungeon_file_name = "dungeon_easy.txt"
    # dungeon_file_name = "dungeon_hard.txt"
    # if not dungeon_parse_file(os.path.join(DUNGEON_FILES_DIR, dungeon_file_name), dungeon):
    #     log_release(f"[main_loop] failed to parse {dungeon_file_name}")
    #
    # dungeon_print_values(dungeon)

    window_title = "Wall Is You"
    window_icon_file = os.path.join(ASSETS_DIR, "game_icon.ico")
    gui.create_window(window_title, window_icon_file)

    while True:
        last_frame_start = fps_manager.get_ctime_ms()

        # exit game
        if fltk.touche_pressee(game_config.EXIT_KEY):
            break

        gui.start_render()
        render()
        gui.render()

        time.sleep(fps_interval_s)
        log_debug(f"fps: {fps_manager.get_fps_count(last_frame_start)}")
