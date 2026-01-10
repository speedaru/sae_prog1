import time

import src.engine.engine_config as engine_config


# to handle time asynchronously between frames
# otherwise if we sleep 3 seconds, we cant handle any event during the 3 seconds
FpsManagerT = list[float | bool]

T_FPS_MANAGER_CURRENT_FRAME_TIME = 0
T_FPS_MANAGER_LAST_FRAME_TIME = 1
T_FPS_MANAGER_LAST_HANDLED_FRAME = 2
T_FPS_MANAGER_SLEEP_TARGET = 3
T_FPS_MANAGER_SLEEPING = 4
T_FPS_MANAGER_COUNT = 5

def fps_manager_create(current_frame_time: float = 0):
    if current_frame_time == 0:
        current_frame_time = time.time()

    fps_manager: FpsManagerT = [None] * T_FPS_MANAGER_COUNT

    fps_manager[T_FPS_MANAGER_CURRENT_FRAME_TIME] = current_frame_time
    fps_manager[T_FPS_MANAGER_LAST_FRAME_TIME] = current_frame_time
    fps_manager[T_FPS_MANAGER_LAST_HANDLED_FRAME] = current_frame_time
    fps_manager[T_FPS_MANAGER_SLEEP_TARGET] = 0.0 # sleep target set at 0, then set manually
    fps_manager[T_FPS_MANAGER_SLEEPING] = False

    return fps_manager

def fps_manager_is_sleeping(fps_manager: FpsManagerT) -> bool:
    return fps_manager[T_FPS_MANAGER_SLEEPING]

def fps_manager_slept_enough(fps_manager: FpsManagerT) -> bool:
    """
    if finished sleeping then set sleeping back to False
    returns: True if currently sleeping but finished sleeping
    """
    if not fps_manager[T_FPS_MANAGER_SLEEPING]:
        return False

    dt = calculate_delta_time(fps_manager[T_FPS_MANAGER_CURRENT_FRAME_TIME], fps_manager[T_FPS_MANAGER_LAST_HANDLED_FRAME])
    target_dt = fps_manager[T_FPS_MANAGER_SLEEP_TARGET]

    slept_enough = (dt - target_dt) > 0

    # reset sleeping bool and sleep target to originals before sleep
    if slept_enough: 
        fps_manager[T_FPS_MANAGER_SLEEPING] = False
        fps_manager[T_FPS_MANAGER_SLEEP_TARGET] = 0.0

        # reset handled frame so next sleep starts now
        fps_manager_handled_frame(fps_manager)

    return slept_enough

def fps_manager_game_sleep(fps_manager: FpsManagerT, time_to_sleep: float):
    """
    sleeps asynchronously by not doing game logic if sleeping. but can still handle events
    !!! WARNING !!! this function should only be called from game_sleep to not mess up GameEventSystemT
    """
    fps_manager[T_FPS_MANAGER_SLEEP_TARGET] = time_to_sleep
    fps_manager[T_FPS_MANAGER_SLEEPING] = True

def fps_manager_handled_frame(fps_manager: FpsManagerT):
    """
    cant handle frame if sleeping
    """
    fps_manager[T_FPS_MANAGER_LAST_HANDLED_FRAME] = fps_manager[T_FPS_MANAGER_CURRENT_FRAME_TIME]


def calculate_delta_time(current_time_s: float, last_update_time_s: float) -> float:
    """
    Calculates Delta Time (dt): the time elapsed since the last call 
    to this function, and updates the internal tracking variable.
    
    Returns:
        float: Delta time in seconds.
    """
    # Delta Time = Current Time - Time of Last Frame
    delta_time_s = current_time_s - last_update_time_s
    
    return delta_time_s

def calculate_fps(delta_time_s: float) -> int:
    """
    Calculates the current FPS based on the last calculated Delta Time.
    
    Args:
        delta_time_s (float): The delta time from the last frame.
        
    Returns:
        int: Frames per second.
    """
    if delta_time_s == 0:
        return 0
    return round(1.0 / delta_time_s)

def sleep_to_cap_fps(delta_time_s: float):
    """
    Calculates the required sleep duration to cap the frame rate
    at the TARGET_FPS.
    
    Args:
        delta_time_s (float): The actual time taken to process the current frame 
                              (logic and rendering).
    """
    
    # Calculate how much time is left in the target frame budget
    time_spent = delta_time_s
    time_left_to_sleep = engine_config.TARGET_FRAME_TIME_S - time_spent

    # Only sleep if we finished the work faster than the target time
    if time_left_to_sleep > 0:
        time.sleep(time_left_to_sleep)
