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
from src.engine.structs.entity_system import *
from src.engine.structs.adventurer import AdventurerT
from src.engine.structs.dragon import DragonT
from src.engine.asset_manager import BLOCK_SCALED_SIZE

from src.game.state_manager import GameFlags
from src.game.entity_definitions import *
from src.game.keys import *


# constants
WINDOW_GRID_SIZE = [6, 6]
WINDOW_SIZE = [WINDOW_GRID_SIZE[0] * BLOCK_SCALED_SIZE[0], WINDOW_GRID_SIZE[1] * BLOCK_SCALED_SIZE[1]]
EXIT_KEY = KEY_ESCAPE
DUNGEON_DRAGONS_COUNT = 3

# types
GameEventDataT = Any
GameEventT = list[FltkEvent | GameEventDataT] # data from game event
GameContextT = list[AssetsT | GameEventT | DungeonT | GameFlags | NoneType | EntityT | AdventurerT | list[DragonT]]

# enum for game context
T_GAME_CTX_ASSETS = 0         # list of block images
T_GAME_CTX_GAME_FLAGS = 1     # game state type
T_GAME_CTX_EVENT = 2          # fltk event if there is one
T_GAME_CTX_GAME_DATA = 3      # stores dungeon, entities etc
T_GAME_CTX_ORIGINAL_GAME_DATA = 4 # store original game state so we can restore it
T_GAME_CTX_FPS_MANAGER = 5    # see use case in engine/fps_manager.py
T_GAME_CTX_COUNT = 6

# enum for game event
T_GAME_EVENT_TYPE = 0 # event type, FltkEvent
T_GAME_EVENT_DATA = 1 # event data
T_GAME_EVENT_COUNT = 2

# game mode enums
GameModeE = int
E_GAME_MODE_NORMAL = 0
E_GAME_MODE_EXTREME = 1
E_GAME_MODE_COUNT = 2

# dungeon, player, dragons, etc...
GameDataT = list[DungeonT | EntitySystemT | int | None]
T_GAME_DATA_DUNGEON = 0
T_GAME_DATA_ENTITY_SYSTEM = 1
T_GAME_DATA_TREASURE_COUNT = 2 # treasure count in dungeon
T_GAME_DATA_GAME_MODE = 3
T_GAME_DATA_ROUND = 4 # which round are we on
T_GAME_DATA_COUNT = 5

def game_data_init() -> GameDataT:
    # dungeon
    dungeon = DungeonT()
    dungeon_init(dungeon, 0, 0)

    game_data: GameDataT = [None] * T_GAME_DATA_COUNT
    game_data[T_GAME_DATA_DUNGEON] = dungeon
    game_data[T_GAME_DATA_ENTITY_SYSTEM] = entity_system_create()
    game_data[T_GAME_DATA_TREASURE_COUNT] = 0
    game_data[T_GAME_DATA_GAME_MODE] = E_GAME_MODE_NORMAL
    game_data[T_GAME_DATA_ROUND] = 1

    return game_data

def game_event_create(event_type = None, event_data = None) -> GameEventT:
    event = [None] * T_GAME_EVENT_COUNT

    event[T_GAME_EVENT_TYPE] = event_type
    event[T_GAME_EVENT_DATA] = event_data

    return event

def game_context_create(assets,
                        game_flags,
                        event: GameEventT,
                        game_data,
                        original_game_data,
                        fps_manager) -> GameContextT:
    game_context = [None] * T_GAME_CTX_COUNT

    game_context[T_GAME_CTX_ASSETS] = assets
    game_context[T_GAME_CTX_GAME_FLAGS] = game_flags
    game_context[T_GAME_CTX_EVENT] = event
    game_context[T_GAME_CTX_GAME_DATA] = game_data
    game_context[T_GAME_CTX_ORIGINAL_GAME_DATA] = original_game_data
    game_context[T_GAME_CTX_FPS_MANAGER] = fps_manager

    return game_context

def get_game_mode_text(game_mode: GameModeE):
    if game_mode == E_GAME_MODE_NORMAL:
        return "normal"
    elif game_mode == E_GAME_MODE_EXTREME:
        return "extreme"
    else:
        return "unknown"
