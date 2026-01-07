import libs.fltk as fltk
import src.utils.fltk_extensions as fltk_ext

from src.engine.structs.dungeon import ScreenPosT

from src.utils.gui_geom import DEFAULT_FONT_SIZE


HudElementT = list[ScreenPosT | int | str]

T_HUD_ELEMENT_RENDER_POS = 0
T_HUD_ELEMENT_COLOR = 1 # fltk color like "red", "green"
T_HUD_ELEMENT_SIZE = 2
T_HUD_ELEMENT_TEXT = 3
T_HUD_ELEMENT_COUNT = 4

def hud_element_create(render_pos: ScreenPosT = (0, 0),
                       color: str = "white",
                       size: int = DEFAULT_FONT_SIZE,
                       text: str = "") -> HudElementT:
    hud_element: HudElementT = [HudElementT()] * T_HUD_ELEMENT_COUNT

    hud_element[T_HUD_ELEMENT_RENDER_POS] = render_pos
    hud_element[T_HUD_ELEMENT_COLOR] = color
    hud_element[T_HUD_ELEMENT_SIZE] = size
    hud_element[T_HUD_ELEMENT_TEXT] = text
    
    return hud_element

def hud_element_render(hud_element: HudElementT):
    render_pos: ScreenPosT = hud_element[T_HUD_ELEMENT_RENDER_POS]
    fltk.texte(render_pos[0], render_pos[1],
               hud_element[T_HUD_ELEMENT_TEXT],
               hud_element[T_HUD_ELEMENT_COLOR],
               taille=hud_element[T_HUD_ELEMENT_SIZE])
