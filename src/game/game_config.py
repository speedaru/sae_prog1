from types import NoneType
from typing import Any

from libs.fltk import FltkEvent

from src.engine.asset_manager import BlockT, BlockListT
from src.engine.structs.dungeon import DungeonT
from src.game.state_manager import GameStateT


# constants
WINDOW_SIZE = [768, 768]
EXIT_KEY = "Escape"

# types
GameEventDataT = Any
GameEventT = list[FltkEvent | GameEventDataT] # data from game event
GameContextT = list[BlockListT | GameEventT | DungeonT | GameStateT | NoneType]

# enum for game context
GAME_CONTEXT_BLOCKS = 0     # list of block images
GAME_CONTEXT_GAME_STATE = 1 # game state type
GAME_CONTEXT_EVENT = 2 # fltk event if there is one
GAME_CONTEXT_DUNGEON = 3    # current dungeon DungeonT
GAME_CONTEXT_COUNT = 4

# enum for game event
GAME_EVENT_TYPE = 0 # event type, FltkEvent
GAME_EVENT_DATA = 1 # event data
GAME_EVENT_COUNT = 2
