import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D 
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
#columns_final = ['Line','Point','index','X_preplot','Y_preplot','X_seismic','Y_seismic','Aslaid Easting','Aslaid Northing','Recovered Easting','Recovered Northing','Deployed by ROV','Recovered by ROV','Distance_S','Distance_D','Distance_R']
#df_merged_final_clean = df_merged_final_clean[columns_final]
#df_merged_final_clean=df_merged_final_clean.rename(columns={'X_preplot':'Preplot_X','Y_preplot':'Preplot_Y','X_seismic':'Seismic_X','Y_seismic':'Seismic_Y','Aslaid Easting':'Aslaid_X','Aslaid Northing':'Aslaid_Y','Recovered Easting':'Recovered_X','Recovered Northing':'Recovered_Y','Distance_S':'Distance_Seismic','Distance_D':'Distance_Deployed','Distance_R':'Distance_Recovered'})
#print(df_merged_final_clean)
#Export CSVs

# Function to plot the circles of radius
def plot_circles(ax):
    radii = [5, 10, 15, 20, 25]
    colors = ['green', 'red', 'purple', 'black', 'red']
    for r, color in zip(radii, colors):
        circle = plt.Circle((0, 0), r, color=color, fill=False)
        ax.add_patch(circle)
        ax.text(r, 0, f'{r}m', ha='center', va='bottom')

# Modified function to plot dots
def plot_dots(ax, df):
    # Define your color thresholds
    thresholds = [5, 10, 15, 20, 25]
    colors = ['green', 'orange', 'red', 'purple', 'black']
    rov_markers = {
        'UHD64':'.',
        'XLX19':'*'
    }
    for _, row in df_merged_final_clean.iterrows():
        distance = row['Distance_S']
        rov_name = row['Deployed by ROV']
        # Determine color based on distance
        if distance <= thresholds[0]:
            color = colors[0]
        elif distance <= thresholds[1]:
            color = colors[1]
        elif distance <= thresholds[2]:
            color = colors[2]
        elif distance <= thresholds[3]:
            color = colors[3]    
        else:
            color = colors[4]
        marker = rov_markers.get(rov_name, '.')
        ax.scatter(row['delta_S_x'], row['delta_S_y'], color=color, marker=marker)  # Plotting dot

# Calculate the distance between Preplot and Calculated points
df_s['Distance'] = np.sqrt((df_s['X_seismic'] - df_s['X_preplot'])**2 + (df_s['Y_seismic'] - df_s['Y_preplot'])**2)

# Calculate the percent of nodes that fell between the specified distances
total_nodes = len(df_s)
nodes_0_to_4_99m = len(df_s[(df_s['Distance'] >= 0) & (df_s['Distance'] < 5)])
nodes_5_to_9_99m = len(df_s[(df_s['Distance'] >= 5) & (df_s['Distance'] < 10)])
nodes_10_to_14_99m = len(df_s[(df_s['Distance'] >= 10) & (df_s['Distance'] < 15)])
nodes_above_15m = len(df_s[df_s['Distance'] >= 15])
nodes_above_20m = len(df_s[df_s['Distance'] >= 20])
percent_0_to_4_99m = round(nodes_0_to_4_99m / total_nodes * 100,2)
percent_5_to_9_99m = round(nodes_5_to_9_99m / total_nodes *100 ,2)
percent_10_to_14_99m = round(nodes_10_to_14_99m / total_nodes *100 ,2)
percent_above_15m = round(nodes_above_15m / total_nodes *100 ,2)
percent_above_20m = round(nodes_above_20m / total_nodes *100 ,2)

# Create the graphic
fig, ax = plt.subplots(figsize=(11, 8))
ax.set_facecolor('#caf0f8')
ax.set_aspect('equal', 'box')


plot_circles(ax)
#plot_azimuth(ax)  # This can be commented out or removed
plot_dots(ax, df_s)

# Additional settings
ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)
ax.set_xticks(np.arange(-30, 31, 5))
ax.set_yticks(np.arange(-30, 31, 5))
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.set_title('Seismic to Preplot Distance Distribution')

legend_elements = [ Line2D([0], [0], color='none', marker='*', linestyle='None', markersize=10, markerfacecolor='none', markeredgecolor='black', label='XLX19'), 
                   Line2D([0], [0], color='none', marker='.', linestyle='None', markersize=10, markerfacecolor='none', markeredgecolor='black', label='UHD64'),]

# Add text with percent of nodes in each distance category
ax.text(1.05, 0.5, f'{nodes_0_to_4_99m} Nodes < 5m: {percent_0_to_4_99m}%', transform=ax.transAxes, color='green')
ax.text(1.05, 0.45, f'{nodes_5_to_9_99m} Nodes >= 5m < 10m: {percent_5_to_9_99m}%', transform=ax.transAxes, color='orange')
ax.text(1.05, 0.4, f'{nodes_10_to_14_99m} Nodes >=10m < 15m: {percent_10_to_14_99m}%', transform=ax.transAxes, color='red')
ax.text(1.05, 0.35, f'{nodes_above_15m} Nodes >= 15m: {percent_above_15m}%', transform=ax.transAxes, color='purple')
ax.text(1.05, 0.30, f'{nodes_above_20m} Nodes >= 20m', transform=ax.transAxes, color='black') #{percent_above_20m}%
ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 0.25)) 
 
# Place the legend below the last line of your statistics 




#Adjust subplot parameters

plt.subplots_adjust(left=0.12, bottom=0.12, right=0.7, top=0.9)

#Show graphic

plt.show()
