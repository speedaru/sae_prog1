import time

import src.engine.engine_config as engine_config

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
