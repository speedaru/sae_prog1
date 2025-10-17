import time

import libs.fltk as fltk

from src.utils.logging import log_release, log_debug, log_debug_full
import src.engine.engine_config as engine_config
import src.game.game_config as game_config
import src.engine.fps_manager as fps_manager
import src.game.gui as gui


def render():
    pass

def main_loop():
    last_frame_start = 0

    fps_interval_s: float = fps_manager.get_target_fps_interval_ms(engine_config.TARGET_FPS) / 1000
    log_debug_full(f"target fps interval ms: {fps_interval_s}")

    gui.create_window()

    while True:
        last_frame_start = fps_manager.get_ctime_ms()

        # exit game
        if fltk.touche_pressee(game_config.EXIT_KEY):
            break

        gui.start_render()
        render()
        gui.render()

        time.sleep(fps_interval_s)
        log_debug_full(f"fps: {fps_manager.get_fps_count(last_frame_start)}")
