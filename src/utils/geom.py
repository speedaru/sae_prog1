

# pos: pos to check
# tl, br: top-left, bottom-right
def in_rectangle(pos: tuple[int, int], tl: tuple[int, int], br: tuple[int, int]) -> bool:
    x, y = pos
    x1, y1 = tl
    x2, y2 = br

    return x1 <= x <= x2 and y1 <= y <= y2
