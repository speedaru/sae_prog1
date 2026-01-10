from src.engine.structs.game_event import *

from src.game.game_definitions import *

# GameEventT -> TemporaryGameEventT
TemporaryGameEventT = GameEventT

T_TEMP_GAME_EVENT_TYPE       = T_GAME_EVENT_COUNT + 0 # type of temp game event
T_TEMP_GAME_EVENT_ON_CREATE  = T_GAME_EVENT_COUNT + 1 # callback to call when temp event gets created
T_TEMP_GAME_EVENT_ON_DESTROY = T_GAME_EVENT_COUNT + 2 # callback to call when temp event gets destroyed
T_TEMP_GAME_EVENT_COUNT      = T_GAME_EVENT_COUNT + 3 #

# enum of all temporary game events that exist
TempEventE = int

# callbacks
TempEventCallbacksT = list

T_TEMP_EVENT_CALLBACKS_ON_CREATE    = 0
T_TEMP_EVENT_CALLBACKS_ON_FRAME     = 1
T_TEMP_EVENT_CALLBACKS_ON_ROUND_END = 2
T_TEMP_EVENT_CALLBACKS_ON_DESTROY   = 3
T_TEMP_EVENT_CALLBACKS_COUNT        = 4


def temp_event_callbacks_create(on_create = None, on_frame = None, on_round_end = None, on_destroy = None):
    callbacks = [None] * T_TEMP_EVENT_CALLBACKS_COUNT

    callbacks[T_TEMP_EVENT_CALLBACKS_ON_CREATE] = on_create
    callbacks[T_TEMP_EVENT_CALLBACKS_ON_FRAME] = on_frame
    callbacks[T_TEMP_EVENT_CALLBACKS_ON_ROUND_END] = on_round_end
    callbacks[T_TEMP_EVENT_CALLBACKS_ON_DESTROY] = on_destroy

    return callbacks

def temporary_game_event_register(event_system: GameEventSystemT,
                                  phase: GamePhaseE, # GamePhaseE in which the event should be handled
                                  duration: int,
                                  on_create, on_frame, on_round_end, on_destroy, # callbacks
                                  temp_event_type: TempEventE,
                                  flags: int,
                                  game_ctx,
                                  size: int = T_TEMP_GAME_EVENT_COUNT) -> TemporaryGameEventT:
    # register game event
    event_id = game_event_register_ex(event_system=event_system,
                                      phase=phase,
                                      duration=duration,
                                      on_frame=on_frame, on_round_end=on_round_end,
                                      flags=flags,
                                      game_ctx=game_ctx,
                                      size=size)

    game_event: TemporaryGameEventT = game_event_get_by_id(event_system, event_id)

    # init extra properties
    game_event[T_TEMP_GAME_EVENT_TYPE] = temp_event_type
    game_event[T_TEMP_GAME_EVENT_ON_CREATE] = on_create
    game_event[T_TEMP_GAME_EVENT_ON_DESTROY] = on_destroy

    # do on create callback
    game_event_execute_callback(game_event, T_TEMP_GAME_EVENT_ON_CREATE)

    log_debug(f"[temporary_game_event_register] registered temporary game event for phase: {phase}, extra callbacks: ")
    log_debug(f"{on_create=}, {on_destroy=}")

    return game_event

def temporary_game_event_unregister(event_system: GameEventSystemT, game_event: GameEventT):
    # do on destroy callback
    game_event_execute_callback(game_event, T_TEMP_GAME_EVENT_ON_DESTROY)

    game_event_unregister(event_system, game_event)

