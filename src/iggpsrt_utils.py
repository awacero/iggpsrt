

import os

def check_file_exists(file_path):
    """Return ``True`` if the given file path exists."""
    return os.path.isfile(file_path)


import yaml

def load_yaml_config(file_path):
    """Load a YAML configuration file and return it as a dictionary.

    Parameters
    ----------
    file_path : str
        Path to the YAML configuration file.

    Returns
    -------
    dict or None
        Parsed configuration or ``None`` if the file could not be read.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)  # Load YAML safely
            return config
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse YAML file '{file_path}': {e}")
        return None

import json
import os

def load_json_config(file_path, encoding="utf-8"):
    """Load a JSON file and return the parsed dictionary.

    Parameters
    ----------
    file_path : str
        Path to the JSON file.
    encoding : str, optional
        Encoding format used to read the file.

    Returns
    -------
    dict or None
        Parsed JSON data or ``None`` if an error occurs.
    """
    try:
        # Open and load JSON
        with open(file_path, "r", encoding=encoding) as file:
            config = json.load(file)  # Parse JSON
            return config

    except json.JSONDecodeError as e:
        print(f"JSON Parsing Error in '{file_path}': {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    
    return None  # Return None if an error occurs

