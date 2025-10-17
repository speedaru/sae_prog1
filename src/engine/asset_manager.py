import os
from pathlib import Path
from sys import version_info
from tkinter import PhotoImage
from types import NoneType

import libs.fltk as fltk

from src.utils.logging import *


# relative to current file path: ../../assets/blocks.png
ASSETS_DIR = os.path.join(Path(__file__).parent, "..", "..", "assets")

_blocks: list[PhotoImage] | list[NoneType] = list()

# enum for blocks since we're not allowed to use real enums
BLOCK_SOLID = 0
BLOCK_SINGLE = 1
BLOCK_DOUBLE_ADJACENT = 2
BLOCK_DOUBLE_OPPOSITE = 3
BLOCK_TRIPLE = 4
BLOCK_QUAD = 5
BLOCK_COUNT = 6 # not real index, just count of blocks

def asset_manager_init():
    global _blocks

    BLOCK_SIZE = (64, 64)
    BLOCK_SCALE = 2
    ASSET_IMAGE_SIZE = (192, 128)

    HORIZONTAL_BLOCK_COUNT = ASSET_IMAGE_SIZE[0] // BLOCK_SIZE[0]
    VERTICAL_BLOCK_COUNT = ASSET_IMAGE_SIZE[1] // BLOCK_SIZE[1]

    ASSET_FILE_NAMES = ("block_solid.png", "block_single.png", "block_double_adjacent.png",
                        "block_double_opposite.png", "block_triple.png", "block_quad.png")

    # reserve space so we can use index directly instead of using append()
    _blocks = [PhotoImage()] * (HORIZONTAL_BLOCK_COUNT * VERTICAL_BLOCK_COUNT)

    for i in range(HORIZONTAL_BLOCK_COUNT):
        for j in range(VERTICAL_BLOCK_COUNT):
            asset_path = os.path.join(ASSETS_DIR, ASSET_FILE_NAMES[i + j])
            _blocks[i + j] = fltk._load_tk_image(asset_path, BLOCK_SIZE[0] * BLOCK_SCALE, BLOCK_SIZE[1] * BLOCK_SCALE)

def asset_manager_initialized() -> bool:
    return len(_blocks) == BLOCK_COUNT

# for BLOCK use a variable like BLOCK_
def asset_manager_get_block(BLOCK: int) -> PhotoImage | NoneType:
    log_debug_full(f"[asset_manger] getting block: {BLOCK}")
    if BLOCK >= len(_blocks): # out of bounds check
        log_debug(f"[asset_manager] failed to get block: {BLOCK} (out of bounds, block count: {len(_blocks)})")
        return None

    return _blocks[BLOCK];
