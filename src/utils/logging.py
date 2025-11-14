LOG_LEVEL_RELEASE = 0x1
LOG_LEVEL_DEBUG = 0x2
LOG_LEVEL_DEBUG_FULL = 0x4
LOG_LEVEL_EVENT = 0x8
LOG_LEVEL_EVENT_TRACE = 0x10
LOG_LEVEL_ERROR = 0x20

# LOG_LEVEL = LOG_LEVEL_RELEASE | LOG_LEVEL_DEBUG | LOG_LEVEL_DEBUG_FULL | LOG_LEVEL_EVENT
LOG_LEVEL = LOG_LEVEL_RELEASE | LOG_LEVEL_DEBUG | LOG_LEVEL_EVENT | LOG_LEVEL_ERROR

def log(log_level, message: str, new_line: bool = True):
    if LOG_LEVEL & log_level:
        terminator = "\n" if new_line else ""
        print(message, end=terminator)

def log_release(message: str, new_line: bool = True):
    log(LOG_LEVEL_RELEASE, message, new_line)

def log_debug(message: str, new_line: bool = True):
    log(LOG_LEVEL_DEBUG, message, new_line)

def log_debug_full(message: str, new_line: bool = True):
    log(LOG_LEVEL_DEBUG_FULL, message, new_line)

def log_event(message: str, new_line: bool = True):
    log(LOG_LEVEL_EVENT, message, new_line)

def log_event_trace(message: str, new_line: bool = True):
    log(LOG_LEVEL_EVENT_TRACE, message, new_line)

def log_error(message: str, new_line: bool = True):
    log(LOG_LEVEL_ERROR, message, new_line)
