import yaml
import os


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
__DATA_FILE = os.path.join(PROJECT_ROOT, 'data.yaml')


def get(name: str):
    with open(__DATA_FILE, 'r') as f:
        data = yaml.load(f)
        if name in data:
            return data[name]
        else:
            print('Value {} was not found in data file.'.format(name))
            return None


def write(name: str, value):
    if os.path.isfile(__DATA_FILE):
        with open(__DATA_FILE, 'r') as f:
            data = yaml.load(f)
    else:
        data = {}
    data[name] = value
    with open(__DATA_FILE, 'w+') as f:
        yaml.dump(data, f, default_flow_style=False)
