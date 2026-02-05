from src.engine.structs.dungeon import *
from src.engine.asset_manager import BLOCK_SCALED_SIZE

# pos: pos to check
# tl, br: top-left, bottom-right
def in_rectangle(pos: tuple[int, int], tl: tuple[int, int], br: tuple[int, int]) -> bool:
    """
    Checks if a position is inside a rectangle defined by its top-left and bottom-right corners.

    Args:
        pos (tuple[int, int]): The position to check (x, y).
        tl (tuple[int, int]): The top-left corner of the rectangle (x, y).
        br (tuple[int, int]): The bottom-right corner of the rectangle (x, y).

    Returns:
        bool: True if the position is inside or on the edges of the rectangle, False otherwise.
    """
    x, y = pos
    x1, y1 = tl
    x2, y2 = br

    return x1 <= x <= x2 and y1 <= y <= y2

def get_room_tl_screen_pos(room_pos: RoomPosT) -> tuple[int, int]:
    """
    return screen coordinates x, y of rooms top left coordinates
    """
    return (room_pos[ROOM_POS_COL] * BLOCK_SCALED_SIZE[0], room_pos[ROOM_POS_ROW] * BLOCK_SCALED_SIZE[1])
