import configparser
import json
import os
import sys
import tomllib

import yaml


def load_config(filename: str, paths: list = []) -> dict:
    """Load a config file and return a dict. Config file will be
    parsed with parser based on file extension.

    If filename is an absolute path, attempt to load it and no other.
    If filename is a bare filename, look for filename in dirs listed
    in paths.

    Exception handling is an upstream responsibility.
    """

    loader = None

    ext = filename.split(".")[-1]
    # TODO no suffix error
    match ext.lower():
        case "yml" | "yaml":
            loader = load_yaml_from_file
        case "json":
            loader = load_json_from_file
        case "ini":
            loader = load_ini_from_file
        case "toml" | "tml":
            loader = load_toml_from_file
        case _:
            raise ValueError("unknown file extension")

    if os.path.isabs(filename):
        # If an absolute path, try to load it.
        return loader(filename)
    else:
        # Else, search for the filename.
        for path in paths:
            if path == ".":
                path == os.path.dirname(os.path.realpath(__file__))
            filepath = os.path.join(path, filename)
            if os.path.isfile(filepath):
                return loader(filepath)
        raise FileNotFoundError


def load_yaml_from_file(filepath: str) -> dict:
    """Open the given filepath and yaml load it.
    Return d: dict.
    Exception handling is an upstream responsibility.
    """
    with open(filepath, "rb") as f:
        d = yaml.load(f, Loader=yaml.SafeLoader)

    return d


def load_ini_from_file(filepath: str) -> dict:
    """Read the given ini file.
    Return d: dict.
    Exception handling is an upstream responsibility.
    """
    c = configparser.ConfigParser()
    c.read(filepath)
    d = {}
    for section in c.sections():
        d[section] = {}
        for key, val in c.items(section):
            d[section][key] = val

    return d


def load_toml_from_file(filepath: str) -> dict:
    """Open the given filepath and toml load it.
    Return d: dict.
    Exception handling is an upstream responsibility.
    """
    with open(filepath, "rb") as f:
        d = tomllib.load(f)

    return d


def load_json_from_file(filepath: str) -> dict:
    """Open the given filepath and json load it.
    Return d: dict.
    Exception handling is an upstream responsibility.
    """
    with open(filepath, "rb") as f:
        d = json.load(f)

    return d
