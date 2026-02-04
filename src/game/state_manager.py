import libs.fltk as fltk


# game flags to indicate the game staet
GameFlags = int

F_GAME_TURN_DUNGEON =        1 << 0  # if set means its the dungeons turn, so we can rotate the blocks and stuff
F_GAME_TURN_PLAYER =         1 << 1  # if set means its the players turn, obsolete if we dont draw the path manually
F_GAME_GAME_FINISHED =       1 << 2  # game is finished and we can draw the end screen message
F_GAME_GAME_WON =            1 << 3  # game is finished and won
F_GAME_GAME_LOST =           1 << 4  # game is finished and lost
F_GAME_ADVENTURER_MOVING =   1 << 5  # adventurer is currently moving
F_GAME_HANDLE_EVENTS =       1 << 6  # dont handle game input events
F_GAME_UPDATE_PATH =         1 << 7  # if set means we need to recalculate the adventurer path
F_GAME_RANDOM_DUNGEON =      1 << 8  # random dungeon menu selector
F_GAME_EXIT_PROGRAM =        1 << 16 # exit program after we finish the current main loop iteration

GAME_FLAGS_STARTUP = F_GAME_HANDLE_EVENTS
GAME_FLAGS_GAME_START = F_GAME_HANDLE_EVENTS | F_GAME_UPDATE_PATH | F_GAME_TURN_DUNGEON

# window enum, like start menu, game menu, ...
WindowE = int
E_WINDOW_START = 0
E_WINDOW_GAME = 1
E_WINDOW_RANDOM_DUNGEON = 2

def get_game_state_text(game_flags: GameFlags) -> str:
    state_text = ""
    if game_flags & F_GAME_ADVENTURER_MOVING:
        state_text = "Déplacement de l'aventurier"
    elif game_flags & F_GAME_TURN_PLAYER:
        state_text = "Tour de l'aventurier"
    elif game_flags & F_GAME_TURN_DUNGEON:
        state_text = "Tour du donjon"

    return state_text

