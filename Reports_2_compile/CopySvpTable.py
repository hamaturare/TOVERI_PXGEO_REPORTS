import shutil
import pandas as pd
# load variables from .conf file
from config_path import config

class CopySvpTable:

    try:
        def __init__ (self):
            self.source_path = config.get('PATHS','SVP_SOURCE_FILE')
            self.destination_path = config.get('PATHS','SVP_DESTINATION_FILE')
            self.headers = int(config.get('PARAMS','SVP_HEADERS'))
            self.df_svp = None
            
        def copy_table(self):
            #copy table
            shutil.copyfile(self.source_path, self.destination_path)        

        def read_table(self):
            #read table
            self.df_svp = pd.read_excel(self.destination_path, skiprows=self.headers)   

        def write_new_svp(self):
            # Drop rows with NULL values
            cleaned_df = self.df_svp.dropna()
            # Write the cleaned DataFrame to a CSV file
            cleaned_df.to_csv(self.destination_path, index=False)
            
    except Exception as e:  # Handle any exception and assign it to variable e
                # Log the error to a file for debugging
                with open('error_log.txt', 'a') as log_file:
                    log_file.write(f"Error: {e}\n")  # Use f-string for Python 3.6+
                print("ERROR", f"ERROR - {e}")

#CopySvpTable()