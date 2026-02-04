from copy import deepcopy

from src.engine.game_event_system import *
from src.engine.structs.dungeon import *
from src.engine.structs.adventurer import *
from src.engine.structs.chaos_seal import *
from src.engine.structs.entity import *

from src.game.game_definitions import *

from src.utils.entity_utils import get_dragon_positions


# ChaosSealT -> GameEventT -> TemporaryGameEventT
ChaosSealEventT = TemporaryGameEventT

T_CHAOS_SEAL_EVENT_ORIGINAL_DUNGEON   = T_TEMP_GAME_EVENT_COUNT
T_CHAOS_SEAL_EVENT_COUNT              = T_TEMP_GAME_EVENT_COUNT + 1

CHAOS_SEAL_DURATION = 1 # lasts 1 round

# temp event enum
E_TEMP_EVENT_CHAOS_SEAL = 0


def _chaos_seal_activate(chaos_seal_event: ChaosSealEventT):
    log_debug(f"[_chaos_seal_on_frame] activated chaos seal")
    game_data = chaos_seal_event[T_GAME_EVENT_GAME_CTX][T_GAME_CTX_GAME_DATA]
    entity_system: EntitySystemT = game_data[T_DUNGEON_DATA_ENTITY_SYSTEM]
    dungeon: DungeonT = game_data[T_DUNGEON_DATA_DUNGEON]

    # create copy of current dungeon to restore it when destroyed
    chaos_seal_event[T_CHAOS_SEAL_EVENT_ORIGINAL_DUNGEON] = deepcopy(dungeon)

    rooms_to_block = get_dragon_positions(entity_system)

    # find lowest level dragon
    dragon_lowest_level = min(entity_system_get_all(entity_system, E_ENTITY_DRAGON), key=lambda e: e[T_ENTITY_LEVEL])

    # remove lower dragon pos from other dragon pos
    rooms_to_block.remove(dragon_lowest_level[T_BASE_ENTITY_ROOM_POS])

    # replace rooms
    for i, row in enumerate(dungeon):
        for j, col in enumerate(row):
            if room_pos_create(row=i, col=j) in rooms_to_block:
                block_id = BLOCK_SOLID
                rotation_count = 0
                dungeon[i][j] = (block_id, rotation_count)
            else:
                block_id = BLOCK_QUAD
                rotation_count = 0
                dungeon[i][j] = (block_id, rotation_count)

def _chaos_seal_on_destroy(chaos_seal_event: ChaosSealEventT):
    game_data = chaos_seal_event[T_GAME_EVENT_GAME_CTX][T_GAME_CTX_GAME_DATA]

    # restore original dungeon
    original_dungeon = chaos_seal_event[T_CHAOS_SEAL_EVENT_ORIGINAL_DUNGEON]
    game_data[T_DUNGEON_DATA_DUNGEON][:] = original_dungeon.copy()

def _chaos_seal_on_round_end(chaos_seal_event: ChaosSealEventT):
    log_debug(f"[_chaos_seal_on_round_end] duration left: {chaos_seal_event[T_GAME_EVENT_DURATION]}")

    # if chaos seal is active but all dragons are trapped, untrap lowest level one

    game_data = chaos_seal_event[T_GAME_EVENT_GAME_CTX][T_GAME_CTX_GAME_DATA]
    entity_system: EntitySystemT = game_data[T_DUNGEON_DATA_ENTITY_SYSTEM]
    dungeon: DungeonT = game_data[T_DUNGEON_DATA_DUNGEON]

    # if no dragons, exit
    dragons = entity_system_get_all(entity_system, E_ENTITY_DRAGON)
    if len(dragons) <= 0:
        return

    # find lowest level dragon
    dragon_lowest_level = min(dragons, key=lambda e: e[T_ENTITY_LEVEL])

    if dragon_lowest_level != None:
        room_pos = dragon_lowest_level[T_BASE_ENTITY_ROOM_POS]
        row, col = room_pos[ROOM_POS_ROW], room_pos[ROOM_POS_COL]
        dungeon[row][col] = [BLOCK_QUAD, dungeon[row][col][ROOM_ROTATION_COUNT]]


def chaos_seal_event_register_ex(event_system: GameEventSystemT,
                                 duration,
                                 phase: GamePhaseE,
                                 flags,
                                 game_ctx):

    temporary_game_event_register(event_system=event_system,
                                  phase=phase,
                                  duration=duration,
                                  on_create=_chaos_seal_activate, on_destroy=_chaos_seal_on_destroy,
                                  on_frame=None, on_round_end=_chaos_seal_on_round_end,
                                  temp_event_type=E_TEMP_EVENT_CHAOS_SEAL,
                                  flags=flags,
                                  game_ctx=game_ctx,
                                  size=T_CHAOS_SEAL_EVENT_COUNT)

    log_debug(f"[chaos_seal_register] registered chaos seal event")

def chaos_seal_event_register(game_ctx):
    event_system = game_ctx[T_GAME_CTX_GAME_DATA][T_GAME_DATA_EVENT_SYSTEM]

    phase = E_PHASE_POST_ADVENTURER
    chaos_seal_event_register_ex(event_system, CHAOS_SEAL_DURATION, phase, F_GAME_EVENT_NONE, game_ctx)

def chaos_seal_get_callbacks() -> TempEventCallbacksT:
    return temp_event_callbacks_create(on_create=_chaos_seal_activate,
                                       on_frame=None,
                                       on_round_end=_chaos_seal_on_round_end,
                                       on_destroy=_chaos_seal_on_destroy)
