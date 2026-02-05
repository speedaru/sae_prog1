import os

import libs.fltk as fltk
import src.utils.fltk_extensions as fltk_ext

import src.engine.engine_config as engine_config
import src.game.game_definitions as game_config

from src.utils.logging import *


def create_window(window_title: str, icon_file: str):
    """
    Creates and initializes the main game window using FLTK.

    It sets the window dimensions based on the game configuration, applies the title,
    and sets the window icon (Windows OS only).

    Args:
        window_title (str): The text to display in the window's title bar.
        icon_file (str): The path to the .ico file for the window icon.

    Note:
        This function triggers graphical calls and cannot be tested via doctest.
    """
    width = game_config.g_window_size[0]
    height = game_config.g_window_size[1]

    fltk.cree_fenetre(width, height, engine_config.TARGET_FPS)
    fltk_ext.fenetre_titre(window_title)

    screen_size = fltk_ext.taille_ecran()
    center_screen = ((screen_size[0] // 2 - width // 2), (screen_size[1] // 2 - height // 2))
    fltk_ext.fenetre_changer_position(game_config.g_window_size, center_screen[0], center_screen[1])

    log_debug(f"os name: {os.name}")

    # icon files work only on windows
    if os.name.lower() == "nt":
        fltk_ext.fenetre_icone(icon_file)

def end_window():
    """
    Closes and destroys the game window.
    
    Should be called when the game loop ends to free resources.
    """
    fltk.ferme_fenetre()

def start_render():
    """
    Prepares the canvas for a new frame by clearing all previous drawings.
    
    This is typically the first step in the rendering loop.
    """
    fltk.efface_tout()

def render():
    """
    Updates the window display to show the newly drawn frame.
    
    This function forces the FLTK engine to refresh the screen content.
    It effectively marks the end of the rendering phase for the current frame.
    """
    fltk.mise_a_jour()
