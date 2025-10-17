import libs.fltk as fltk

import src.engine.engine_config as engine_config
import src.game.game_config as game_config


def create_window():
    width = game_config.WINDOW_SIZE[0]
    height = game_config.WINDOW_SIZE[1]

    fltk.cree_fenetre(width, height, engine_config.TARGET_FPS)

def end_window():
    fltk.ferme_fenetre()

def start_render():
    fltk.efface_tout()

def render():
    fltk.mise_a_jour()
