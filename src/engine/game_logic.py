from os import path
import src.engine.pathfinding as pathfinding
from src.engine.structs.dungeon import *
from src.engine.structs.entity import *
from src.engine.structs.adventurer import *
from src.engine.structs.dragon import *
from src.engine.event_info import *

from src.game.game_config import *


def rotate_room(event_info: EventInfoT, game_context: GameContextT):
    ev: FltkEvent = event_info[EVENT_INFO_EV]
    click_postion = fltk_ext.position_souris(ev)

    # rotate room at click positons
    clicked_room_col = click_postion[0] // BLOCK_SCALED_SIZE[0]
    clicked_room_row = click_postion[1] // BLOCK_SCALED_SIZE[1]

    # if cursor outside of dungeon do nothing
    dungeon: DungeonT = game_context[GAME_CONTEXT_DUNGEON]
    if clicked_room_col >= dungeon_get_width(dungeon) or clicked_room_row >= dungeon_get_height(dungeon):
        return False

    dungeon_rotate_room(dungeon, clicked_room_row, clicked_room_col)

def manually_update_player_path(event_info: EventInfoT, game_context: GameContextT):
    ev: FltkEvent = event_info[EVENT_INFO_EV]
    click_postion = fltk_ext.position_souris(ev)

    # rotate room at click positons
    clicked_room_col: int = click_postion[0] // BLOCK_SCALED_SIZE[0]
    clicked_room_row: int = click_postion[1] // BLOCK_SCALED_SIZE[1]
    clicked_room: RoomPosT = (clicked_room_row, clicked_room_col)

    # if cursor outside of dungeon do nothing
    dungeon: DungeonT = game_context[GAME_CONTEXT_DUNGEON]
    if clicked_room_col >= dungeon_get_width(dungeon) or clicked_room_row >= dungeon_get_height(dungeon):
        return False

    # if clicked room not adjacent then dont add it to path

    # add selected room to path
    adventurer: AdventurerT = game_context[GAME_CONTEXT_ADVENTURER]
    movement_path: MovementPathT = adventurer[ADVENTURER_PATH]
    movement_path.append(clicked_room)

def do_dungeon_turn(game_context: GameContextT):
    adventurer: AdventurerT = game_context[GAME_CONTEXT_ADVENTURER]
    dragons: list[DragonT] = game_context[GAME_CONTEXT_DRAGONS]

    pathfinding.find_and_set_adventurer_path(adventurer, dragons)
    pathfinding.do_adventurer_path(adventurer)
