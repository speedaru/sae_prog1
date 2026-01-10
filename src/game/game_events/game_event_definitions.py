# general game event definitions
from src.engine.structs.temporary_game_event import *

from src.game.game_events.chaos_seal import *


# dict of all temporary game events, with their registration callback
TEMPORARY_GAME_EVENTS: dict[TempEventE, Any] = {
    E_TEMP_EVENT_CHAOS_SEAL: chaos_seal_event_register,
}
