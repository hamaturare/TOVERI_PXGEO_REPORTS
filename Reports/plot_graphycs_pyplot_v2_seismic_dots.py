import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Assuming CopyCumulativeTable and config_path setup remains as in your original code

#Initiating CopyCumulativeTable class with PATHS and HEADERS to skip rows

node_stats_destine = r'Z:\03_QC\21-Nodes_Stats_and_followup\0256_3D_SEPIA_Nodes_Stats.csv'
#node_stats_destine = r'C:\Users\mta1.nv1.qccnslt\Documents\003023-Sepia\QC\0256_3D_SEPIA_Nodes_Stats.csv'

# Create the DataFrame
df = pd.read_csv(node_stats_destine)
columns = ['RL','index','Station','X_preplot','Y_preplot','X_seismic','Y_seismic','Azimuth-seismic']
#df = df[columns]

# Calculate deltas
df['delta_x'] = df['X_seismic'] - df['X_preplot']
df['delta_y'] = df['Y_seismic'] - df['Y_preplot']
# Calculate the distance from 0, 0 using the deltas
df['Distance'] = np.sqrt(df['delta_x']**2 + df['delta_y']**2)
df = df[df['index'] == 1]


# Function to plot the circles of radius
def plot_circles(ax):
    radii = [5, 10, 15, 20, 25]
    colors = ['green', 'red', 'purple', 'black', 'red']
    for r, color in zip(radii, colors):
        circle = plt.Circle((0, 0), r, color=color, fill=False)
        ax.add_patch(circle)
        ax.text(r, 0, f'{r}m', ha='center', va='bottom')

# This function becomes redundant as we're not plotting azimuth lines anymore
# def plot_azimuth(ax):
#     pass

# Modified function to plot dots
def plot_dots(ax, df):
    # Define your color thresholds
    thresholds = [5, 10, 15, 20, 25]
    colors = ['green', 'orange', 'red', 'purple', 'black']
    for _, row in df.iterrows():
        distance = row['Distance']
        # Determine color based on distance
        if distance < thresholds[0]:
            color = colors[0]
        elif distance < thresholds[1]:
            color = colors[1]
        elif distance < thresholds[2]:
            color = colors[2]
        elif distance < thresholds[3]:
            color = colors[3]    
        else:
            color = colors[4]
        ax.scatter(row['delta_x'], row['delta_y'], color=color, s=10)  # Plotting dot

# Calculate the distance between Preplot and Calculated points
df['Distance'] = np.sqrt((df['X_seismic'] - df['X_preplot'])**2 + (df['Y_seismic'] - df['Y_preplot'])**2)

# Calculate the percent of nodes that fell between the specified distances
total_nodes = len(df)
nodes_0_to_4_99m = len(df[(df['Distance'] < 5)])
nodes_5_to_9_99m = len(df[(df['Distance'] >= 5) & (df['Distance'] < 10)])
nodes_10_to_14_99m = len(df[(df['Distance'] >= 10) & (df['Distance'] < 15)])
nodes_above_15m = len(df[df['Distance'] >= 15])
nodes_above_20m = len(df[df['Distance'] >= 20])
percent_0_to_4_99m = round(nodes_0_to_4_99m / total_nodes * 100,1)
percent_5_to_9_99m = round(nodes_5_to_9_99m / total_nodes *100 ,1)
percent_10_to_14_99m = round(nodes_10_to_14_99m / total_nodes *100 ,1)
percent_above_15m = round(nodes_above_15m / total_nodes *100 ,1)
percent_above_20m = round(nodes_above_20m / total_nodes *100 ,1)

# Create the graphic
fig, ax = plt.subplots(figsize=(11, 8))
ax.set_facecolor('#caf0f8')
ax.set_aspect('equal', 'box')


plot_circles(ax)
#plot_azimuth(ax)  # This can be commented out or removed
plot_dots(ax, df)

# Additional settings
ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)
ax.set_xticks(np.arange(-30, 31, 5))
ax.set_yticks(np.arange(-30, 31, 5))
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.set_title('Seismic to Preplot Distance Distribution')


# Add text with percent of nodes in each distance category
ax.text(1.05, 0.5, f'{nodes_0_to_4_99m} Nodes < 5m: {percent_0_to_4_99m}%', transform=ax.transAxes, color='green')
ax.text(1.05, 0.45, f'{nodes_5_to_9_99m} Nodes >= 5m < 10m: {percent_5_to_9_99m}%', transform=ax.transAxes, color='orange')
ax.text(1.05, 0.4, f'{nodes_10_to_14_99m} Nodes >=10m < 15m: {percent_10_to_14_99m}%', transform=ax.transAxes, color='red')
ax.text(1.05, 0.35, f'{nodes_above_15m} Nodes >= 15m: {percent_above_15m}%', transform=ax.transAxes, color='purple')
ax.text(1.05, 0.30, f'{nodes_above_20m} Nodes >= 20m', transform=ax.transAxes, color='black') #{percent_above_20m}%

#Adjust subplot parameters

plt.subplots_adjust(left=0.12, bottom=0.12, right=0.7, top=0.9)

#Show graphic

plt.show()
