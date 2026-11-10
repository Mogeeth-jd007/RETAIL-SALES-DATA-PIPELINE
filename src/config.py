import json
from pathlib import Path


# Locate the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Locate the configuration file
CONFIG_FILE = BASE_DIR / "config.json"


def load_config():

    # Read the main configuration
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)

    return config


def load_dataset_config(dataset_name=None):

    # Load the main configuration
    config = load_config()

    # Get the active dataset if none is specified
    if dataset_name is None:
        dataset_name = config["active_dataset"]

    # Check whether the requested dataset exists
    if dataset_name not in config["datasets"]:
        raise ValueError(
            f"Unknown dataset profile: {dataset_name}"
        )

    # Return the selected dataset configuration
    return config["datasets"][dataset_name]


def get_project_path(relative_path):

    # Convert a relative path into an absolute project path
    return BASE_DIR / relative_path