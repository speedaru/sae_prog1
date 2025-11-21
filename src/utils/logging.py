"""
Simple logging module using bitwise flags (log levels) to control message output.

The global LOG_LEVEL constant determines which types of messages will be printed.
"""

LOG_LEVEL_RELEASE = 0x1
LOG_LEVEL_DEBUG = 0x2
LOG_LEVEL_DEBUG_FULL = 0x4
LOG_LEVEL_EVENT = 0x8
LOG_LEVEL_TRACE = 0x10
LOG_LEVEL_ERROR = 0x20

# LOG_LEVEL = LOG_LEVEL_RELEASE | LOG_LEVEL_DEBUG | LOG_LEVEL_DEBUG_FULL | LOG_LEVEL_EVENT
# LOG_LEVEL = LOG_LEVEL_RELEASE | LOG_LEVEL_DEBUG | LOG_LEVEL_EVENT | LOG_LEVEL_ERROR
LOG_LEVEL = LOG_LEVEL_RELEASE

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
