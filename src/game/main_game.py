import time

import libs.fltk as fltk
from libs.fltk import FltkEvent

from src.config import *
from src.engine.engine_config import *
from src.utils.logging import log_release, log_debug, log_debug_full

import src.engine.engine_config as engine_config
import src.engine.fps_manager as fps_manager
import src.game.logic as logic
from src.engine.asset_manager import *
from src.engine.fps_manager import T_FPS_MANAGER_LAST_FRAME_TIME, T_FPS_MANAGER_CURRENT_FRAME_TIME
from src.engine.structs.dungeon import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *
from src.engine.structs.treasure import *
from src.engine.structs.strong_sword import *
from src.engine.parsing import *

import src.game.gui as gui
import src.game.start_menu as start_menu
import src.game.event_handler as event_handler
import src.game.hud as hud
from src.game.state_manager import *
from src.game.game_definitions import *


def render_start_menu(game_context: GameContextT) -> GameEventDataT | NoneType:
    """
    Renders the start menu and handles the dungeon selection logic.

    Delegates the rendering and interaction handling to the `start_menu` module.

    Args:
        game_context (GameContextT): The global game context containing assets and events.

    Returns:
        GameEventDataT | NoneType: Returns the selected Dungeon structure if a choice is made,
                                   otherwise returns None.
    """
    # get event data
    selected_dungeon: DungeonT | NoneType = start_menu.render(game_context)

    return selected_dungeon

def render_game(game_context: GameContextT):
    """
    Renders the main game screen (dungeon, characters, entities).

    It retrieves the game state (dungeon, adventurer, dragons) from the context
    and calls the respective render functions for each component.

    Args:
        game_context (GameContextT): The global game context.
    """
    assets: AssetsT = game_context[T_GAME_CTX_ASSETS]
    game_data: GameDataT = game_context[T_GAME_CTX_GAME_DATA]
    entity_system: EntitySystemT = game_data[T_GAME_DATA_ENTITY_SYSTEM]

    dungeon: DungeonT = game_data[T_GAME_DATA_DUNGEON]

    # render dungeon
    if dungeon:
        log_debug_full("rendering dungeon: {dungeon_get_width(dungeon)}x{dungeon_get_height(dungeon)}")
        dungeon_render(dungeon, assets)

    # render entities
    if entity_system != None:
        log_debug_full("rendering entities . . .")
        entity_system_render(entity_system, assets)

    # render hud
    hud_elements = hud.get_hud_elements(game_context)
    hud.render_hud_elements(hud_elements)

def render_game_end(game_context: GameContextT):
    GAME_END_MESSAGE_FONT_SIZE = 48
    game_state: GameFlags = game_context[T_GAME_CTX_GAME_FLAGS]

    message = ""
    message_color = ""
    if game_state & F_GAME_GAME_WON:
        message = "Partie gagnée !"
        message_color = "lime"
    elif game_state & F_GAME_GAME_LOST:
        message = "Partie perdue"
        message_color = "red"

    message_size = fltk.taille_texte(message, taille=GAME_END_MESSAGE_FONT_SIZE)
    message_size = fltk.taille_texte(message, taille=GAME_END_MESSAGE_FONT_SIZE)
    center_x, center_y = (WINDOW_SIZE[0] / 2) - (message_size[0] / 2), (WINDOW_SIZE[1] / 2) - (message_size[1] / 2)
    fltk.texte(center_x, center_y - 50, message, couleur=message_color, taille=GAME_END_MESSAGE_FONT_SIZE)

    # so it calls event handler to then update game state to STATE_EXIT
    return game_state

def render(game_context: GameContextT) -> GameEventDataT:
    """
    Main rendering dispatcher.

    Switches between rendering the Start Menu or the Active Game based on the
    current game state (`GAME_CONTEXT_GAME_STATE`).
    
    It also handles just-in-time initialization of game elements like dragons
    when transitioning to the player turn.

    Args:
        game_context (GameContextT): The global game context.

    Returns:
        GameEventDataT: Any data resulting from the render step (e.g., selected dungeon),
                        passed back to the event handler.
    """
    game_flags: int = game_context[T_GAME_CTX_GAME_FLAGS]

    event_data: GameEventDataT = None

    # if no dungeon selected then render the start_menu, otherwise render the dungeon
    if game_flags & F_GAME_MENU:
        event_data = render_start_menu(game_context)
    # render game normally
    elif game_flags & F_GAME_GAME:
        render_game(game_context)
        # render game end menu if game ended
        if game_flags & F_GAME_GAME_FINISHED:
            event_data = render_game_end(game_context)

    return event_data

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
                                            game_flags=GAME_FLAGS_STARTUP_FLAGS,
                                            event=game_event_create(),
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
            game_context[T_GAME_CTX_EVENT] = game_event_create(event_type=event_type)    

        # render
        # pass event to render function so it can send back event_data
        gui.start_render()
        event_data: GameEventDataT = render(game_context)
        gui.render()

        # handle event if there is one
        if game_context[T_GAME_CTX_GAME_FLAGS] & F_GAME_HANDLE_EVENTS:
            game_context[T_GAME_CTX_EVENT][T_GAME_EVENT_DATA] = event_data

        # call event handler
        event_handler.handle_event(game_context)

        # handle specific game logic every frame
        logic.handle_logic(game_context)

        # fps
        fps_mgr[T_FPS_MANAGER_LAST_FRAME_TIME] = fps_mgr[T_FPS_MANAGER_CURRENT_FRAME_TIME]
        fps_manager.sleep_to_cap_fps(dt)
        log_fps(f"fps: {fps_manager.calculate_fps(dt)}")
