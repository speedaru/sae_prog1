import os

import libs.fltk as fltk
import src.utils.fltk_extensions as fltk_ext

import src.engine.engine_config as engine_config
import src.game.game_config as game_config

from src.utils.logging import *


def create_window(window_title: str, icon_file: str):
    width = game_config.WINDOW_SIZE[0]
    height = game_config.WINDOW_SIZE[1]

    fltk.cree_fenetre(width, height, engine_config.TARGET_FPS)
    fltk_ext.fenetre_titre(window_title)

    log_debug(f"os name: {os.name}")

    # icon files work only on windows
    if os.name.lower() == "nt":
        fltk_ext.fenetre_icone(icon_file)

def end_window():
    fltk.ferme_fenetre()

def start_render():
    fltk.efface_tout()

def render():
    fltk.mise_a_jour()
