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
    Used to access `InputEventT` list elements.
    GAME_EVENT_TYPE, GAME_EVENT_DATA.
"""
from types import NoneType
from typing import Any

from libs.fltk import FltkEvent

import src.engine.structs.dungeon as dungeon_mod
import src.engine.game_event_system as game_event_system_mod
import src.engine.entity_system as entity_system_mod
from src.engine.asset_manager import *

from src.game.globals import *

from src.game.state_manager import GameFlags
from src.game.entity_definitions import *
from src.game.keys import *


# types
GameEventDataT = Any # to make it explicit when functions return event data
InputEventT = list[FltkEvent | GameEventDataT] # data from game event
GameContextT = list

# enum for game context
T_GAME_CTX_ASSETS               = 0 # list of block images
T_GAME_CTX_GAME_FLAGS           = 1 # game state type
T_GAME_CTX_ACTIVE_WINDOW        = 2 # current active window (menu, or game or wtv)
T_GAME_CTX_EVENT                = 3 # fltk event if there is one
T_GAME_CTX_GAME_DATA            = 4 # stores dungeon, entities etc
T_GAME_CTX_ORIGINAL_GAME_DATA   = 5 # store original game state so we can restore it
T_GAME_CTX_FPS_MANAGER          = 6 # see use case in engine/fps_manager.py
T_GAME_CTX_COUNT                = 7

# enum for game event
T_INPUT_EVENT_TYPE = 0 # event type, FltkEvent
T_INPUT_EVENT_DATA = 1 # event data
T_INPUT_EVENT_COUNT = 2

# game mode enums
GameModeE = int
E_GAME_MODE_NORMAL = 0
E_GAME_MODE_SINGLE_TURN = 1
E_GAME_MODE_EXTREME = 2
E_GAME_MODE_COUNT = 3

# simple dungeon with just the dungeon and whats inside
DungeonDataT = list
T_DUNGEON_DATA_DUNGEON = 0 # DungeonT
T_DUNGEON_DATA_ENTITY_SYSTEM = 1 # EntitySystemT
T_DUNGEON_DATA_TREASURE_COUNT = 2 # treasure count left in dungeon (mutable)
T_DUNGEON_DATA_GAME_MODE = 3 # GameModeE
T_DUNGEON_DATA_COUNT = 4

# dungeon data but with extra stuff like game mode round counter etc...
GameDataT = list
T_GAME_DATA_EVENT_SYSTEM = T_DUNGEON_DATA_COUNT + 0 # GameEventSystemT
T_GAME_DATA_ROUND = T_DUNGEON_DATA_COUNT + 1 # round counter (starts at 1)
T_GAME_DATA_COUNT = T_DUNGEON_DATA_COUNT + 2

def dungeon_data_init(size = T_DUNGEON_DATA_COUNT) -> DungeonDataT:
    # dungeon
    dungeon = dungeon_mod.DungeonT()
    dungeon_mod.dungeon_init(dungeon, 0, 0)

    dungeon_data: GameDataT = [None] * size
    dungeon_data[T_DUNGEON_DATA_DUNGEON] = dungeon
    dungeon_data[T_DUNGEON_DATA_ENTITY_SYSTEM] = entity_system_mod.entity_system_create()
    dungeon_data[T_DUNGEON_DATA_TREASURE_COUNT] = 0
    dungeon_data[T_DUNGEON_DATA_GAME_MODE] = E_GAME_MODE_NORMAL

    return dungeon_data

def game_data_init() -> GameDataT:
    game_data = dungeon_data_init(T_GAME_DATA_COUNT)

    game_data[T_GAME_DATA_EVENT_SYSTEM] = game_event_system_mod.game_event_system_create()
    game_data[T_GAME_DATA_ROUND] = 1

    return game_data

def game_data_set_dungeon_data(game_data, dungeon_data):
    for i in range(T_DUNGEON_DATA_COUNT):
        game_data[i] = dungeon_data[i]

def input_event_create(event_type = None, event_data = None) -> InputEventT:
    event = [None] * T_INPUT_EVENT_COUNT

    event[T_INPUT_EVENT_TYPE] = event_type
    event[T_INPUT_EVENT_DATA] = event_data

    return event

def game_context_create(assets,
                        game_flags,
                        active_window,
                        event, # InputEventT
                        game_data,
                        original_game_data,
                        fps_manager) -> GameContextT:
    game_context = [None] * T_GAME_CTX_COUNT

    game_context[T_GAME_CTX_ASSETS] = assets
    game_context[T_GAME_CTX_GAME_FLAGS] = game_flags
    game_context[T_GAME_CTX_ACTIVE_WINDOW] = active_window
    game_context[T_GAME_CTX_EVENT] = event
    game_context[T_GAME_CTX_GAME_DATA] = game_data
    game_context[T_GAME_CTX_ORIGINAL_GAME_DATA] = original_game_data
    game_context[T_GAME_CTX_FPS_MANAGER] = fps_manager

    return game_context

def get_game_mode_text(game_mode: GameModeE):
    if game_mode == E_GAME_MODE_NORMAL:
        return "normal"
    elif game_mode == E_GAME_MODE_SINGLE_TURN:
        return "single turn"
    elif game_mode == E_GAME_MODE_EXTREME:
        return "extreme"
    else:
        return "unknown"

def get_game_mode_text_color(game_mode: GameModeE):
    if game_mode == E_GAME_MODE_NORMAL:
        return "white"
    elif game_mode == E_GAME_MODE_SINGLE_TURN:
        return "yellow"
    elif game_mode == E_GAME_MODE_EXTREME:
        return "red"
