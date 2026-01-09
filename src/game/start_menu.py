# std python
import os
from types import NoneType
from pathlib import Path

# external librairies
import libs.fltk as fltk

# engine
from src.engine.structs.dungeon import DungeonT
from src.engine.parsing import *

# config and game
from src.config import DUNGEON_FILES_DIR
from src.game.game_definitions import *
from src.game.keys import *

# utils
from src.utils.logging import *
from src.utils.geom import * 
from src.engine.asset_manager import ASSETS_DIR

import src.utils.fltk_extensions as fltk_ext 
import src.utils.gui_geom as gui_geom 


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
    """
    Initializes the position structure for a menu item.

    This structure holds the metadata required to draw the menu item text
    and detect clicks on it (bounding box calculation).

    Args:
        positions (_PositionsT): The list to initialize (modified in-place).
        dungeon_name (str): The name of the dungeon file.
        pos (tuple[int, int]): The (x, y) coordinates of the text.
        size (tuple[int, int]): The (width, height) of the text.
    """
    
    if len(positions) != _POSITIONS_COUNT:
        positions[:] = [None] * _POSITIONS_COUNT

    positions[_POSITIONS_DUNGEON] = dungeon_name
    positions[_POSITIONS_POS] = pos
    positions[_POSITIONS_SIZE] = size


def _get_tl(position: _PositionsT) -> tuple[int, int]:
    """
    Gets the Top-Left coordinate of the menu item's bounding box.

    Args:
        position (_PositionsT): The initialized position structure.

    Returns:
        tuple[int, int]: The (x, y) coordinates.
    """
    return position[_POSITIONS_POS]

def _get_br(position: _PositionsT) -> tuple[int, int]:
    """
    Calculates the Bottom-Right coordinate of the menu item's bounding box.

    This is derived from the position (Top-Left) and the size of the text.

    Args:
        position (_PositionsT): The initialized position structure.

    Returns:
        tuple[int, int]: The (x + width, y + height) coordinates.
    """
    x, y = position[_POSITIONS_POS]
    w, h = position[_POSITIONS_SIZE]
    return (x + w, y + h)


def render(game_context: GameContextT) -> GameDataT | NoneType: 
    """
    Renders the Start Menu interface and handles dungeon selection.

    Process:
    1. Scans the `dungeons/` directory for dungeon files.
    2. Calculates the layout to center the dungeon names on the screen.
    3. Draws the names using FLTK.
    4. Checks for a Left Click event.
    5. If a click occurs inside a dungeon name's bounding box, parses that dungeon file.

    Args:
        game_context (GameContextT): The global game context containing events.

    Returns:
        GameDataT | NoneType: The parsed GameDataT structure (dungeon, adventure, dragons) if a file was clicked,
                             otherwise None.
    """
    # background
    BACKGROUND_FILE = "start_background.png"
    background_path = os.path.join(ASSETS_DIR, BACKGROUND_FILE)
    fltk.image(0,0,background_path,ancrage="nw")

    # game mode
    game_mode: GameModeE = game_context[T_GAME_CTX_GAME_DATA][T_GAME_DATA_GAME_MODE]
    text = f"Mode de jeu: {get_game_mode_text(game_mode)}"
    font_size = 24
    pos = gui_geom.anchor_text(gui_geom.E_UI_ANCHOR_BOTTOM_LEFT, text, font_size, padding=20)
    color = "red" if game_mode == E_GAME_MODE_EXTREME else "yellow"
    fltk.texte(pos[0], pos[1], chaine=text, couleur=color, taille=font_size)
    game_mode_button_size = fltk.taille_texte(text, taille=font_size)
    game_mode_button_rect = (pos, (pos[0] + game_mode_button_size[0], pos[1] + game_mode_button_size[1]))

    # retrieving dungeon files
    path_dungeons = Path(DUNGEON_FILES_DIR)

    dungeon_files = []
    for f in os.listdir(path_dungeons):
        # exclude files that start with $ bcs its save file
        if f.startswith("$"):
            continue

        if os.path.isfile(os.path.join(path_dungeons, f)):
            dungeon_files.append(f)

    # displaying centered names
    x = fltk.largeur_fenetre() / 2
    y: int = fltk.hauteur_fenetre() // 2 - 150

    PADDING_Y = 35
    positions: list[_PositionsT] = []  # to store positions

    for dungeon_name in dungeon_files:
        text = dungeon_name[:-4]  # remove ".txt"
        text_size = fltk.taille_texte(text)

        center_x: int = x - (text_size[0] / 2)
        fltk.texte(center_x, y, text, couleur="white")

        # create and initialize the complete structure
        pos_struct: _PositionsT = _PositionsT() * _POSITIONS_COUNT
        _positions_init(pos_struct, dungeon_name=dungeon_name, pos=(center_x, y), size=text_size)
        positions.append(pos_struct)

        y += text_size[1] + PADDING_Y

    # if left clicked pressed return selected dungeon as EventDataT
    ev: FltkEvent = game_context[T_GAME_CTX_EVENT][T_GAME_EVENT_TYPE]
    if fltk.type_ev(ev) == KEY_X1:
        click_pos = fltk_ext.position_souris(ev)  # coordonnées de la souris

        # game mode button clicked
        if in_rectangle(click_pos, game_mode_button_rect[0], game_mode_button_rect[1]):
            game_data = game_context[T_GAME_CTX_GAME_DATA]
            current_mode = game_data[T_GAME_DATA_GAME_MODE]
            game_data[T_GAME_DATA_GAME_MODE] = (current_mode + 1) % E_GAME_MODE_COUNT

        # check which text was clicked
        for position in positions:
            tl = _get_tl(position)
            br = _get_br(position)
            if in_rectangle(click_pos, tl, br):
                game_file_path = os.path.join(DUNGEON_FILES_DIR, str(position[_POSITIONS_DUNGEON]))
                parsed_game_data: GameDataT = game_context[T_GAME_CTX_GAME_DATA][:]
                parsed_successfuly = game_data_parse_file(parsed_game_data, game_file_path)
                if parsed_successfuly:
                    return parsed_game_data

    return None

