import json
from os import listdir
from os.path import isfile, join

from webserver.widgets import telemetry_widgets


def save_layout(layouts, configs, directory, filename):
    with open(directory / (filename + '.json'), 'w') as save_file:
        json.dump({'layouts': layouts, 'configs': configs}, save_file)


def get_saves(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    # print(files)
    return [f.replace('.json', '') for f in files]


def load_widgets(directory, filename):
    with open(directory / (filename + '.json'), 'r') as f:
        loaded_layout = json.load(f)
        children_configs = loaded_layout['configs']
        children = [create_child_from_config(cfg) for cfg in children_configs]
        return children


def load_layouts(directory, filename):
    with open(directory / (filename + '.json'), 'r') as f:
        loaded_layout = json.load(f)
        return loaded_layout['layouts']


def create_child_from_config(cfg):
    widget_type = cfg['id']['type']
    return telemetry_widgets[widget_type](saved_data=cfg).widget
