import os
import json

# load config file from config.json
def load_config(app: str) -> 'dict[str, str]':
    with open(f'{app}_config.json') as f:
        return json.load(f)

def get_config_value(key: str, app: str) -> str:
    config = load_config(app)
    return config[key] if key in config else ""