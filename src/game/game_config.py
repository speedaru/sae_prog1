"""
Game Configuration Module.

This module holds global constants, type definitions, and index mappings (enums)
used across the game. It serves as a central point for game settings.

It defines:
- Window settings (size).
- Game keys (exit).
- Data structures for the Game Context and Game Events (using lists).
- Indices for accessing these list-based structures.

Global Constants:
    WINDOW_SIZE: Dimensions of the game window [width, height].
    EXIT_KEY: The key used to exit the game.
    DUNGEON_DRAGONS_COUNT: Default number of dragons.

Context Indices (Pseudo-Enums):
    Used to access `GameContextT` list elements.
    GAME_CONTEXT_ASSETS, GAME_CONTEXT_GAME_STATE, etc.

Event Indices (Pseudo-Enums):
    Used to access `GameEventT` list elements.
    GAME_EVENT_TYPE, GAME_EVENT_DATA.
"""
from types import NoneType
from typing import Any

from libs.fltk import FltkEvent

from src.engine.asset_manager import AssetsT, BlockT, BlockListT
from src.engine.structs.dungeon import DungeonT
from src.engine.structs.entity import EntityT
from src.engine.structs.adventurer import AdventurerT
from src.engine.structs.dragon import DragonT

from src.game.state_manager import GameStateT
from src.game.keys import *


# constants
WINDOW_SIZE = [768, 768]
EXIT_KEY = KEY_ESCAPE
DUNGEON_DRAGONS_COUNT = 3

# types
GameEventDataT = Any
GameEventT = list[FltkEvent | GameEventDataT] # data from game event
GameContextT = list[AssetsT | GameEventT | DungeonT | GameStateT | NoneType | EntityT | AdventurerT | list[DragonT]]

# enum for game context
GAME_CONTEXT_ASSETS = 0         # list of block images
GAME_CONTEXT_GAME_STATE = 1     # game state type
GAME_CONTEXT_EVENT = 2          # fltk event if there is one
GAME_CONTEXT_DUNGEON = 3        # current dungeon DungeonT
GAME_CONTEXT_ORIGINAL_DUNGEON = 4   # so we can reload it
GAME_CONTEXT_ADVENTURER = 5     # adventurer, AdventurerT
GAME_CONTEXT_DRAGONS = 6        # list dragons in the dungeon, list[DragonT]
GAME_CONTEXT_ORIGINAL_ADVENTURER = 7 # copy of adventurer when adventurer is created
GAME_CONTEXT_ORIGINAL_DRAGONS = 8 # copy of dragons when dragons is created
GAME_CONTEXT_COUNT = 9

# enum for game event
GAME_EVENT_TYPE = 0 # event type, FltkEvent
GAME_EVENT_DATA = 1 # event data
GAME_EVENT_COUNT = 2

def game_context_init() -> GameContextT:
    return [[None] for _ in range(GAME_CONTEXT_COUNT)]
