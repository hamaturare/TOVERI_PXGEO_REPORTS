import os

# Get the absolute path of the current script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the configuration file
relative_config_path = 'Config/config.ini'

# Join the absolute path of the current script file with the relative path to the configuration file
CONFIG_PATH = os.path.join(script_dir, relative_config_path)


