import os
import sys
import configparser

def get_config_path(filename):

    try:
        # Check if the program is running as a bundled executable
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            application_path = os.path.join(application_path, 'QC Reports GEN') #put here the name of the executable it will be the same name a folder will be created inside the dist directory
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        full_path = os.path.join(application_path, filename)
        return full_path
    except Exception as e:  # Handle any exception and assign it to variable e
                # Log the error to a file for debugging
                with open('error_log.txt', 'a') as log_file:
                    log_file.write(f"Error: {e}\n")  # Use f-string for Python 3.6+
                print("ERROR", f"ERROR - {e}")

config = configparser.ConfigParser()
config_file = get_config_path('Config\\config.ini') # IF USING reports_gen.spec file which was the first that worked
config.read(config_file, encoding='utf-8')