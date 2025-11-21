"""
Global Configuration Module.

This module defines constants related to file paths and directories within the project
structure. It relies on Python's built-in `os` and `pathlib` modules to construct
system-independent paths.
"""

import os
from pathlib import Path

DUNGEON_FILES_DIR = os.path.join(Path(__file__).parent, "..", "dungeons")
