from types import NoneType
from typing import Any

from src.game.state_manager import *
from src.game.game_phases import *

from src.utils.logging import *


GameEventFlags = int
GameEventT = list[int | Any]
GameEventSystemT = list[list[GameEventT]] # each sublist corresponds to a game phase

T_GAME_EVENT_ID             = 0 # unique id, should never be accessed outside of this module
T_GAME_EVENT_DURATION       = 1 # number of rounds that the events lasts (-1 if perpetual + F_GAME_EVENT_PERPETUAL flag)
T_GAME_EVENT_ON_FRAME       = 2 # callback to call every frame
T_GAME_EVENT_ON_ROUND_END   = 3 # callback to call when round finished
T_GAME_EVENT_FLAGS          = 4 # flags
T_GAME_EVENT_GAME_CTX       = 5 # data to pass to on_tick function
T_GAME_EVENT_COUNT          = 6

EVENT_DURATION_PERPERTUAL = -1

F_GAME_EVENT_NONE       = 0       # event is paused dont handle it
F_GAME_EVENT_PAUSED     = 1 << 0  # event is paused dont handle it
F_GAME_EVENT_COMPLETED  = 1 << 1  # event is finished, we can remove it
F_GAME_EVENT_PERPETUAL  = 1 << 2  # event is perpetual, never stop



# -------------------- private functions

def _generate_id(event_system) -> int:
    max_id = 0
    for phase_list in event_system:
        for event in phase_list:
            if event[T_GAME_EVENT_ID] > max_id:
                max_id = event[T_GAME_EVENT_ID]
    return max_id + 1


# -------------------- public api

def game_event_create(event_id: int,
                      duration: int,
                      on_frame, on_round_end,
                      flags: GameFlags,
                      game_ctx,
                      size: int = T_GAME_EVENT_COUNT):
    """
    create game event
    """
    game_event: GameEventT = [None] * size

    game_event[T_GAME_EVENT_ID] = event_id
    game_event[T_GAME_EVENT_DURATION] = duration
    game_event[T_GAME_EVENT_ON_FRAME] = on_frame
    game_event[T_GAME_EVENT_ON_ROUND_END] = on_round_end
    game_event[T_GAME_EVENT_FLAGS] = flags
    game_event[T_GAME_EVENT_GAME_CTX] = game_ctx

    return game_event

def game_event_register_ex(event_system: GameEventSystemT,
                        phase: GamePhaseE, # GamePhaseE in which the event should be handled
                        duration: int,
                        on_frame, on_round_end, # callbacks
                        flags: int,
                        game_ctx,
                        size: int = T_GAME_EVENT_COUNT) -> int:
    """
    returns: created event id
    """
    game_event = game_event_create(event_id=_generate_id(event_system),
                                   duration=duration,
                                   on_frame=on_frame, on_round_end=on_round_end,
                                   flags=flags,
                                   game_ctx=game_ctx,
                                   size=size)

    event_system[phase].append(game_event)

    log_debug(f"[game_event_register] registered game event for phase: {phase}, callbacks: ")
    log_debug(f"{on_frame=}, {on_round_end=}")

    return game_event[T_GAME_EVENT_ID] 

def game_event_register(event_system,
                        phase: GamePhaseE,
                        duration: int,
                        on_frame = None,
                        on_round_end = None,
                        game_ctx = None,
                        size: int = T_GAME_EVENT_COUNT) -> int:
    # set perpetual flag if duration is -1
    flags = F_GAME_EVENT_PERPETUAL if duration == EVENT_DURATION_PERPERTUAL else F_GAME_EVENT_NONE

    return game_event_register_ex(event_system, phase, duration, on_frame, on_round_end, flags, game_ctx, size)

def game_event_is_perpertual(event: GameEventT) -> bool:
    return bool(event[T_GAME_EVENT_FLAGS] & F_GAME_EVENT_PERPETUAL)

def game_event_unregister(event_system: GameEventSystemT, game_event: GameEventT):
    for current_phase in range(len(event_system)):
        phase_events = event_system[current_phase]
        if game_event in phase_events:
            event_system[current_phase].remove(game_event)
            return

def game_event_get_by_id(event_system: GameEventSystemT, event_id: int) -> GameEventT | NoneType:
    for phase_list in event_system:
        for event in phase_list:
            if event[T_GAME_EVENT_ID] == event_id:
                return event

    log_error(f"couldnt find event id: {event_id}")
    return None

def game_event_system_is_temporary_game_event(game_event):
    # >= cuz can be child of other higher classes
    return len(game_event) >= T_TEMP_GAME_EVENT_COUNT

def game_event_execute_callback(event: GameEventT, callback_idx: int):
    """
    executes specified callback if not None
    """
    callback = event[callback_idx]
    if callback != None:
        # callback(event[T_GAME_EVENT_GAME_CTX])
        callback(event)

