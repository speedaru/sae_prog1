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

CHARACTERS_SIZES = (64, 64)

# types
BlockT = list[PhotoImage]
BlockListT = list[BlockT]
CharacterT = PhotoImage
CharacterListT = list[CharacterT]
AssetsT = list[BlockListT | CharacterListT]

# enum for blocks since we're not allowed to use real enums
BLOCK_SOLID = 0
BLOCK_SINGLE = 1
BLOCK_DOUBLE_ADJACENT = 2
BLOCK_DOUBLE_OPPOSITE = 3
BLOCK_TRIPLE = 4
BLOCK_QUAD = 5
BLOCK_WALL_BACKGROUND = 6
BLOCK_COUNT = 7 # not real index, just count of blocks

# enum for characters
CHARACTERS_ADVENTURER = 0
CHARACTERS_DRAGONS = 1
CHARACTERS_COUNT = 2

# enum for assets list
ASSETS_BLOCKS = 0
ASSETS_CHARACTERS = 1
ASSETS_COUNT = 2

# max rotations for each block image in order
BLOCK_MAX_ROTATIONS = (1, 4, 4, 2, 4, 1, 1)

def asset_manager_init() -> AssetsT:
    BLOCK_FILE_NAMES = ("block_solid.png", "block_single.png", "block_double_adjacent.png",
                        "block_double_opposite.png", "block_triple.png", "block_quad.png",
                        "wall_background.png")

    CHARARCTERS_FILE_NAMES = ("knight.png", "dragon.png")

    # reserve space so we can use index directly instead of using append()
    blocks = [[PhotoImage()] * states_count for states_count in BLOCK_MAX_ROTATIONS]
    characters = [PhotoImage()] * CHARACTERS_COUNT # knight and dragons
    assets: AssetsT = [list()] * ASSETS_COUNT # blocks and characters

    # load blocks
    for block_id, asset_file_name in enumerate(BLOCK_FILE_NAMES):
        # for each block loop over each different state
        for states_count in range(BLOCK_MAX_ROTATIONS[block_id]):
            # different states are just stored in _x.png files
            asset_path = os.path.join(ASSETS_DIR, asset_file_name)
            asset_path = asset_path.replace(".png", f"_{states_count + 1}.png")

            blocks[block_id][states_count] = \
                    fltk._load_tk_image(asset_path, BLOCK_SCALED_SIZE[0], BLOCK_SCALED_SIZE[1])

    # load characters
    for character in range(CHARACTERS_COUNT):
        image = os.path.join(ASSETS_DIR, CHARARCTERS_FILE_NAMES[character])
        characters[character] = fltk._load_tk_image(image, CHARACTERS_SIZES[0], CHARACTERS_SIZES[0])

    assets[ASSETS_BLOCKS] = blocks
    assets[ASSETS_CHARACTERS] = characters

    return assets

def asset_manager_initialized(assets: AssetsT) -> bool:
    # checks lenght of assets
    assets_count = len(assets)
    if assets_count != ASSETS_COUNT:
        return False

    # check length of blocks
    blocks = assets[ASSETS_BLOCKS]
    blocks_count = len(blocks)
    if blocks_count != BLOCK_COUNT:
        return False

    # check length of characters
    characters = assets[ASSETS_CHARACTERS]
    characters_count = len(characters)
    if characters_count != CHARACTERS_COUNT:
        return False

    return True

# for block use a variable like BLOCK_
def asset_manager_get_block(assets: AssetsT, block_idx: int, rotation_count: int) -> PhotoImage | NoneType:
    if not asset_manager_initialized(assets):
        return None

    blocks: BlockListT = assets[ASSETS_BLOCKS]

    log_debug_full(f"[asset_manger] getting block: {block_idx}")
    if block_idx >= len(blocks): # out of bounds check
        log_debug(f"[asset_manager] failed to get block: {block_idx} (out of bounds, block count: {len(blocks)})")
        return None

    block: BlockT | NoneType = blocks[block_idx] 

    # check invalid
    if isinstance(block, NoneType):
        return None

    return block[rotation_count % len(block)]
