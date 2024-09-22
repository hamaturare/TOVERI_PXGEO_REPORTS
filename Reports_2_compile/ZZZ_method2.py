import glob
import os
import pandas as pd
import shutil
import datetime

def update_number_method2():
        destination_directory = r'C:\Users\mta1.nv1.qccnslt\Documents\QC\Real_time_Prod'
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        # Check if the cumulative spreadsheet has been updated recently
        navview_path = r'Z:\06_SURVEY\Real-Time_Prod'
        navview_files = glob.glob(os.path.join(navview_path, '*_Fixes__*.txt'))

        # Filter the files based on their creation time
        #navview_files = sorted(navview_files, key=lambda x: os.path.getctime(os.path.join(navview_path, x)), reverse=True ) # sort file by creation time.
        
        filtered_files = [
            file
            for file in navview_files
            if (yesterday <= datetime.date.fromtimestamp(os.path.getctime(os.path.join(navview_path, file))) <= today)        
        ]

        # Copy the filtered files to the destination directory
        for file in filtered_files:
            shutil.copy(os.path.join(navview_path, file), destination_directory)

        # Read all the .txt files in the destination directory into a DataFrame
        dataframes = []

        for file in os.listdir(destination_directory):
            if file.endswith('.txt'):
                df = pd.read_csv(os.path.join(destination_directory, file), sep=',', header=None, parse_dates=[0])
                dataframes.append(df)

        # Concatenate all DataFrames
        all_data = pd.concat(dataframes)

        # Sort by date using the first column
        all_data = all_data.sort_values(by=0)

        # Reset the index
        all_data.reset_index(drop=True, inplace=True)
        
        all_data_today = all_data[all_data[0].dt.date == today]
        # Print the sorted DataFrame
        print(len(all_data_today))
update_number_method2()