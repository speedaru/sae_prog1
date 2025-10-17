import time

from src.utils.logging import log_release, log_debug, log_debug_full
import src.engine.engine_config as engine_config
import src.engine.fps_manager as fps_manager
import src.game.gui as gui


def main_loop():
    last_frame_start = 0

    fps_interval_s: float = fps_manager.get_target_fps_interval_ms(engine_config.TARGET_FPS) / 1000
    log_debug(f"target fps interval ms: {fps_interval_s}")

    while True:
        last_frame_start = fps_manager.get_ctime_ms()

        gui.start_render()
        gui.render()
        gui.end_render()

        time.sleep(fps_interval_s)
        log_debug(f"fps: {fps_manager.get_fps_count(last_frame_start)}")
