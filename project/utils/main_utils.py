import yaml


def get_yaml_data(key):
    with open('config//config.yaml', 'r') as f:
        yaml_data = yaml.safe_load(f)
    f.close()
    return yaml_data[key]     