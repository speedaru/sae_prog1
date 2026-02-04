import src.game.hud as hud
import src.game.start_menu as start_menu
import src.game.random_dungeon_selector as random_dungeon_selector
from src.game.game_definitions import *


def render_start_menu(game_context: GameContextT) -> GameEventDataT | NoneType:
    # get event data
    selected_dungeon: DungeonT | NoneType = start_menu.render(game_context)

    return selected_dungeon

def render_random_dungeon_selector(game_context: GameContextT) -> GameEventDataT | NoneType:
    pass

def render_game(game_context: GameContextT):
    assets: AssetsT = game_context[T_GAME_CTX_ASSETS]
    game_data: GameDataT = game_context[T_GAME_CTX_GAME_DATA]
    entity_system: EntitySystemT = game_data[T_DUNGEON_DATA_ENTITY_SYSTEM]

    dungeon: DungeonT = game_data[T_DUNGEON_DATA_DUNGEON]

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
    game_flags: int = game_context[T_GAME_CTX_GAME_FLAGS]
    window: WindowE = game_context[T_GAME_CTX_ACTIVE_WINDOW]

    event_data: GameEventDataT = None

    # if no dungeon selected then render the start_menu, otherwise render the dungeon
    if window == E_WINDOW_START:
        event_data = render_start_menu(game_context)
    # render game normally
    elif window == E_WINDOW_GAME:
        render_game(game_context)
        # render game end menu if game ended
        if game_flags & F_GAME_GAME_FINISHED:
            event_data = render_game_end(game_context)
    elif window == E_WINDOW_RANDOM_DUNGEON:
        event_data = random_dungeon_selector.render(game_context)

    return event_data

