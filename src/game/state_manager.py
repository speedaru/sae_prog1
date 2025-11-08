STATE_MENU_START = 0
STATE_GAME_DUNGEON = 1
STATE_COUNT = 2

_current_state = STATE_MENU_START

# returns local game state
def get_game_state() -> int:
    global _current_state
    return _current_state

# update game state (checks for invalid states)
def set_game_state(new_game_state: int):
    global _current_state

    # return if new_state is not a valid state
    if new_game_state < 0 or new_game_state >= STATE_COUNT:
        return

    _current_state = new_game_state
