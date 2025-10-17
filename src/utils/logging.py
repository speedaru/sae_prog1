LOG_LEVEL_RELEASE = 0x1
LOG_LEVEL_DEBUG = 0x2
LOG_LEVEL_DEBUG_FULL = 0x4

# LOG_LEVEL = LOG_LEVEL_RELEASE | LOG_LEVEL_DEBUG | LOG_LEVEL_DEBUG_FULL
LOG_LEVEL = LOG_LEVEL_RELEASE | LOG_LEVEL_DEBUG

def log_release(message: str, new_line: bool = True):
    if LOG_LEVEL & LOG_LEVEL_RELEASE:
        terminator = "\n" if new_line else ""
        print(message, end=terminator)

def log_debug(message: str, new_line: bool = True):
    if LOG_LEVEL & LOG_LEVEL_DEBUG:
        terminator = "\n" if new_line else ""
        print(message, end=terminator)

def log_debug_full(message: str, new_line: bool = True):
    if LOG_LEVEL & LOG_LEVEL_DEBUG_FULL:
        terminator = "\n" if new_line else ""
        print(message, end=terminator)
