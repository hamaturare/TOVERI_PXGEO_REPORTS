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

###############
################

# Create the DataFrame From Cumulative Table for Deployment Only
df_d = pd.read_csv(cumulative_destine, skiprows=header_rows,encoding='latin1')
columns_d = ['Line','Point','Index','Preplot Easting','Preplot Northing','Aslaid Easting','Aslaid Northing','Deployed by ROV']

df_d = df_d[df_d['Index'] == 1]
df_d = df_d[columns_d]

# Calculate deltas for Aslaid to Preplot (Deployment)
df_d['delta_D_x'] = df_d['Aslaid Easting'] - df_d['Preplot Easting']
df_d['delta_D_y'] = df_d['Aslaid Northing'] - df_d['Preplot Northing']
# Calculate the distance from 0, 0 using the deltas
df_d['Distance_D'] = np.sqrt(df_d['delta_D_x']**2 + df_d['delta_D_y']**2)

#################
##################

# Create the DataFrame From Cumulative Table For Recovered Only
df_r = pd.read_csv(cumulative_destine, skiprows=header_rows,encoding='latin1')
columns_r = ['Line','Point','Index','Preplot Easting','Preplot Northing','Recovered Easting','Recovered Northing','Recovered by ROV']

#df = df[columns]
df_r = df_r[df_r['Index'] == 1]
df_r = df_r[columns_r]

# Calculate deltas for recovered to Preplot
df_r['delta_R_x'] = df_r['Recovered Easting'] - df_r['Preplot Easting']
df_r['delta_R_y'] = df_r['Recovered Northing'] - df_r['Preplot Northing']
# Calculate the distance from 0, 0 using the deltas
df_r['Distance_R'] = np.sqrt(df_r['delta_R_x']**2 + df_r['delta_R_y']**2)

####################
#####################


#Grabing Node Stats with Seismic to Preplot Coordinates
node_stats_destine = r'Z:\03_QC\21-Nodes_Stats_and_followup\0256_3D_SEPIA_Nodes_Stats.csv'

# Create the DataFrame
df_s = pd.read_csv(node_stats_destine)
columns_s = ['RL','Station','index','X_preplot','Y_preplot','X_seismic','Y_seismic']

#df = df[columns]
df_s = df_s[df_s['index'] == 1]
df_s = df_s[columns_s]
df_s.rename(columns={'RL':'Line','Station':'Point'}, inplace=True)

# Calculate deltas for Seismic To Preplot
df_s['delta_S_x'] = df_s['X_seismic'] - df_s['X_preplot']
df_s['delta_S_y'] = df_s['Y_seismic'] - df_s['Y_preplot']
# Calculate the distance from 0, 0 using the deltas
df_s['Distance_S'] = np.sqrt(df_s['delta_S_x']**2 + df_s['delta_S_y']**2)



###############
################

df_s = pd.merge(df_s, df_r[['Line','Point','Recovered Easting','Recovered Northing','Recovered by ROV','Distance_R']], on=['Line', 'Point'], how='left')
df_s = pd.merge(df_s, df_d[['Line','Point','Aslaid Easting','Aslaid Northing','Deployed by ROV','Distance_D']], on=['Line', 'Point'], how='left')
df_merged_final_clean = df_s.dropna()
columns_final = ['Line','Point','index','X_preplot','Y_preplot','X_seismic','Y_seismic','Aslaid Easting','Aslaid Northing','Recovered Easting','Recovered Northing','Deployed by ROV','Recovered by ROV','Distance_S','Distance_D','Distance_R']
df_merged_final_clean = df_merged_final_clean[columns_final]
df_merged_final_clean=df_merged_final_clean.rename(columns={'X_preplot':'Preplot_X','Y_preplot':'Preplot_Y','X_seismic':'Seismic_X','Y_seismic':'Seismic_Y','Aslaid Easting':'Aslaid_X','Aslaid Northing':'Aslaid_Y','Recovered Easting':'Recovered_X','Recovered Northing':'Recovered_Y','Distance_S':'Distance_Seismic','Distance_D':'Distance_Deployed','Distance_R':'Distance_Recovered'})
#print(df_merged_final_clean)
#Export CSVs
df_merged_final_clean.to_csv(r'C:\Users\mta1.nv1.qccnslt\Documents\003023-Sepia\QC\Nodes_above_5m_by_ROVs.csv' , index=False)

#Short Table
columns_short=['Line','Point','index','Seismic_X','Seismic_Y','Deployed by ROV','Distance_Seismic']
df_merged_final_clean_short=df_merged_final_clean[columns_short]

df_merged_final_clean_short.to_csv(r'C:\Users\mta1.nv1.qccnslt\Documents\003023-Sepia\QC\Nodes_above_5m_by_ROVs_short.csv' , index=False)