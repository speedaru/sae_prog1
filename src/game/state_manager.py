import libs.fltk as fltk

# game flags to indicate the game staet
GameFlags = int

F_GAME_MENU =                1 << 0  # if set means we're in the start menu
F_GAME_GAME =                1 << 1  # if set means we're in the main game screen
F_GAME_TURN_DUNGEON =        1 << 2  # if set means its the dungeons turn, so we can rotate the blocks and stuff
F_GAME_TURN_PLAYER =         1 << 3  # if set means its the players turn, obsolete if we dont draw the path manually
F_GAME_GAME_FINISHED =       1 << 4  # game is finished and we can draw the end screen message
F_GAME_GAME_WON =            1 << 5  # game is finished and won
F_GAME_GAME_LOST =           1 << 6  # game is finished and lost
F_GAME_ADVENTURER_MOVING =   1 << 7  # adventurer is currently moving
F_GAME_HANDLE_EVENTS =       1 << 8  # dont handle game input events
F_GAME_UPDATE_PATH =         1 << 9  # if set means we need to recalculate the adventurer path
F_GAME_EXIT_PROGRAM =        1 << 16 # exit program after we finish the current main loop iteration

GAME_FLAGS_STARTUP_FLAGS = F_GAME_MENU | F_GAME_HANDLE_EVENTS

def get_game_state_text(game_flags: GameFlags) -> str:
    state_text = ""
    if game_flags & F_GAME_MENU:
        state_text = "Menu"
    elif game_flags & F_GAME_ADVENTURER_MOVING:
        state_text = "Déplacement de l'aventurier"
    elif game_flags & F_GAME_TURN_PLAYER:
        state_text = "Tour de l'aventurier"
    elif game_flags & F_GAME_TURN_DUNGEON:
        state_text = "Tour du donjon"

    return state_text
