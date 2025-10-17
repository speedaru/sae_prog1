import time

import src.engine.engine_config as engine_config


def get_ctime_ms() -> float:
    ctime_ns = time.time_ns()
    return ctime_ns / 1_000_000 # conversion NS -> MS

# returns target ms to sleep in order to run at TARGET_FPS
def get_target_fps_interval_ms(target_fps: int):
    return (1 / target_fps) * 1000 # *1000 to get in ms

def sleep_cap_fps(last_frame_start_ms: float):
    ctime_ms = get_ctime_ms()
    diff_ms = ctime_ms - last_frame_start_ms
    ms_to_sleep = diff_ms - get_target_fps_interval_ms(engine_config.TARGET_FPS)

    # only sleep if executing code too fast
    if ms_to_sleep > 0:
        time.sleep(ms_to_sleep / 1000) # convert to seconds

def get_fps_count(last_frame_start_ms: float) -> int:
    # print(f"ctime: {get_ctime_ms()} | last_frame_start_ms: {last_frame_start_ms}")
    return round(1000 / (get_ctime_ms() - last_frame_start_ms))

