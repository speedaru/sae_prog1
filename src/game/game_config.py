from types import NoneType
from typing import Any

from libs.fltk import FltkEvent

from src.engine.asset_manager import AssetsT, BlockT, BlockListT
from src.engine.structs.dungeon import DungeonT
from src.game.state_manager import GameStateT


# constants
WINDOW_SIZE = [768, 768]
EXIT_KEY = "Escape"
DUNGEON_DRAGONS_COUNT = 3

# types
GameEventDataT = Any
GameEventT = list[FltkEvent | GameEventDataT] # data from game event
GameContextT = list[AssetsT | GameEventT | DungeonT | GameStateT | NoneType]

# enum for game context
GAME_CONTEXT_ASSETS = 0     # list of block images
GAME_CONTEXT_GAME_STATE = 1 # game state type
GAME_CONTEXT_EVENT = 2      # fltk event if there is one
GAME_CONTEXT_DUNGEON = 3    # current dungeon DungeonT
GAME_CONTEXT_ADVENTURER = 4 # adventurer, AdventurerT
GAME_CONTEXT_DRAGONS = 5    # list dragons in the dungeon, list[DragonT]
GAME_CONTEXT_COUNT = 6

# enum for game event
GAME_EVENT_TYPE = 0 # event type, FltkEvent
GAME_EVENT_DATA = 1 # event data
GAME_EVENT_COUNT = 2
