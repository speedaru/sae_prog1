"""
event system to queue game events, like queue event that lasts 3 rounds
and do stuff on event start, event ends and event round tick
this way we can handle events in a simple way instead of manually adding stuff
to GameDataT struct and modifying the code constantly.
"""
from src.engine.structs.game_event import *
from src.engine.structs.temporary_game_event import *


# -------------------- private functions

def _game_event_system_remove_completed(event_system: GameEventSystemT, event):
    # event not completed
    if not (event[T_GAME_EVENT_FLAGS] & F_GAME_EVENT_COMPLETED):
        return

    # is temp event
    if game_event_system_is_temporary_game_event(event):
        temporary_game_event_unregister(event_system, event)
    # is regular event
    else:
        game_event_unregister(event_system, event)

def _game_event_system_remove_completed_events(event_system: GameEventSystemT):
    for phase_events in event_system:
        for event in phase_events:
            _game_event_system_remove_completed(event_system, event)

def _remove_event_by_id(event_system: GameEventSystemT, event_id: int):
    # find phase and idx in which event is
    phase = None
    idx = None
    for current_phase, phase_events in enumerate(event_system):
        found = False
        for i, event in enumerate(phase_events):
            if event[T_GAME_EVENT_ID] == event_id:
                phase, idx = current_phase, i
                found = True
                break
        if found:
            break

    # event_id not found
    if phase == None or idx == None:
        log_error(f"[_game_event_unregister] event_id {event_id} not found")
        return
    
    # pop event from phase sublist
    event_system[phase].pop(idx)

# -------------------- public api

def game_event_system_create():
    # bcs its just a list
    return [list() for _ in range(E_PHASE_COUNT)]

# def game_event_system_is_phase_paused(event_system: GameEventSystemT, phase: GamePhaseE) -> bool:
#     flags: int = event_system[phase][T_GAME_EVENT_FLAGS]
#     return bool(flags & F_GAME_EVENT_PAUSED)

def game_event_system_is_temporary_game_event(game_event):
    # >= cuz can be child of other higher classes
    return len(game_event) >= T_TEMP_GAME_EVENT_COUNT

def game_event_system_pause_phase(event_system: GameEventSystemT, phase: GamePhaseE):
    for event in event_system[phase]:
        event[T_GAME_EVENT_FLAGS] |= F_GAME_EVENT_PAUSED

def game_event_system_unpause_phase(event_system: GameEventSystemT, phase: GamePhaseE):
    for event in event_system[phase]:
        event[T_GAME_EVENT_FLAGS] &= ~F_GAME_EVENT_PAUSED

def game_event_system_frame_tick(event_system: GameEventSystemT):
    """
    expected to get called every frame (when we draw game)
    """
    log_rendering(f"running per frame logic")

    for phase_events in event_system:
        for game_event in phase_events:
            # skip event if paused
            if game_event[T_GAME_EVENT_FLAGS] & F_GAME_EVENT_PAUSED:
                log_rendering(f"NOT DOING PER FRAME LOGIC BCS SLEEPING: {game_event[T_GAME_EVENT_ON_FRAME]}")
                continue
            
            # execute frame tick callback
            game_event_execute_callback(game_event, T_GAME_EVENT_ON_FRAME)

def game_event_system_round_tick(event_system: GameEventSystemT):
    """
    expected to get called only when round ends and round counter is incremented
    """
    log_rendering(f"running per round logic")

    for phase_events in event_system:
        i = 0
        while i < len(phase_events):
            game_event = phase_events[i]
            i += 1

            # skip event if paused
            if game_event[T_GAME_EVENT_FLAGS] & F_GAME_EVENT_PAUSED:
                log_rendering(f"NOT DOING PER ROUND LOGIC BCS SLEEPING: {game_event[T_GAME_EVENT_ON_ROUND_END]}")
                continue
            
            # execute round tick callback
            game_event_execute_callback(game_event, T_GAME_EVENT_ON_ROUND_END)

            # decrease duration if not perpetual bcs round decreased
            if not game_event_is_perpertual(game_event):
                # decrease duration
                if game_event[T_GAME_EVENT_DURATION] >= 0:
                    game_event[T_GAME_EVENT_DURATION] -= 1

                # set completed flag if no more rounds left to do
                if game_event[T_GAME_EVENT_DURATION] < 0 and not game_event_is_perpertual(game_event):
                    game_event[T_GAME_EVENT_FLAGS] |= F_GAME_EVENT_COMPLETED

            # remove current event if finished
            _game_event_system_remove_completed(event_system, game_event)
