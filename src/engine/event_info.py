from types import NoneType

import libs.fltk as fltk
from libs.fltk import FltkEvent

from src.game.game_config import *

import src.utils.fltk_extensions as fltk_ext


EventInfoT = list[FltkEvent | str | NoneType | bool]

EVENT_INFO_EV = 0      # FltkEvent
EVENT_INFO_TYPE = 1    # optional str
EVENT_INFO_IS_KEY = 2  # bool
EVENT_INFO_KEY_PRESSED = 3 # str
EVENT_INFO_COUNT = 4


# get info on event, such as if is key or mouse pressed, keycode etc
def event_get_info(game_event: GameEventT) -> EventInfoT:
    event_info: EventInfoT = [None] * EVENT_INFO_COUNT

    event_info[EVENT_INFO_EV] = game_event[GAME_EVENT_TYPE]
    event_info[EVENT_INFO_TYPE] = fltk.type_ev(event_info[EVENT_INFO_EV])
    if event_info[EVENT_INFO_TYPE] == None:
        return event_info

    ev_type: str = event_info[EVENT_INFO_TYPE].lower()
    event_info[EVENT_INFO_IS_KEY] = ev_type == "touche"
    event_info[EVENT_INFO_KEY_PRESSED] = None
    if event_info[EVENT_INFO_IS_KEY]:
        tk_event: TkEvent = event_info[EVENT_INFO_EV][fltk_ext.FLTK_EVENT_TK_EVENT]
        event_info[EVENT_INFO_KEY_PRESSED] = tk_event.keysym.lower()
    
    return event_info
