import libs.fltk as fltk

from src.engine.structs.dungeon import *

from src.game.game_definitions import *


# enum
UIAnchorE = int
E_UI_ANCHOR_LEFT = 0x1
E_UI_ANCHOR_TOP = 0x2
E_UI_ANCHOR_RIGHT = 0x4
E_UI_ANCHOR_BOTTOM = 0x8
E_UI_ANCHOR_TOP_LEFT = E_UI_ANCHOR_TOP | E_UI_ANCHOR_LEFT
E_UI_ANCHOR_TOP_RIGHT = E_UI_ANCHOR_TOP | E_UI_ANCHOR_RIGHT
E_UI_ANCHOR_BOTTOM_LEFT = E_UI_ANCHOR_BOTTOM | E_UI_ANCHOR_LEFT
E_UI_ANCHOR_BOTTOM_RIGHT = E_UI_ANCHOR_BOTTOM | E_UI_ANCHOR_RIGHT

DEFAULT_FONT_SIZE = 18


def get_center() -> ScreenPosT:
    return (g_window_size[0] // 2, g_window_size[1] // 2)

def get_center_x() -> int:
    return g_window_size[0] // 2

def get_center_y() -> int:
    return g_window_size[1] // 2

def calculate_center(item_size: ScreenPosT) -> ScreenPosT:
    return get_center_x() - (item_size[0] // 2), get_center_y() - (item_size[1] // 2)

def calculate_center_x(item_width: int) -> int:
    return get_center_x() - (item_width // 2)

def calculate_center_y(item_height: int) -> int:
    return get_center_y() - (item_height // 2)

def calculate_text_size(text: str, size: int = DEFAULT_FONT_SIZE) -> ScreenPosT:
    return fltk.taille_texte(text, taille=size)

def calculate_text_center(text: str, size: int = DEFAULT_FONT_SIZE) -> ScreenPosT:
    return calculate_center(calculate_text_size(text, size))

def calculate_text_center_x(text: str, size: int = DEFAULT_FONT_SIZE) -> int:
    return calculate_center_x(calculate_text_size(text, size)[0])

def calculate_text_center_y(text: str, size: int = DEFAULT_FONT_SIZE) -> int:
    return calculate_center_y(calculate_text_size(text, size)[1])

def anchor_item(anchor_pos: UIAnchorE, item_size: ScreenPosT, padding: int) -> ScreenPosT:
    item_w, item_h = item_size
    screen_w, screen_h = g_window_size
    x, y = 0, 0
    
    # horizontal calculation
    # check if both are set
    if (anchor_pos & E_UI_ANCHOR_LEFT) and (anchor_pos & E_UI_ANCHOR_RIGHT):
        x = (screen_w - item_w) // 2
    elif anchor_pos & E_UI_ANCHOR_LEFT:
        x = padding
    elif anchor_pos & E_UI_ANCHOR_RIGHT:
        x = screen_w - item_w - padding

    # vertical calculation
    # check if both are set
    if (anchor_pos & E_UI_ANCHOR_TOP) and (anchor_pos & E_UI_ANCHOR_BOTTOM):
        y = (screen_h - item_h) // 2
    elif anchor_pos & E_UI_ANCHOR_TOP:
        y = padding
    elif anchor_pos & E_UI_ANCHOR_BOTTOM:
        y = screen_h - item_h - padding

    return (x, y)

def anchor_text(anchor_pos: UIAnchorE, text: str, size: int = DEFAULT_FONT_SIZE, padding: int = 8) -> ScreenPosT:
    return anchor_item(anchor_pos, calculate_text_size(text, size), padding)
