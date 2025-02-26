

import os

def check_file_exists(file_path):
    """
    Check if a file exists.

    :param file_path: Path to the file.
    :return: True if the file exists, False otherwise.
    """
    return os.path.isfile(file_path)


import yaml

def load_yaml_config(file_path):
    """
    Reads a YAML file and returns the configuration as a dictionary.

    :param file_path: Path to the YAML configuration file.
    :return: Dictionary with the configuration.
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
    """
    Reads a JSON file and returns the configuration as a dictionary.

    :param file_path: Path to the JSON file.
    :param encoding: Encoding format (default: 'utf-8').
    :return: Dictionary with the JSON content or None if an error occurs.
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

