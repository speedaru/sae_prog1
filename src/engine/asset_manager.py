import os
from pathlib import Path
from sys import version_info
from tkinter import PhotoImage
from types import NoneType

import libs.fltk as fltk

from src.utils.logging import *


# relative to current file path: ../../assets/blocks.png
ASSETS_DIR = os.path.join(Path(__file__).parent, "..", "..", "assets")

WINDOW_ICON_PATH = os.path.join(ASSETS_DIR, "logo", "game_icon.ico")

# constants
BLOCK_SIZE = (64, 64)
BLOCK_SCALE = 2
BLOCK_SCALED_SIZE = (BLOCK_SIZE[0] * BLOCK_SCALE, BLOCK_SIZE[1] * BLOCK_SCALE)

# types
BlockT = list[PhotoImage]
BlockListT = list[BlockT]

# enum for blocks since we're not allowed to use real enums
BLOCK_SOLID = 0
BLOCK_SINGLE = 1
BLOCK_DOUBLE_ADJACENT = 2
BLOCK_DOUBLE_OPPOSITE = 3
BLOCK_TRIPLE = 4
BLOCK_QUAD = 5
BLOCK_WALL_BACKGROUND = 6
BLOCK_COUNT = 7 # not real index, just count of blocks

# max rotations for each block image in order
BLOCK_MAX_ROTATIONS = (1, 4, 4, 2, 4, 1, 1)

def asset_manager_init() -> BlockListT:
    ASSET_FILE_NAMES = ("block_solid.png", "block_single.png", "block_double_adjacent.png",
                        "block_double_opposite.png", "block_triple.png", "block_quad.png",
                        "wall_background.png")

    # reserve space so we can use index directly instead of using append()
    blocks = [[PhotoImage()] * states_count for states_count in BLOCK_MAX_ROTATIONS]

    for block_id, asset_file_name in enumerate(ASSET_FILE_NAMES):
        # for each block loop over each different state
        for states_count in range(BLOCK_MAX_ROTATIONS[block_id]):
            # different states are just stored in _x.png files
            asset_path = os.path.join(ASSETS_DIR, asset_file_name)
            asset_path = asset_path.replace(".png", f"_{states_count + 1}.png")

            blocks[block_id][states_count] = \
                    fltk._load_tk_image(asset_path, BLOCK_SCALED_SIZE[0], BLOCK_SCALED_SIZE[1])

    return blocks

def asset_manager_initialized(blocks: list[BlockT] | list[NoneType]) -> bool:
    return len(blocks) == BLOCK_COUNT

# for block use a variable like BLOCK_
def asset_manager_get_block(blocks: list[BlockT] | list[NoneType], block_idx: int, rotation_count: int) -> PhotoImage | NoneType:
    if not asset_manager_initialized(blocks):
        return None

    log_debug_full(f"[asset_manger] getting block: {block_idx}")
    if block_idx >= len(blocks): # out of bounds check
        log_debug(f"[asset_manager] failed to get block: {block_idx} (out of bounds, block count: {len(_blocks)})")
        return None

    block: BlockT | NoneType = blocks[block_idx] 

    # check invalid
    if isinstance(block, NoneType):
        return None

    return block[rotation_count % len(block)]
