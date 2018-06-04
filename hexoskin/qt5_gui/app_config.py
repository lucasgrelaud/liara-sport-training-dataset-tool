import sys
import os

from ruamel.yaml import YAML
from ruamel.yaml import YAMLError
def get_tags_list():
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    path += os.path.sep + 'config' + os.path.sep + 'tags.yml'
    with open(path) as stream:
        try:
            data = YAML().load(stream)
            return data['tags']
        except YAMLError as error:
            print(error)