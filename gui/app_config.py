"""This module provide the function needed to get the application configuration.
"""
import sys
import os

from ruamel.yaml import YAML


def get_tags_list() -> list:
    """Generate a list of tag label

    It will try to import the tag list from the config file 'config/tags.yml'.

    Returns
    -------
        tags_list : list
            A list of string which represent the tags label
    """
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    path += os.path.sep + 'config' + os.path.sep + 'tags.yml'
    try:
        with open(path) as stream:
            data = YAML().load(stream)
            return data['tags']
    except FileNotFoundError:
        return []
    except IOError:
        return []
