import yaml

def load_config(path):
    """
    Load configuration data.
    """
    open(path, 'r')
    try:
        with open(path, 'r') as f:
            config_dict = yaml.safe_load(f)
        return config_dict
    except:
        return None