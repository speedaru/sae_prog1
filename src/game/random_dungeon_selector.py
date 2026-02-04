from dataclasses import asdict

import src.engine.dungeon_generator as dungeon_generator
import libs.fltk as fltk
import src.utils.fltk_extensions as fltk_ext

import src.engine.ui_framework.ui as ui
from src.engine.ui_framework.ui import SizeT, RectT
from src.engine.dungeon_generator import DungeonSettingsT, SettingT

from src.game.game_definitions import *

import src.utils.gui_geom as gui_geom

# settings = {
#     "dungeon_size": SettingT("Dungeon dimensions", SizeT(2, 2), SizeT(0, 0), SizeT(WINDOW_GRID_SIZE[0], WINDOW_GRID_SIZE[1])),
#     "dragon_count": SettingT("Number of dragons", 1, 0, 10),
#     "treasure_count": SettingT("Number of treasures", 2, 0, 10),
#     "strong_sword_count": SettingT("Number of strong swords", 0, 0, 10),
#     "chaos_seal_count": SettingT("Number of chaos seals", 0, 0, 10),
# }
settings = DungeonSettingsT(
        SettingT("Dungeon dimensions", SizeT(6, 6), SizeT(0, 0), SizeT(WINDOW_GRID_SIZE[0], WINDOW_GRID_SIZE[1])),
        SettingT("Number of dragons", 3, 0, 10),
        SettingT("Number of treasures", 2, 0, 10),
        SettingT("Number of strong swords", 0, 0, 10),
        SettingT("Number of chaos seals", 0, 0, 10)
)


FONT_SIZE = 18
TEXT_COLOR = "white"

def _render_arrows(label, y) -> tuple[RectT, RectT]:
    """
    returns rect of left and right arrow
    """
    ARROW_OFFSET = 8
    
    left_arrow = "←"
    right_arrow = "→"

    label_x = gui_geom.calculate_text_center_x(label, FONT_SIZE)
    label_width = fltk.taille_texte(label, taille=FONT_SIZE)[0]

    # left arrow
    left_arrow_size = fltk.taille_texte(left_arrow, taille=FONT_SIZE)
    # ui.button(None, (label_x - ARROW_OFFSET - left_arrow_size[0], y), left_arrow, text_color="black", font_size=FONT_SIZE, outline_size=2, inner_padding=8)
    fltk.texte(label_x - ARROW_OFFSET - left_arrow_size[0], y, left_arrow, taille=FONT_SIZE, couleur=TEXT_COLOR)
    left_arrow_rect = RectT(ui.ScreenPosT(label_x - ARROW_OFFSET - left_arrow_size[0], y), \
            ui.ScreenPosT(label_x - ARROW_OFFSET, y + left_arrow_size[1]))

    # right arrow
    right_arrow_size = fltk.taille_texte(right_arrow, taille=FONT_SIZE)
    # ui.button(None, (label_x + label_width + ARROW_OFFSET, y), right_arrow, text_color="black", font_size=FONT_SIZE, outline_size=2, inner_padding=8)
    fltk.texte(label_x + label_width + ARROW_OFFSET, y, right_arrow, taille=FONT_SIZE, couleur=TEXT_COLOR)
    right_arrow_rect = RectT(ui.ScreenPosT(label_x + label_width + ARROW_OFFSET, y), \
            ui.ScreenPosT(label_x + label_width + ARROW_OFFSET + right_arrow_size[0], y + right_arrow_size[1]))

    return left_arrow_rect, right_arrow_rect

def _handle_arrows(ev, left_arrow_rect: RectT, right_arrow_rect: RectT, setting_name: str):
    left_arrow_pressed = ui.do_button(ev, left_arrow_rect)
    right_arrow_pressed = ui.do_button(ev, right_arrow_rect)

    # settings where setting value is an int
    int_settings = [name for name, setting in asdict(settings).items() if isinstance(setting.val, int)]

    delta = -1 if left_arrow_pressed else 1 if right_arrow_pressed else 0
    if setting_name in int_settings:
        settings.__getattribute__(setting_name).val += delta
    elif setting_name == "dungeon_size":
        val: SizeT = settings.__getattribute__(setting_name).val
        settings.__getattribute__(setting_name).val = SizeT(val.width + delta, val.height + delta)

    setting = settings.__getattribute__(setting_name)
    settings.__getattribute__(setting_name).val = max(setting.min, min(setting.val, setting.max))

def render(game_context: GameContextT) -> GameEventDataT | NoneType:
    BASE_Y = gui_geom.get_center_y() / 2

    # verticall padding is x1.5 text size
    PAD_Y = 1.5 * fltk.taille_texte("blablabla", taille=FONT_SIZE)[1]

    y = BASE_Y

    ev: FltkEvent = game_context[T_GAME_CTX_EVENT][T_INPUT_EVENT_TYPE]

    # draw background
    BACKGROUND_FILE = "start_background.png"
    background_path = os.path.join(ASSETS_DIR, BACKGROUND_FILE)
    fltk.image(0,0,background_path,ancrage="nw")

    # render different settings
    for name, setting in asdict(settings).items():
        text = f"{setting.label} : {setting.val}"

        x = gui_geom.calculate_text_center_x(text, FONT_SIZE)
        fltk.texte(x, y, text, taille=FONT_SIZE, couleur=TEXT_COLOR)

        left_arrow_rect, right_arrow_rect = _render_arrows(text, y)
        _handle_arrows(ev, left_arrow_rect, right_arrow_rect, name)

        y += PAD_Y

    # ok button
    text = "OK"
    pos = (gui_geom.calculate_text_center_x(text, FONT_SIZE), y + 40)
    if ui.button(ev, pos, text, font_size=FONT_SIZE, text_color=TEXT_COLOR, outline_color="yellow", outline_size=2, inner_padding=8):
        dungeon_data = dungeon_generator.generate_dungeon_data(settings)
        dungeon_data[T_DUNGEON_DATA_GAME_MODE] = game_context[T_GAME_CTX_GAME_DATA][T_DUNGEON_DATA_GAME_MODE]
        return dungeon_data

    return None
