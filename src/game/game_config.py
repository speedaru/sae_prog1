from types import NoneType

from src.engine.asset_manager import BlockT, BlockListT
from src.engine.structs.dungeon import DungeonT
from src.game.state_manager import GameStateT


WINDOW_SIZE = [768, 768]
EXIT_KEY = "Escape"

GameContextT = list[BlockListT | DungeonT | GameStateT | NoneType]

GAME_CONTEXT_BLOCKS = 0
GAME_CONTEXT_GAME_STATE = 1
GAME_CONTEXT_DUNGEON = 2
GAME_CONTEXT_COUNT = 3
