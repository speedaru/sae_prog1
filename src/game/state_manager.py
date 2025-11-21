import libs.fltk as fltk

GameStateT = int

STATE_MENU_START = 0
STATE_GAME_TURN_DUNGEON = 1
STATE_GAME_TURN_PLAYER = 2
STATE_GAME_DONE_WON = 3
STATE_GAME_DONE_LOST = 4
STATE_EXIT = 5
STATE_COUNT = 6


def game_state_render(game_state: GameStateT):
    TEXT_POS = (10, 5)

    state_text = ""
    if game_state == STATE_MENU_START:
        state_text = "Menu"
    elif game_state == STATE_GAME_TURN_PLAYER:
        state_text = "Tour de l'aventurier"
    elif game_state == STATE_GAME_TURN_DUNGEON:
        state_text = "Tour du donjon"

    # no state to show
    if state_text == "":
        return

    fltk.texte(TEXT_POS[0], TEXT_POS[1], state_text, couleur='lime', taille=18)
