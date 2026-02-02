from types import NoneType

import libs.fltk as fltk
import src.utils.fltk_extensions as fltk_ext
from libs.fltk import FltkEvent, taille_texte

import src.utils.geom as geom
from src.utils.gui_geom import DEFAULT_FONT_SIZE


class ScreenPosT:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)

class SizeT:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def is_null(self):
        return self.width == 0 and self.height == 0;

class RectT:
    def __init__(self, tl: ScreenPosT, br: ScreenPosT):
        self.tl = tl
        self.br = br

def button(ev: FltkEvent | NoneType, pos, text: str,
           size = (0, 0), # if 0, size will be auto
           font_size: int = DEFAULT_FONT_SIZE,
           text_color: str | NoneType = "white",
           bg_color: str = "",
           outline_color: str = "black",
           outline_size: int = 0,
           inner_padding: int = 0) -> bool:
    """
    returns true if clicked
    """
    # turn into classes
    pos = ScreenPosT(pos[0], pos[1])
    size = SizeT(size[0], size[1])

    if size.is_null():
        text_size = fltk.taille_texte(text, taille=font_size)
        size = SizeT(text_size[0], text_size[1])

    size.width += inner_padding
    size.height += inner_padding

    rect = RectT(pos, ScreenPosT(pos.x + size.width, pos.y + size.height))
    rect_middle = ScreenPosT((rect.tl.x + rect.br.x) // 2, (rect.tl.y + rect.br.y) // 2)

    if bg_color != "" or outline_size != 0:
        fltk.rectangle(rect.tl.x, rect.tl.y, rect.br.x, rect.br.y, remplissage=bg_color, couleur=outline_color, epaisseur=outline_size)

    fltk.texte(rect_middle.x, rect_middle.y, text, taille=font_size, couleur=text_color, ancrage="center")

    if ev != None:
        click_pos: tuple = fltk_ext.position_souris(ev)
        return geom.in_rectangle(click_pos, rect.tl.to_tuple(), rect.br.to_tuple())
    return False
