from types import NoneType

import libs.fltk as fltk

from src.config import *
from src.engine.structs.dungeon import *
from src.game.game_config import *
from src.utils.logging import *



# returns None (if not clicked), returns dungeon if clicked
def render(game_context: GameContextT) -> DungeonT | NoneType:
    # # mouse_click_coords = fltk.click_gauche()
    # fltk.attend_clic_gauche
    #
    # if fltk.type_ev(fltk.attend_ev()) == "ClicGauche":
    #     dungeon: DungeonT = DungeonT()
    #     # dungeon_file_path = os.path.join(DUNGEON_FILES_DIR, "dungeon_easy.txt")
    #     dungeon_file_path = os.path.join(DUNGEON_FILES_DIR, "dungeon_hard.txt")
    #
    #     dungeon_parse_file(dungeon_file_path, dungeon)
    #
    #     return dungeon

    # mouse_click_coords = fltk.click_gauche()
    ev = game_context[GAME_CONTEXT_EVENT][GAME_EVENT_TYPE]

    if fltk.type_ev(ev) == "ClicGauche":
        dungeon: DungeonT = DungeonT()
        dungeon_file_path = os.path.join(DUNGEON_FILES_DIR, "dungeon_hard.txt")

        dungeon_parse_file(dungeon, dungeon_file_path)

        return dungeon

    return None

