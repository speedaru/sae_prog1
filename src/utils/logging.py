"""
Simple logging module using bitwise flags (log levels) to control message output.

The global LOG_LEVEL constant determines which types of messages will be printed.
"""

LOG_LEVEL_RELEASE =     1 << 0
LOG_LEVEL_DEBUG =       1 << 1
LOG_LEVEL_DEBUG_FULL =  1 << 2
LOG_LEVEL_EVENT =       1 << 3
LOG_LEVEL_TRACE =       1 << 4
LOG_LEVEL_ERROR =       1 << 5
LOG_LEVEL_FPS   =       1 << 6
LOG_LEVEL_WARNING =     1 << 7
LOG_LEVEL_RENDERING =   1 << 8

# LOG_LEVEL = LOG_LEVEL_RELEASE | LOG_LEVEL_DEBUG | LOG_LEVEL_DEBUG_FULL | LOG_LEVEL_EVENT
LOG_LEVEL = LOG_LEVEL_RELEASE | LOG_LEVEL_DEBUG | LOG_LEVEL_EVENT | LOG_LEVEL_ERROR | LOG_LEVEL_WARNING
# LOG_LEVEL = LOG_LEVEL_RELEASE | LOG_LEVEL_ERROR

def log(log_level, message: str, new_line: bool = True):
    """
    Prints a message to the console if its severity level is active in LOG_LEVEL.

    Args:
        log_level (int): The severity level of the message (must be one of the LOG_LEVEL_* constants).
        message (str): The string content to print.
        new_line (bool, optional): Whether to end the message with a newline character. Defaults to True.
    """
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

def log_trace(message: str, new_line: bool = True):
    log(LOG_LEVEL_TRACE, message, new_line)

def log_error(message: str, new_line: bool = True):
    log(LOG_LEVEL_ERROR, message, new_line)

def log_fps(message: str, new_line: bool = True):
    log(LOG_LEVEL_FPS, message, new_line)

def log_warning(message: str, new_line: bool = True):
    log(LOG_LEVEL_WARNING, message, new_line)

def log_rendering(message: str, new_line: bool = True):
    log(LOG_LEVEL_RENDERING, message, new_line)
