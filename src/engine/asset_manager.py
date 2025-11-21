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
    """
    Initializes the game asset manager by loading all necessary images from disk.

    This function:
    1. Defines the file names for blocks and characters.
    2. Pre-allocates lists for blocks and characters based on defined counts.
    3. Iterates through block types and their rotation states (suffix `_x.png`), loading them into `PhotoImage` objects.
    4. Loads character images (knight, dragons).
    5. Scales images to the configured sizes.

    Returns:
        AssetsT: A list structure organized by constants:
                 - `assets[ASSETS_BLOCKS]`: A list of block images (each element is a list of rotations).
                 - `assets[ASSETS_CHARACTERS]`: A list of character images.
    """
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
    """
    Verifies if the asset manager structure has been correctly initialized.

    Args:
        assets (AssetsT): The asset structure to check.

    Returns:
        bool: True if the structure matches the expected format (correct number of asset categories
              defined by `ASSETS_COUNT`, `BLOCK_COUNT`, and `CHARACTERS_COUNT`). False otherwise.
    """
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
    """
    Retrieves the image for a specific block type at a specific rotation.

    Args:
        assets (AssetsT): The initialized asset structure.
        block_idx (int): The index of the block type (e.g., `BLOCK_SOLID`, `BLOCK_SINGLE`).
        rotation_count (int): The number of 90-degree clockwise rotations.
                              The function uses modulo arithmetic to map this to a valid image state.

    Returns:
        PhotoImage | NoneType: The tkinter PhotoImage object for the requested block,
                               or None if the assets are not initialized, the index is out of bounds,
                               or the block data is invalid.
    """
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
