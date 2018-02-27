import json
import os
from typing import Optional

from seaplane.constants import PROJECT_DIR, SEAPLANE_DIR

config = None
defaults = None


def load_config(file: Optional[str] = None) -> None:
    global config
    global defaults

    if config is not None and defaults is not None:
        return

    if file is None:
        file = PROJECT_DIR + '/seaplane.json'

    if os.path.exists(file):
        with open(file) as f:
            config = json.loads(f.read()) or {}
    else:
        config = {}

    with open(SEAPLANE_DIR + '/configuration/defaults.json') as f:
        defaults = json.loads(f.read())


def get_value(key: str) -> str:
    return config.get(key, defaults[key])
