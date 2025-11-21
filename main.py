import src.game.main_game as main_game


def main():
    """
    Entry point of the Wall Is You game.

    This function delegates the execution to the main game loop defined in
    the `src.game.main_game` module. It initializes the game components
    and starts the event processing loop.
    """
    main_game.main_loop()


if __name__ == "__main__":
    main()
