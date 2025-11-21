# std python
import os
from types import NoneType
from pathlib import Path

# external librairies
import libs.fltk as fltk

# import games project files
from src.config import DUNGEON_FILES_DIR
from src.engine.structs.dungeon import DungeonT, dungeon_parse_file
from src.game.game_config import *
from src.utils.logging import *
from src.utils.geom import * 
from src.engine.asset_manager import ASSETS_DIR

import src.utils.fltk_extensions as fltk_ext 


# types
_PositionsT = list[str | tuple[int, int] | int]

# enum for positions structure
_POSITIONS_DUNGEON = 0      # dungeon_filename (string)
_POSITIONS_POS = 1          # position (tuple[int, int])
_POSITIONS_SIZE = 2         # text_size (width, height)
_POSITIONS_COUNT = 3        # total_fields_count

def _positions_init(positions: _PositionsT,
                   dungeon_name: str = "",
                   pos: tuple[int, int] = (0, 0),
                   size: tuple[int, int] = (0, 0)):
    
    if len(positions) != _POSITIONS_COUNT:
        positions[:] = [None] * _POSITIONS_COUNT

    positions[_POSITIONS_DUNGEON] = dungeon_name
    positions[_POSITIONS_POS] = pos
    positions[_POSITIONS_SIZE] = size


def _get_tl(position: _PositionsT):
    return position[_POSITIONS_POS]

def _get_br(position: _PositionsT):
    x, y = position[_POSITIONS_POS]
    w, h = position[_POSITIONS_SIZE]
    return (x + w, y + h)


def render(game_context: GameContextT) -> DungeonT | NoneType: 
    #background
    BACKGROUND_FILE = "start_background.png"
    background_path = os.path.join(ASSETS_DIR, BACKGROUND_FILE)
    fltk.image(0,0,background_path,ancrage="nw")

    # retrieving dungeon files
    path_dungeons = Path(DUNGEON_FILES_DIR)

    dungeon_files = []
    for f in os.listdir(path_dungeons):
        if os.path.isfile(os.path.join(path_dungeons, f)):
            dungeon_files.append(f)

    # displaying centered names
    x = fltk.largeur_fenetre() / 2
    y = fltk.hauteur_fenetre() / 2 - 150

    PADDING_Y = 35
    positions: list[_PositionsT] = []  # to store positions

    for dungeon_name in dungeon_files:
        text = dungeon_name[:-4]  # remove ".txt"
        text_size = fltk.taille_texte(text)

        center_x = x - (text_size[0] / 2)
        fltk.texte(center_x, y, text, couleur="white")

        # create and initialize the complete structure
        pos_struct: _PositionsT = [None] * _POSITIONS_COUNT
        _positions_init(pos_struct, dungeon_name=dungeon_name, pos=(center_x, y), size=text_size)
        positions.append(pos_struct)

        y += text_size[1] + PADDING_Y

    fltk.mise_a_jour()

    # handling left click
    ev = game_context[GAME_CONTEXT_EVENT][GAME_EVENT_TYPE]
    if fltk.type_ev(ev) == "ClicGauche":
        click_pos = fltk_ext.position_souris(ev)  # mouse coordinates

        # check which text was clicked
        for position in positions:
            tl = _get_tl(position)
            br = _get_br(position)
            log_debug(f"clique{click_pos}")
            log_debug(f"tl,br{tl,br}")
            if in_rectangle(click_pos, tl, br):
                log_debug("OUI")
                dungeon = DungeonT()
                dungeon_file_path = os.path.join(DUNGEON_FILES_DIR,
                                                position[_POSITIONS_DUNGEON])
                log_debug(f"FICHIERS {dungeon_file_path} ")
                dungeon_parse_file (dungeon,dungeon_file_path)
                return dungeon

    return None

