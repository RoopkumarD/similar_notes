import os
import selectors
import sys


def get_config_dir():
    """
    Get the appropriate directory for storing configuration files based on the user's OS.
    """
    home_dir = os.path.expanduser("~")  # Get user's home directory

    # Check the operating system and construct the config directory path
    if sys.platform.startswith("linux"):
        config_dir = os.path.join(home_dir, ".config", "simnotesconfig")
    elif sys.platform.startswith("darwin"):  # macOS
        config_dir = os.path.join(home_dir, ".simnotesconfig")
    elif sys.platform.startswith("win"):
        # For Windows, use AppData\Roaming for per-user configuration
        appData = os.getenv("APPDATA")
        if appData == None:
            raise Exception("APPDATA env not found")
        config_dir = os.path.join(appData, "Simnotes")
    else:
        # Default to a generic hidden directory in the home directory
        config_dir = os.path.join(home_dir, ".simnotesconfig")

    return config_dir


def is_stdin_available():
    selector = selectors.DefaultSelector()
    key = selector.register(sys.stdin, selectors.EVENT_READ)

    events = selector.select(0.1)  # Set a timeout of 0.1 seconds

    selector.unregister(sys.stdin)

    return bool(events)
