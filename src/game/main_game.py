from tkinter import PhotoImage

import libs.fltk as fltk
from libs.fltk import FltkEvent

from src.config import *
from src.utils.logging import log_release, log_debug, log_debug_full

import src.engine.engine_config as engine_config
from src.engine.asset_manager import *
# import src.engine.fps_manager as fps_manager
from src.engine.structs.dungeon import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *

import src.game.gui as gui
import src.game.start_menu as start_menu
import src.game.event_handler as event_handler
from src.game.state_manager import *
from src.game.game_config import *


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

    dungeon: DungeonT = game_context[GAME_CONTEXT_DUNGEON]
    adventurer: AdventurerT = game_context[GAME_CONTEXT_ADVENTURER]
    dragons: list[DragonT] = game_context[GAME_CONTEXT_DRAGONS]

    # render dungeon
    if dungeon != None:
        log_debug_full("rendering dungeon: {dungeon_get_width(dungeon)}x{dungeon_get_height(dungeon)}")
        dungeon_render(dungeon, assets)
    else:
        log_error("cant render dungeon because dungeon is None")

    # render adventurer
    if adventurer != None:
        log_debug_full(f"rendering adventurer: level: room_pos: {adventurer[ADVENTURER_ROOM_POS]} {adventurer[ADVENTURER_LEVEL]}")
        adventurer_render(adventurer, assets)
    else:
        log_error("cant render adventurer because adventurer is None")

    # render dragons
    if dragons != None:
        log_debug_full(f"rendering dragons: {dragons}")
        for dragon in dragons:
            dragon_render(dragon, assets)
    else:
        log_error("cant render dragons because dragons is None")


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
    elif game_state == STATE_GAME_TURN_PLAYER:
        dragons: list[DragonT] = game_context[GAME_CONTEXT_DRAGONS] 

        # initialize dragons if none
        if len(dragons) == 0:
            dungeon: DungeonT = game_context[GAME_CONTEXT_DUNGEON]
            assert(len(dungeon) > 0) # make sure dungeon is not empty

            dungeon_size = (len(dungeon), len(dungeon[0]))
            dragon_create_dragons(dragons, dungeon_size)

        render_game(game_context)

    return event_data


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
    # globals
    assets: AssetsT = list()
    current_dungeon: DungeonT = DungeonT()
    adventurer: AdventurerT = AdventurerT()
    dragons: list[DragonT] = list[DragonT]()
    game_state = STATE_MENU_START
    game_context: GameContextT = [None] * GAME_CONTEXT_COUNT

    # init stuff
    window_title = "Wall Is You"
    window_icon_file: str = os.path.join(ASSETS_DIR, "game_icon.ico")
    gui.create_window(window_title, window_icon_file)

    if not asset_manager_initialized(assets):
        assets = asset_manager_init()

    # create adventurer
    adventurer_init(adventurer)
    
    # init game event
    game_event: GameEventT | NoneType = [None] * GAME_EVENT_COUNT

    # init game context
    game_context[GAME_CONTEXT_ASSETS] = assets
    game_context[GAME_CONTEXT_GAME_STATE] = game_state
    game_context[GAME_CONTEXT_EVENT] = game_event
    game_context[GAME_CONTEXT_DUNGEON] = current_dungeon
    game_context[GAME_CONTEXT_ADVENTURER] = adventurer
    game_context[GAME_CONTEXT_DRAGONS] = dragons

    while True:
        # get event
        event_type: FltkEvent | NoneType = fltk.donne_ev()
        game_event[GAME_EVENT_TYPE] = event_type

        # render
        gui.start_render()

        # pass event to render function so it can send back event_data
        event_data: GameEventDataT = render(game_context)

        gui.render()

        # exit game if exit key pressed
        if fltk.touche_pressee(EXIT_KEY):
            return

        # handle event only if there is event to handle
        if not isinstance(event_type, NoneType):
            game_event[GAME_EVENT_DATA] = event_data

            event_handler.handle_event(game_event, game_context)
