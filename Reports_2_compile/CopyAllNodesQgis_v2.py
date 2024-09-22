from GenerateReports import GenerateReports
import pandas as pd
# load variables from .conf file
from config_path import config


class CopyAllNodesQgisv2:
    try:
        def __init__ (self):
            self.header_rows = int(config.get('PARAMS','CUMULATIVE_HEADERS'))
            self.cumulative_path = config.get('PATHS','CUMMULATIVE_SOURCE_FILE')
            self.reports_path = config.get('PATHS', 'QGIS_DEPLOY_RECOVERY_PATH')
            self.tablegen = GenerateReports(self.cumulative_path, self.header_rows)
            self.cumulative = self.tablegen.read_table()

        def create_tables(self):
            columns_deployed = config.get('COLUMNS','DEPLOYED_ALL_COLUMNS_4_QGIS_NODES').split(',')
            columns_recovered = config.get('COLUMNS','RECOVERY_ALL_COLUMNS_4_QGIS_NODES').split(',')
            
            df_dep = self.cumulative[columns_deployed]
            df_rec = self.cumulative[columns_recovered]

            for values in df_dep['Aslaid Easting']:
                if not pd.isnull(values):   
                    df_deployed = self.cumulative[columns_deployed]
                    df_deployed.to_csv(self.reports_path + 'Deployed_All.csv', index=False)

            for values in df_rec['Recovered Easting']:
                if not pd.isnull(values):
                    df_recovered = self.cumulative[columns_recovered]
                    df_recovered.to_csv(self.reports_path + 'Recovered_All.csv', index=False)
                    
    except Exception as e:  # Handle any exception and assign it to variable e
            # Log the error to a file for debugging
            with open('error_log.txt', 'a') as log_file:
                log_file.write(f"Error: {e}\n")  # Use f-string for Python 3.6+
            print("ERROR", f"ERROR - {e}")

start = CopyAllNodesQgisv2()
start.create_tables()