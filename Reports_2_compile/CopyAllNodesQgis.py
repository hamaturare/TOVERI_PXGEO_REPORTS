from GenerateReports import GenerateReports
# load variables from .conf file
from config_path import config


class CopyAllNodesQgis:
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
            
            df_deployed = self.cumulative[columns_deployed]
            cleaned_deployed_df = df_deployed.dropna()
            cleaned_deployed_df.to_csv(self.reports_path + 'Deployed_All.csv', index=False)

            df_recovered = self.cumulative[columns_recovered]
            cleaned_recovered_df = df_recovered.dropna()
            cleaned_recovered_df.to_csv(self.reports_path + 'Recovered_All.csv', index=False)
            
    except Exception as e:  # Handle any exception and assign it to variable e
                # Log the error to a file for debugging
                with open('error_log.txt', 'a') as log_file:
                    log_file.write(f"Error: {e}\n")  # Use f-string for Python 3.6+
                print("ERROR", f"ERROR - {e}")