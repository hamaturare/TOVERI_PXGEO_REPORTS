import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from CopyCumulativeTable import CopyCumulativeTable 

from config_path import config

#Initiating CopyCumulativeTable class with PATHS and HEADERS to skip rows
cumulative_source = config.get('PATHS','CUMMULATIVE_SOURCE_FILE')
cumulative_destine = config.get('PATHS','CUMMULATIVE_COPIED_FILE')
copier = CopyCumulativeTable(cumulative_source, cumulative_destine)
copier.copy_table()
header_rows = int(config.get('PARAMS','CUMULATIVE_HEADERS'))

# Create the DataFrame
df = pd.read_csv(cumulative_destine, skiprows=header_rows,encoding='latin1')
columns = ['Line','Point','Index','Aslaid Easting','Aslaid Northing']

df = df[df['Index'] == 2]
df = df[columns]

df.to_csv(r'C:\Users\mta1.nv1.qccnslt\Documents\003023-Sepia\QC\Index_2_colocated_nodes.csv' , index=False)

