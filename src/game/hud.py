from src.engine.structs.hud_element import *

from src.game.game_definitions import *
from src.game.state_manager import *

import src.utils.gui_geom as gui_geom
from src.utils.gui_geom import UIAnchorE


# returns y size of added element
def _add_hud_element(hud_elements: list[HudElementT],
                     anchor: UIAnchorE,
                     text: str,
                     color: str,
                     current_offset_y: int) -> int:
    pos = gui_geom.anchor_text(anchor, text)
    pos = (pos[0], pos[1] + current_offset_y)
    hud_elements.append(hud_element_create(pos, color=color, text=text))

    return gui_geom.calculate_text_size(text)[1]

def get_hud_elements(game_context: GameContextT) -> list[HudElementT]:
    game_data: GameDataT = game_context[GAME_CONTEXT_GAME_DATA]
    hud_elements: list[HudElementT] = []

    Y_PAD = 6

    top_right_offset_y = 0
    top_left_offset_y = 0
    bottom_right_offset_y = 0
    bottom_left_offset_y = 0

    # game state info
    text = get_game_state_text(game_context[GAME_CONTEXT_GAME_STATE])
    el_height = _add_hud_element(hud_elements, gui_geom.E_UI_ANCHOR_TOP_LEFT, text, "lime", top_left_offset_y)
    top_left_offset_y += el_height + Y_PAD

    # indicate game mode
    text = f"Mode de jeu: {get_game_mode_text(game_data[GAME_DATA_GAME_MODE])}"
    el_height = _add_hud_element(hud_elements, gui_geom.E_UI_ANCHOR_BOTTOM_LEFT, text, "yellow", bottom_left_offset_y)
    bottom_left_offset_y -= el_height - Y_PAD

    # indicate which round we're on
    text = f"Tour: {game_data[GAME_DATA_ROUND]}"
    el_height = _add_hud_element(hud_elements, gui_geom.E_UI_ANCHOR_TOP_LEFT, text, "white", top_left_offset_y)
    top_left_offset_y += el_height + Y_PAD

    return hud_elements

def render_hud_elements(hud_elements: list[HudElementT]):
    for hud_el in hud_elements:
        hud_element_render(hud_el)
