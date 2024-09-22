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
columns = ['NodeCode','Index','Preplot Easting','Preplot Northing','Aslaid Easting','Aslaid Northing','Aslaid Azimuth']

#df = df[df['Index'] == 1]

# Calculate deltas
df['delta_x'] = df['Aslaid Easting'] - df['Preplot Easting']
df['delta_y'] = df['Aslaid Northing'] - df['Preplot Northing']
# Calculate the distance from 0, 0 using the deltas
df['Distance'] = np.sqrt(df['delta_x']**2 + df['delta_y']**2)

# Function to plot the circles of radius
def plot_circles(ax):
    radii = [5, 10, 15]
    colors = ['green', 'red', 'purple']
    for r, color in zip(radii, colors):
        circle = plt.Circle((0, 0), r, color=color, fill=False)
        ax.add_patch(circle)
        ax.text(r, 0, f'{r}m', ha='center', va='bottom')
        
# Function to plot the azimuth line
def plot_azimuth(ax):
    azimuth = 210
    x = [0, 15 * np.cos(np.radians(azimuth))]
    y = [0, 15 * np.sin(np.radians(azimuth))]
    ax.plot(x, y, color='gray')
    ax.text(x[1], y[1], '210°', ha='center', va='bottom')

# Modified function to plot dots
def plot_dots(ax, df):
    # Define your color thresholds
    thresholds = [5, 10, 15, 20]
    colors = ['green', 'orange', 'red', 'purple']
    for _, row in df.iterrows():
        distance = row['Distance']
        # Determine color based on distance
        if distance <= thresholds[0]:
            color = colors[0]
        elif distance <= thresholds[1]:
            color = colors[1]
        elif distance <= thresholds[2]:
            color = colors[2]
        else:
            color = colors[3]
        ax.scatter(row['delta_x'], row['delta_y'], color=color, s=10)  # Plotting dot

# Calculate the distance between Preplot and Calculated points
df['Distance'] = np.sqrt((df['Aslaid Easting'] - df['Preplot Easting'])**2 + (df['Aslaid Northing'] - df['Preplot Northing'])**2)

# Calculate the percent of nodes that fell between 0 to 4.99m, 5 to 9.99m, 10 to 14.99m and above 15m respectively
mask = pd.notna(df['Aslaid Easting']) & df['Aslaid Easting'] 
total_nodes = len(df[mask])

nodes_0_to_4_99m = len(df[(df['Distance'] >= 0) & (df['Distance'] < 5)])
nodes_5_to_9_99m = len(df[(df['Distance'] >= 5) & (df['Distance'] < 10)])
nodes_10_to_14_99m = len(df[(df['Distance'] >= 10) & (df['Distance'] < 15)])
nodes_above_15m = len(df[df['Distance'] >= 15])
percent_0_to_4_99m = round(nodes_0_to_4_99m / total_nodes * 100,2)
percent_5_to_9_99m = round(nodes_5_to_9_99m / total_nodes *100 ,2)
percent_10_to_14_99m= round(nodes_10_to_14_99m / total_nodes *100 ,2)
percent_above_15m= round(nodes_above_15m / total_nodes *100 ,2)

# Create the graphic
fig, ax = plt.subplots(figsize=(11, 8))
ax.set_facecolor('#caf0f8')
ax.set_aspect('equal', 'box')


plot_circles(ax)
#plot_azimuth(ax)  # This can be commented out or removed
plot_dots(ax, df)

# Additional settings
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
ax.set_xticks(np.arange(-20, 21, 5))
ax.set_yticks(np.arange(-20, 21, 5))
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.set_title('Aslaid to Preplot Distance Distribution')


# Add text with percent of nodes in each distance category
ax.text(1.05, 0.5, f'{nodes_0_to_4_99m} Nodes < 5m: {percent_0_to_4_99m}%', transform=ax.transAxes, color='green')
ax.text(1.05, 0.45, f'{nodes_5_to_9_99m} Nodes >= 5m < 10m: {percent_5_to_9_99m}%', transform=ax.transAxes, color='orange')
ax.text(1.05, 0.4, f'{nodes_10_to_14_99m} Nodes >=10m < 15m: {percent_10_to_14_99m}%', transform=ax.transAxes, color='red')
ax.text(1.05, 0.35, f'{nodes_above_15m} Nodes >= 15m: {percent_above_15m}%', transform=ax.transAxes, color='purple')

#Adjust subplot parameters

plt.subplots_adjust(left=0.12, bottom=0.12, right=0.7, top=0.9)

#Show graphic

plt.show()