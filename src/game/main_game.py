import time

import libs.fltk as fltk
from libs.fltk import FltkEvent

from src.config import *
from src.engine.engine_config import *
from src.utils.logging import log_release, log_debug, log_debug_full

import src.engine.engine_config as engine_config
import src.engine.fps_manager as fps_manager
import src.engine.game_logic as game_logic
from src.engine.asset_manager import *
from src.engine.structs.dungeon import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *
from src.engine.structs.treasure import *
from src.engine.parsing import *

import src.game.gui as gui
import src.game.start_menu as start_menu
import src.game.event_handler as event_handler
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
    assets: AssetsT = game_context[GAME_CONTEXT_ASSETS]

    dungeon: DungeonT = game_context[GAME_CONTEXT_GAME_DATA][GAME_DATA_DUNGEON]
    adventurer: AdventurerT = game_context[GAME_CONTEXT_GAME_DATA][GAME_DATA_ENTITIES][ENTITIES_ADVENTURER]
    dragons: list[DragonT] = game_context[GAME_CONTEXT_GAME_DATA][GAME_DATA_ENTITIES][ENTITIES_DRAGONS]
    treasure: TreasureT = game_context[GAME_CONTEXT_GAME_DATA][GAME_DATA_ENTITIES][ENTITIES_TREASURE]

    # render dungeon
    if dungeon != None:
        log_debug_full("rendering dungeon: {dungeon_get_width(dungeon)}x{dungeon_get_height(dungeon)}")
        dungeon_render(dungeon, assets)
    else:
        log_error("cant render dungeon because dungeon is None")

    # render adventurer
    if adventurer != None:
        log_debug_full(f"rendering adventurer: level: room_pos: {adventurer[ENTITY_ROOM_POS]} {adventurer[ENTITY_LEVEL]}")
        adventurer_render(adventurer, assets)
        adventurer_render_path(adventurer)
    else:
        log_error("cant render adventurer because adventurer is None")

    # render dragons
    if dragons != None:
        log_debug_full(f"rendering dragons: {dragons}")
        for dragon in dragons:
            dragon_render(dragon, assets)
    else:
        log_error("cant render dragons because dragons is None")

    # render treasure
    if treasure != None:
        log_debug_full(f"rendering treasure: {treasure}")
        treasure_render(treasure, assets)

def render_game_end(game_context: GameContextT):
    GAME_END_MESSAGE_FONT_SIZE = 48
    game_state: GameStateT = game_context[GAME_CONTEXT_GAME_STATE]

    message = ""
    message_color = ""
    if game_state == STATE_GAME_DONE_WON:
        message = "Partie gagnée !"
        message_color = "lime"
    elif game_state == STATE_GAME_DONE_LOST:
        message = "Partie perdue"
        message_color = "red"

    message_size = fltk.taille_texte(message, taille=GAME_END_MESSAGE_FONT_SIZE)
    message_size = fltk.taille_texte(message, taille=GAME_END_MESSAGE_FONT_SIZE)
    center_x, center_y = (WINDOW_SIZE[0] / 2) - (message_size[0] / 2), (WINDOW_SIZE[1] / 2) - (message_size[1] / 2)
    fltk.texte(center_x, center_y, message, couleur=message_color, taille=GAME_END_MESSAGE_FONT_SIZE)

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
    game_state = game_context[GAME_CONTEXT_GAME_STATE]

    event_data: GameEventDataT = None

    # if no dungeon selected then render the start_menu, otherwise render the dungeon
    if game_state == STATE_MENU_START:
        event_data = render_start_menu(game_context)
    elif game_state == STATE_GAME_TURN_PLAYER or game_state == STATE_GAME_TURN_DUNGEON:
        render_game(game_context)
    # render game end menu if game ended
    elif game_state == STATE_GAME_DONE_WON or game_state == STATE_GAME_DONE_LOST:
        event_data = render_game_end(game_context)

    # render game state info
    game_state_render(game_context[GAME_CONTEXT_GAME_STATE])

    return event_data

def handle_logic(game_context: GameContextT):
    game_state: GameStateT = game_context[GAME_CONTEXT_GAME_STATE]

    if game_state == STATE_GAME_TURN_PLAYER or game_state == STATE_GAME_TURN_DUNGEON:
        # handle collisions between adventurer and dragons
        game_logic.do_collisions(game_context)


def main_loop():
    """
    The main entry point and loop of the game application.

    Responsibilities:
    1. Initializes the window, assets, and global game context.
    2. Runs the infinite game loop.
    3. Captures FLTK events.
    4. Calls the `render` pipeline.
    5. Dispatches events to the `event_handler`.
    6. Handles the exit condition (Escape key).
    """
    last_update_time_s = time.time()

    # globals
    assets: AssetsT = list()
    game_state = STATE_MENU_START
    game_context: GameContextT = game_context_init()

    # init stuff
    window_title = "Wall Is You"
    window_icon_file: str = os.path.join(ASSETS_DIR, "game_icon.ico")
    gui.create_window(window_title, window_icon_file)

    # init assets
    if not asset_manager_initialized(assets):
        assets = asset_manager_init()

    # init game event
    game_event: GameEventT | NoneType = [None] * GAME_EVENT_COUNT

    # init game context
    game_context[GAME_CONTEXT_ASSETS] = assets
    game_context[GAME_CONTEXT_GAME_STATE] = game_state
    game_context[GAME_CONTEXT_EVENT] = game_event
    game_context[GAME_CONTEXT_GAME_DATA] = game_data_init()
    game_context[GAME_CONTEXT_ORIGINAL_GAME_DATA] = game_data_init()

    while True:
        # handle fps cap and delta time
        ctime = time.time()
        dt = fps_manager.calculate_delta_time(ctime, last_update_time_s)
        last_update_time_s = ctime

        # get event
        event_type: FltkEvent | NoneType = fltk.donne_ev()
        game_event[GAME_EVENT_TYPE] = event_type

        # render
        # pass event to render function so it can send back event_data
        gui.start_render()
        event_data: GameEventDataT = render(game_context)
        gui.render()

        # handle event only if there is event to handle
        if event_type != None or event_data != None:
        # if event_type != None:
            game_event[GAME_EVENT_DATA] = event_data

            event_handler.handle_event(game_event, game_context)

        # handle specific logic every frame
        handle_logic(game_context)

        # end game
        if game_context[GAME_CONTEXT_GAME_STATE] == STATE_EXIT:
            break

        fps_manager.sleep_to_cap_fps(dt)
        # log_debug_full(f"fps: {fps_manager.calculate_fps(dt)}")

