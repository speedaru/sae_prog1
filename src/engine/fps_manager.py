import time

import src.engine.engine_config as engine_config


def get_ctime_ms() -> float:
    """
    Gets the current system time in milliseconds.

    Returns:
        float: The current time in milliseconds (converted from nanoseconds).
    """
    ctime_ns = time.time_ns()
    return ctime_ns / 1_000_000 # conversion NS -> MS

# returns target ms to sleep in order to run at TARGET_FPS
def get_target_fps_interval_ms(target_fps: int):
    """
    Calculates the time interval required for one frame to reach the target FPS.

    Args:
        target_fps (int): The desired frames per second.

    Returns:
        float: The duration of a single frame in milliseconds.
    """
    return (1 / target_fps) * 1000 # *1000 to get in ms

def sleep_cap_fps(last_frame_start_ms: float):
    """
    Pauses execution to cap the application's framerate.

    Calculates the time elapsed since the start of the last frame and sleeps
    if the frame completed faster than the target interval.

    Args:
        last_frame_start_ms (float): The timestamp (in ms) when the current frame started.
    """
    ctime_ms = get_ctime_ms()
    diff_ms = ctime_ms - last_frame_start_ms
    ms_to_sleep = diff_ms - get_target_fps_interval_ms(engine_config.TARGET_FPS)

    # only sleep if executing code too fast
    if ms_to_sleep > 0:
        time.sleep(ms_to_sleep / 1000) # convert to seconds

def get_fps_count(last_frame_start_ms: float) -> int:
    """
    Calculates the current frames per second (FPS).

    Args:
        last_frame_start_ms (float): The timestamp (in ms) when the last frame started.

    Returns:
        int: The estimated FPS based on the time difference between now and the last frame.
    """
    # print(f"ctime: {get_ctime_ms()} | last_frame_start_ms: {last_frame_start_ms}")
    return round(1000 / (get_ctime_ms() - last_frame_start_ms))

