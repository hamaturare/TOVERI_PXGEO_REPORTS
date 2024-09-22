import os
import sys
import configparser

def get_config_path(filename):
    # Check if the program is running as a bundled executable
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        application_path = os.path.join(application_path, 'QC Reports GEN - Pre-Release') #put here the name of the executable it will be the same name a folder will be created inside the dist directory
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
   
    return os.path.join(application_path, filename)

config = configparser.ConfigParser()
config_file = get_config_path('Config\\config.ini')
#config.read(get_config_path('Config/config.ini'))

config.read(config_file, encoding='utf-8')