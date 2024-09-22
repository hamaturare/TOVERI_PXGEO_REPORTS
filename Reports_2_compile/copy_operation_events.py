import os
import pandas as pd
import glob
import warnings
# load variables from .conf file
from config_path import config

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

rows = 18

def copy_daily_log(log_files_path, destine_file_xlsx):
    pd.set_option('display.max_colwidth', 100)
    # Get a list of all xlsm files in the folder
    log_files = glob.glob(os.path.join(log_files_path, '*.xlsm'))
    log_files = [f for f in log_files if not os.path.basename(f).startswith('~')] # exclude temporary files
    log_files.sort(key=os.path.getctime, reverse=True) # Sorting files by creation time
    df = pd.DataFrame(log_files[0:3], columns=['Logs'])
    print(df)
    print("\n")
    while True:
        try: 
            id = input("Type the number of the log you want to use from list above:  \n")
            print("\n")
            break
        except:
            print("Please type 0 or 1 \n")
            print("\n")

    daily_log = log_files[int(id)] # Set 1 to get the yesterdays log if they keep the current today log file updating there and zero if they don't.
    print('Importing the Daily Log from: ', daily_log)

    # Reading QC Table from Pxgeo
    df = pd.read_excel(daily_log, engine='openpyxl', skiprows=rows, index_col=None, na_values=['NA'], usecols="E:H", header=None)
    df.to_excel(destine_file_xlsx, index=False, header=['Event', 'Start', 'End', 'Remarks'])


destine_file_xlsx = config.get('PATHS','OPERATIONAL_EVENTS_TABLE')
log_files_path = config.get('PATHS','DAILY_LOG_PATH')
copy_daily_log(log_files_path, destine_file_xlsx)
        
    
