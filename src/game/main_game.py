import time

import libs.fltk as fltk
from libs.fltk import FltkEvent

from src.config import *
from src.engine.engine_config import *
from src.utils.logging import log_release, log_debug, log_debug_full

import src.engine.engine_config as engine_config
import src.engine.fps_manager as fps_manager
import src.engine.renderer as renderer
from src.engine.asset_manager import *
from src.engine.fps_manager import T_FPS_MANAGER_LAST_FRAME_TIME, T_FPS_MANAGER_CURRENT_FRAME_TIME
from src.engine.structs.dungeon import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *
from src.engine.structs.treasure import *
from src.engine.structs.strong_sword import *
from src.engine.parsing import *

import src.game.gui as gui
import src.game.event_handler as event_handler
import src.game.logic as logic
from src.game.state_manager import *
from src.game.game_definitions import *


def main_loop():
    """
    The main entry point and loop of the game application.
    """
    fps_mgr = fps_manager.fps_manager_create()

    # globals
    assets: AssetsT = list()

    # init stuff
    window_title = "Wall Is You"
    window_icon_file: str = os.path.join(ASSETS_DIR, "game_icon.ico")
    gui.create_window(window_title, window_icon_file)

    # init assets
    if not asset_manager_initialized(assets):
        assets = asset_manager_init()

    # init game context
    game_context: Any = game_context_create(assets=assets,
                                            game_flags=GAME_FLAGS_STARTUP,
                                            active_window=E_WINDOW_START,
                                            event=input_event_create(),
                                            game_data=game_data_init(),
                                            original_game_data=game_data_init(),
                                            fps_manager=fps_mgr)

    # while EXIT_PROGRAM flag is not set
    while not (game_context[T_GAME_CTX_GAME_FLAGS] & F_GAME_EXIT_PROGRAM):
        # handle fps cap and delta time
        ctime = time.time()
        dt = fps_manager.calculate_delta_time(ctime, fps_mgr[T_FPS_MANAGER_LAST_FRAME_TIME])
        fps_mgr[T_FPS_MANAGER_CURRENT_FRAME_TIME] = ctime

        # get event before rendering bcs we might use it in render fn
        if game_context[T_GAME_CTX_GAME_FLAGS] & F_GAME_HANDLE_EVENTS:
            event_type: FltkEvent | NoneType = fltk.donne_ev()
            game_context[T_GAME_CTX_EVENT] = input_event_create(event_type=event_type)    

        # render
        # pass event to render function so it can send back event_data
        gui.start_render()
        event_data: GameEventDataT = renderer.render(game_context)
        gui.render()

        # handle event if there is one
        if game_context[T_GAME_CTX_GAME_FLAGS] & F_GAME_HANDLE_EVENTS:
            game_context[T_GAME_CTX_EVENT][T_INPUT_EVENT_DATA] = event_data

        # call event handler
        event_handler.handle_event(game_context)

        # handle specific game logic every frame
        logic.handle_logic(game_context)

        # fps
        fps_mgr[T_FPS_MANAGER_LAST_FRAME_TIME] = fps_mgr[T_FPS_MANAGER_CURRENT_FRAME_TIME]
        fps_manager.sleep_to_cap_fps(dt)
        log_fps(f"fps: {fps_manager.calculate_fps(dt)}")
