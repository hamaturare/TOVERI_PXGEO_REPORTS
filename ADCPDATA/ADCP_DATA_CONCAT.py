#This will concatenate all ADCP .dat file into one cumulative spread sheet called ADCP_Cumulative_PY.csv 
#The table will be located unde the ADCP folder C:\\Users\\mta1.nv1.qccnslt\\Documents\\001021-Itapu\\Odyssey\\ADCP data\\ADCP_Cumulative_PY.csv
#In order for this python script to work you will need to place all ADCP files into the folder: C:\\Users\\mta1.nv1.qccnslt\\Documents\\001021-Itapu\\Odyssey\\ADCP data\\ADCP_4_QUERY
#This folder must contain only the ACDP files you will use and nothing more
#The Cumulative spread sheet will have only every 24th measurement from each individual ADCP.dat file

import pandas as pd
import glob
import configparser
from config_path import CONFIG_PATH

# load variables from .conf file
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

adcp_data_frame = pd.DataFrame()
adcp_data = []

path = config.get("PATH", 'ADCP_FOLDER')
files = glob.glob(path + "/*.dat")

print("Creating ADCP Data CSV Table")
print("ADCP_Cumulative_PY.csv")
print("Please Hold.....") 

# Opening all the files inside the folder "path"

for csv_files in files:
    
    df = pd.read_csv(csv_files)
    adcp_data.append(df)
    adcp_data_frame = pd.concat(adcp_data)

adcp_data_frame.rename(columns = {'%     Date' : 'Date'}, inplace=True )
adcp_data_frame.sort_values(by = 'Date', ascending=True, ignore_index=True)
df2 = adcp_data_frame[adcp_data_frame.index % 24 == 0]    
ADCP_CONCAT_FILE = config.get('PATH', 'ADCP_CONCAT_FILE')
df2.to_csv(ADCP_CONCAT_FILE, index=False) 
print(df2)