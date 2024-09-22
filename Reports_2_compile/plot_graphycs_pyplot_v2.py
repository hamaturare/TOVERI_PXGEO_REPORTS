import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from CopyCumulativeTable import CopyCumulativeTable 
from GenerateReports import GenerateReports

from config_path import config

#Initiating CopyCumulativeTable class with PATHS and HEADERS to skip rows
cumulative_source = config.get('PATHS','CUMMULATIVE_SOURCE_FILE')
cumulative_destine = config.get('PATHS','CUMMULATIVE_COPIED_FILE')
copier = CopyCumulativeTable(cumulative_source, cumulative_destine)
copier.copy_table()
header_rows = int(config.get('PARAMS','CUMULATIVE_HEADERS'))

# Create the DataFrame
df = pd.read_csv(cumulative_destine, skiprows=header_rows)
columns = ['NodeCode','Preplot Easting','Preplot Northing','Aslaid Easting','Aslaid Northing','Aslaid Azimuth']
#df = df[columns]

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

# Function to plot the lines of the DataFrame
def plot_lines(ax, df):
    for _, row in df.iterrows():
        angle = row['Aslaid Azimuth']
        x_start = row['Distance'] * np.cos(np.radians(angle))
        y_start = row['Distance'] * np.sin(np.radians(angle))
        x_end = x_start * 0.8
        y_end = y_start * 0.8
        if row['Distance'] <= 5:
            color = 'green'
        elif row['Distance'] <= 10:
            color = 'red'
        else:
            color = 'purple'
        ax.plot([x_start, x_end], [y_start, y_end], color=color)

# Calculate the distance between Preplot and Calculated points
df['Distance'] = np.sqrt((df['Aslaid Easting'] - df['Preplot Easting'])**2 + (df['Aslaid Northing'] - df['Preplot Northing'])**2)

# Calculate the percent of nodes that fell between 0 to 4.99m, 5 to 9.99m, 10 to 14.99m and above 15m respectively
total_nodes = len(df)
nodes_0_to_4_99m = len(df[(df['Distance'] >= 0) & (df['Distance'] < 5)])
nodes_5_to_9_99m = len(df[(df['Distance'] >= 5) & (df['Distance'] < 10)])
nodes_10_to_14_99m = len(df[(df['Distance'] >= 10) & (df['Distance'] < 15)])
nodes_above_15m = len(df[df['Distance'] >= 15])
percent_0_to_4_99m = round(nodes_0_to_4_99m / total_nodes * 100,2)
percent_5_to_9_99m = round(nodes_5_to_9_99m / total_nodes *100 ,2)
percent_10_to_14_99m= round(nodes_10_to_14_99m / total_nodes *100 ,2)
percent_above_15m= round(nodes_above_15m / total_nodes *100 ,2)

# Create the graphic
fig, ax = plt.subplots(figsize=(11,8))
#fig.set_facecolor('lightgreen') # Set the background color to light green
ax.set_facecolor('#caf0f8') # Set the background color of the inside of the graphic to light green
ax.set_aspect('equal', adjustable='datalim')

plot_circles(ax)
plot_azimuth(ax)
plot_lines(ax, df)

# Additional settings
ax.set_xlim(-20,20)
ax.set_ylim(-20,20)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title('Aslaid to Preplot Distance with Azimuth')

# Add text with percent of nodes that fell between 0 to 4.99m, 5 to 9.99m, 10 to 14.99m and above 15m respectively
ax.text(1.05, 0.5,
        f'Nodes < 5m: {percent_0_to_4_99m}%',
        transform=ax.transAxes,
        color='green')
ax.text(1.05, 0.45,
        f'Nodes >= 5m < 10m: {percent_5_to_9_99m}%',
        transform=ax.transAxes,
        color='red')
ax.text(1.05, 0.4,
        f'Nodes >=10m < 15m: {percent_10_to_14_99m}%',
        transform=ax.transAxes,
        color='purple')
ax.text(1.05, 0.35,
        f'Nodes >= 15m: {percent_above_15m}%',
        transform=ax.transAxes,
        color='black')

# Adjust subplot parameters
plt.subplots_adjust(left=0.12, bottom=0.12, right=0.7, top=0.9)

# Show graphic
plt.show()
