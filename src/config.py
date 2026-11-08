
import json
from pathlib import Path


# Locate the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Locate the configuration file
CONFIG_FILE = BASE_DIR / "config.json"


def load_config():

    # Read configuration from JSON
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)

    return config


def get_project_path(relative_path):

    # Convert a relative path into an absolute project path
    return BASE_DIR / relative_path
