from src.engine.structs.temporary_game_event import *

from src.game.game_definitions import *
from src.game.game_events.chaos_seal import *

from src.utils.logging import *


# save the state of a temporary_game_event so we can 
SavedTempEventT = TemporaryGameEventT

T_SAVED_TEMP_EVENT_TYPE         = 0 # TempEventE
T_SAVED_TEMP_EVENT_PHASE        = 1 # GamePhaseE
T_SAVED_TEMP_EVENT_DURATION     = 2 # int, duration left
T_SAVED_TEMP_EVENT_FLAGS        = 3 # int, game event flags
T_SAVED_TEMP_EVENT_SIZE         = 4 # int, struct size
T_SAVED_TEMP_EVENT_EXTRA_DATA   = 5 # list of child data (anything at or after T_TEMP_GAME_EVENT_COUNT)
T_SAVED_TEMP_EVENT_COUNT        = 6

def temporary_game_event_save(temp_game_event: TemporaryGameEventT, phase: GamePhaseE) -> SavedTempEventT:
    saved_temp_event: SavedTempEventT = [None] * T_SAVED_TEMP_EVENT_COUNT
    
    saved_temp_event[T_SAVED_TEMP_EVENT_TYPE] = temp_game_event[T_TEMP_GAME_EVENT_TYPE]
    saved_temp_event[T_SAVED_TEMP_EVENT_PHASE] = phase
    saved_temp_event[T_SAVED_TEMP_EVENT_DURATION] = temp_game_event[T_GAME_EVENT_DURATION]
    saved_temp_event[T_SAVED_TEMP_EVENT_FLAGS] = temp_game_event[T_GAME_EVENT_FLAGS]
    saved_temp_event[T_SAVED_TEMP_EVENT_SIZE] = len(temp_game_event)

    # save extra child data in a sublist
    if len(temp_game_event) > T_TEMP_GAME_EVENT_COUNT:
        saved_temp_event[T_SAVED_TEMP_EVENT_EXTRA_DATA] = temp_game_event[T_TEMP_GAME_EVENT_COUNT:]

    log_debug(f"saved temp event for phase: {saved_temp_event[T_SAVED_TEMP_EVENT_TYPE]}")
    return saved_temp_event

def temporary_game_event_save_events(event_system: GameEventSystemT) -> list[SavedTempEventT]:
    saved_events = []

    for phase, phase_events in enumerate(event_system):
        for game_event in phase_events:
            # only save temp events
            if not game_event_system_is_temporary_game_event(game_event):
                log_debug(f"not temp event, {game_event[T_GAME_EVENT_ON_FRAME]}")
                continue

            # save temp event
            log_debug(f"temp game event type: {game_event[T_TEMP_GAME_EVENT_TYPE]}")
            saved_events.append(temporary_game_event_save(game_event, phase))

    return saved_events

def temporary_game_event_load(game_context: GameContextT, saved_temp_event: SavedTempEventT):
    """
    registers temporary game event from SavedTempEventT
    """
    event_system: GameEventSystemT = game_context[T_GAME_CTX_GAME_DATA][T_GAME_DATA_EVENT_SYSTEM]
    log_debug(f"[temporary_game_event_load] saved_temp_ev: {saved_temp_event}")

    temp_game_event = None
    callbacks: TempEventCallbacksT | NoneType = None

    temp_event_type: TempEventE = saved_temp_event[T_SAVED_TEMP_EVENT_TYPE]
    if temp_event_type == E_TEMP_EVENT_CHAOS_SEAL:
        callbacks = chaos_seal_get_callbacks()
        log_debug(f"got chaos seal callbacks")

    # invalid event type
    if callbacks == None:
        log_warning(f"trying to load unknown saved temp event type: {temp_event_type}")
        return

    # register temp event
    temp_game_event = temporary_game_event_register(event_system=event_system,
                                                    phase=saved_temp_event[T_SAVED_TEMP_EVENT_PHASE],
                                                    duration=saved_temp_event[T_SAVED_TEMP_EVENT_DURATION],
                                                    on_create=callbacks[T_TEMP_EVENT_CALLBACKS_ON_CREATE],
                                                    on_frame=callbacks[T_TEMP_EVENT_CALLBACKS_ON_FRAME],
                                                    on_round_end=callbacks[T_TEMP_EVENT_CALLBACKS_ON_ROUND_END],
                                                    on_destroy=callbacks[T_TEMP_EVENT_CALLBACKS_ON_DESTROY],
                                                    temp_event_type=temp_event_type,
                                                    flags=saved_temp_event[T_SAVED_TEMP_EVENT_FLAGS],
                                                    game_ctx=game_context,
                                                    size=saved_temp_event[T_SAVED_TEMP_EVENT_SIZE])

    # load game data
    temp_game_event[T_GAME_EVENT_GAME_CTX] = game_context

    # set other extra game info
    child_class_base = T_TEMP_GAME_EVENT_COUNT
    for i, val in enumerate(saved_temp_event[T_SAVED_TEMP_EVENT_EXTRA_DATA]):
        temp_game_event[child_class_base + i] = val
