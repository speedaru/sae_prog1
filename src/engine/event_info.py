from types import NoneType

import libs.fltk as fltk
from libs.fltk import FltkEvent

from src.game.game_definitions import *

import src.utils.fltk_extensions as fltk_ext


InputEventInfoT = list[FltkEvent | str | NoneType | bool]

INPUT_EVENT_INFO_EV = 0      # FltkEvent
INPUT_EVENT_INFO_TYPE = 1    # optional str
INPUT_EVENT_INFO_IS_KEY = 2  # bool
INPUT_EVENT_INFO_KEY_PRESSED = 3 # str
INPUT_EVENT_INFO_COUNT = 4


# get info on event, such as if is key or mouse pressed, keycode etc
def input_event_get_info(game_event: InputEventT) -> InputEventInfoT:
    event_info: InputEventInfoT = [None] * INPUT_EVENT_INFO_COUNT

    event_info[INPUT_EVENT_INFO_EV] = game_event[T_INPUT_EVENT_TYPE]
    event_info[INPUT_EVENT_INFO_TYPE] = fltk.type_ev(event_info[INPUT_EVENT_INFO_EV])
    if event_info[INPUT_EVENT_INFO_TYPE] == None:
        return event_info

    ev_type: str = event_info[INPUT_EVENT_INFO_TYPE].lower()
    event_info[INPUT_EVENT_INFO_IS_KEY] = ev_type == "touche"
    event_info[INPUT_EVENT_INFO_KEY_PRESSED] = None
    if event_info[INPUT_EVENT_INFO_IS_KEY]:
        tk_event: TkEvent = event_info[INPUT_EVENT_INFO_EV][fltk_ext.FLTK_EVENT_TK_EVENT]
        event_info[INPUT_EVENT_INFO_KEY_PRESSED] = tk_event.keysym.lower()
    
    return event_info
