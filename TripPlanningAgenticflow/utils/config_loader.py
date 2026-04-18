import yaml
import os 

def load_config(config_file_path:str = "config/config.yaml")->dict:
    """opens the yaml file, reads it and converts into dict and returns"""
    with open(config_file_path, "r") as file:
        config = yaml.safe_load(file)
        return config