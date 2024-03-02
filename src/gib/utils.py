import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")


def get_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        print("Config file not found.")


def set_config(model):
    config = {"model_name": model}
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)
    print("Config set.")
