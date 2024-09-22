import shutil
import pandas as pd
# load variables from .conf file
from config_path import config

class CopyPiesTable:

    try:
        def __init__ (self):
            self.source_path = config.get('PATHS','PIES_SOURCE_FILE')
            self.destination_path = config.get('PATHS','PIES_DESTINATION_FILE')

            self.df_pies = None

        def copy_table(self):
            #copy table
            shutil.copyfile(self.source_path, self.destination_path)       

        def read_table(self):
            #read table
            try:
                self.df_pies = pd.read_csv(self.destination_path)
            except:
                self.df_pies = pd.read_excel(self.destination_path)
            
        def write_new_pies(self):
            #columns = config.get('COLUMNS','COLLUMNS_TO_USE_ON_PIES_FILE').split(',')
            #df_pies_new = self.df_pies[columns]

            # renaming columns for PBR
            #rename_coulumns = config.get('COLUMNS','COLLUMNS_RENAMED_TO_USE_IN_QGIS').split(',')
            #df_pies_new.columns = rename_coulumns
            #df_pies_new.loc[:,'PIES location'] = df_pies_new.loc[:,'PIES location'].apply(lambda x: x[:-5])

            # writing to new path file
            #df_pies_new.to_csv(self.destination_path, index=False)
            self.df_pies.to_csv(self.destination_path, index=False)

    except Exception as e:  # Handle any exception and assign it to variable e
                # Log the error to a file for debugging
                with open('error_log.txt', 'a') as log_file:
                    log_file.write(f"Error: {e}\n")  # Use f-string for Python 3.6+
                print("ERROR", f"ERROR - {e}")

teste = CopyPiesTable()
teste.write_new_pies()
print(teste)