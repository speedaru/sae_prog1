from types import NoneType

import libs.fltk as fltk
from libs.fltk import FltkEvent

from src.engine.structs.dungeon import *

import src.game.game_config as game_config


def handle_input(input_event: FltkEvent | NoneType, dungeon: DungeonT):
    if input_event == None:
        return

