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
from src.engine.structs.dungeon import DungeonT, dungeon_init
from src.engine.structs.entity import EntityT, EntitiesT, entities_init
from src.engine.structs.adventurer import AdventurerT
from src.engine.structs.dragon import DragonT
from src.engine.asset_manager import BLOCK_SCALED_SIZE

from src.game.state_manager import GameStateT
from src.game.keys import *


# constants
WINDOW_GRID_SIZE = [6, 6]
WINDOW_SIZE = [WINDOW_GRID_SIZE[0] * BLOCK_SCALED_SIZE[0], WINDOW_GRID_SIZE[1] * BLOCK_SCALED_SIZE[1]]
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
GAME_CONTEXT_GAME_DATA = 3      # stores dungeon, entities etc
GAME_CONTEXT_ORIGINAL_GAME_DATA = 4 # store original game state so we can restore it
GAME_CONTEXT_COUNT = 5

# enum for game event
GAME_EVENT_TYPE = 0 # event type, FltkEvent
GAME_EVENT_DATA = 1 # event data
GAME_EVENT_COUNT = 2

# entity enums
E_ENTITY_UNKNOWN = 0xffff
E_ENTITY_ADVENTURER = 0
E_ENTITY_DRAGON = 1
E_ENTITY_TREASURE = 2
E_ENTITY_COUNT = 3

# game mode enums
GameModeE = int
E_GAME_MODE_NORMAL = 0
E_GAME_MODE_EXTREME = 1
E_GAME_MODE_COUNT = 2

ENTITY_CHARS = { "A": E_ENTITY_ADVENTURER, "D": E_ENTITY_DRAGON, "T": E_ENTITY_TREASURE }

# dungeon, player, dragons, etc...
GameDataT = list[DungeonT | EntitiesT | int]
GAME_DATA_DUNGEON = 0
GAME_DATA_ENTITIES = 1
GAME_DATA_TREASURE_COUNT = 2 # treasure count in dungeon
GAME_DATA_GAME_MODE = 3
GAME_DATA_ROUND = 4 # which round are we on
GAME_DATA_COUNT = 5

def game_data_init() -> GameDataT:
    # dungeon
    dungeon = DungeonT()
    dungeon_init(dungeon, 0, 0)

    # entities
    entities: EntitiesT = EntitiesT()
    entities_init(entities)

    game_data: GameDataT = [None] * GAME_DATA_COUNT
    game_data[GAME_DATA_DUNGEON] = dungeon
    game_data[GAME_DATA_ENTITIES] = entities
    game_data[GAME_DATA_TREASURE_COUNT] = 0
    game_data[GAME_DATA_GAME_MODE] = E_GAME_MODE_NORMAL
    game_data[GAME_DATA_ROUND] = 1

    return game_data

def game_context_init() -> GameContextT:
    return [[None] for _ in range(GAME_CONTEXT_COUNT)]

def get_game_mode_text(game_mode: GameModeE):
    if game_mode == E_GAME_MODE_NORMAL:
        return "normal"
    elif game_mode == E_GAME_MODE_EXTREME:
        return "extreme"
    else:
        return "unknown"
