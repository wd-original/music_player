# contains CRUD operations on JSON files

import json
from typing import Any, IO
import os

def check_filepath_validity(filepath: str, mode: str) -> IO[Any]:
    """checks if filepath is valid (can be opened)

    WARNING:
        returns the file stream opened in mode

    Args:
        filepath (str): file to check
        mode (str): mode to open it in, does not apply any aditional logic, just tries to execute the mode, raising errors

    Returns:
        IO[Any]: the file stream opened in mode
    """
    try:
        return open(filepath, mode)

    except FileNotFoundError:
        print(f"[ERROR] The path '{filepath}' does not exist or is invalid.")
        return None

    except IsADirectoryError:
        print(f"[ERROR] The path '{filepath}' points to a folder, not a file.")
        return None

    except PermissionError:
        print(f"[ERROR] The file exists, but we do not have the permission to read it.")
        return None

    except ValueError as e:
        print(f"[ERROR]: Invalid mode {mode} for opening a file")
        return None

    except OSError as e:
        print(f"[ERROR]: Invalid path syntax or OS error: {e}")
        return None


def read_data(path: str) -> dict:
    """
    reads json from file, returns empty creates nothing

    Args:
        path - path to the file (must be a valid path)

    Returns:
        a dictionary of the read json
    """

    f = check_filepath_validity(path, 'r')

    j: dict

    if not f or file_empty(path):
        j = {}
    else:
        j = json.load(f)

    f.close()

    return j


def write_data(path: str, data):
    """
    OVERWRITES file with data

    Args:
        path - path of file
        data - data that will be written to file
    """

    f = check_filepath_validity(path, 'w')

    if f:
        json.dump(data, f, indent=4)
    else:
        raise RuntimeError(f"Cannot save data to path '{path}'\ncannot create/open file")

    f.close()


# TODO: move these into a separate file_crud file
def clear_file(path: str):
    """file become empty
    """
    with open(path, 'w'):
        pass

def file_empty(path: str):
    if not os.path.exists(path):
        return False
    
    return os.path.getsize(path) == 0

