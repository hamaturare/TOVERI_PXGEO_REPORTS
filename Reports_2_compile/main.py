import tkinter as tk
import ButtonsFunction
import glob
import os
import pandas as pd
import shutil
import datetime as dtime
from PIL import Image, ImageTk
from CopyCumulativeTable import CopyCumulativeTable
from GenerateReports import GenerateReports
from datetime import datetime
# Load images Favicon and Logo
from resources_path import favicon_path, logo_path
# load variables from .conf file
from config_path import config 

#Initiating CopyCumulativeTable class with PATHS and HEADERS to skip rows
cumulative_source = config.get('PATHS','CUMMULATIVE_SOURCE_FILE')
cumulative_destine = config.get('PATHS','CUMMULATIVE_COPIED_FILE')
copier_method1 = CopyCumulativeTable(cumulative_source, cumulative_destine)
copier_method1.copy_table()
header_rows = int(config.get('PARAMS','CUMULATIVE_HEADERS'))

#Initializing GenerateReports Instance
reportgen_method1 = GenerateReports(cumulative_destine, header_rows)
LABEL_NODE_LIVE = '\n Node Count Live: \n'
VERSION = " Pre-Release"
LOGO = logo_path
FAVICON = favicon_path

class Main:

    try:
        def __init__(self):
            # Images for logo and favicon
            favicon_file = FAVICON
            logo_file = LOGO

            """ tk windows parameters """
            # create the main window
            root = tk.Tk()
            root.geometry("1180x850")
            root.config(bg="white")
            
            root.iconbitmap(favicon_file) # Insert Favicon on the window frame
            root.resizable(False, False) # Make window not be resizable
            
            # Set the title with date and clock
            self.update_title(root)
            self.root = root

            """ Initializing a frame to hold buttons """
            button_frame = tk.Frame(root, bd=5, bg="lightblue", relief="groove")
            button_frame.grid(padx=10, pady=10)
            root.grid_columnconfigure(0, weight=1)

            # create a frame for the logo
            logo_frame = tk.Frame(button_frame)
            # pack the logo frame into the main window
            logo_frame.grid(row=8, column=2, rowspan=2)  # specify row and column for logo frame
            # load the logo image using PIL
            image = Image.open(logo_file)
            new_size = (image.width * 2, image.height * 2)
            logo_image = image.resize(new_size)
            logo_photo = ImageTk.PhotoImage(logo_image) # load the logo image of Toveri
            # create a label for the logo and display it on the frame
            logo_label = tk.Label(logo_frame, image=logo_photo, bg='lightblue')
            logo_label.grid(row=9, column=2)  # specify row and column for logo


            """ Starting Tk's buttons parametrization """
            # Add Node Count - one Label version
            self.deployed_label = tk.Label(button_frame, bd=3, relief="solid", text=f'{LABEL_NODE_LIVE}' + str(self.initiate_count('Aslaid Time')) + '\n', font=("Helvetica", 24, "bold"), fg="black", bg="lightgreen", height=3)
            self.deployed_label.grid(row=0, column=2, padx=10, pady=10, sticky="we")


            """ Deployed Node Count Button Update """
            fancy_button = ButtonsFunction.DeployedNodesButton(button_frame)
            fancy_button.button.grid(row=0, column=0, pady=10, padx=10, sticky="we")

            """ Recovered Node Count Button Update """
            fancy_button = ButtonsFunction.RecoveredNodesButton(button_frame)
            fancy_button.button.grid(row=0, column=1, pady=10, padx=10, sticky="we")

            """ Todays Button """
            todays_button = ButtonsFunction.TodaysButton(button_frame)
            todays_button.button.grid(row=1, column=0, pady=20, padx=10)
            
            """ Yesterdays Button """
            yesterdays_button = ButtonsFunction.YesterdaysButton(button_frame)
            yesterdays_button.button.grid(row=1, column=1, pady=20, padx=10)
            
            """ Toveri Reports Button """
            toverireport_button = ButtonsFunction.ToveriReportsButton(button_frame)
            toverireport_button.button.grid(row=3, column=0, padx=5)

            # Create a label with Enter Date (YYY-MM-DD): instructions and pack it
            self.label = tk.Label(button_frame, text="Enter Date (YYY-MM-DD): ", font=("Helvetica", 12, "bold"), fg="black", bg="lightblue")
            self.label.grid(row=4, column=0, padx=5)

            """ PBR Reports Button """
            pbr_report_button = ButtonsFunction.PbrReportsButton(button_frame)
            pbr_report_button.button.grid(row=3, column=1, padx=5)

            # Create a label with Enter Date (YYY-MM-DD): instructions and pack it
            self.labe2 = tk.Label(button_frame, text="Enter Date (YYY-MM-DD): ", font=("Helvetica", 12, "bold"), fg="black", bg="lightblue")
            self.labe2.grid(row=4, column=1, padx=5)

            # Add horizontal separators between rows 1 and 2, and between rows 3 and 4
            separator1 = tk.Frame(button_frame, height=3, bd=2, relief="sunken")
            separator1.grid(row=2, column=0, columnspan=3, sticky="we", padx=5, pady=30)
            separator2 = tk.Frame(button_frame, height=3, bd=2, relief="sunken")
            separator2.grid(row=6, column=0, columnspan=3, sticky="we", padx=5, pady=20)

            """ Copy PIES Button """
            copy_pies_button = ButtonsFunction.CopyPiesButton(button_frame)
            copy_pies_button.button.grid(row=7, column=0, pady=20, padx=2)

            """ Copy SVP Button """
            copy_svp_button = ButtonsFunction.CopySvpButton(button_frame)
            copy_svp_button.button.grid(row=7, column=1, pady=20, padx=2)

            """ Copy Nodes 2 QGIS """
            copy_2_qgis_button = ButtonsFunction.CopyNode2QgisButton(button_frame)
            copy_2_qgis_button.button.grid(row=8, column=0, pady=20, padx=2)
            copy_2_qgis_button.button.grid_configure(sticky="nsew")

            """ Generate Operational Events """
            operational_events_button = ButtonsFunction.OperationEventButton(button_frame)
            operational_events_button.button.grid(row=8, column=1, pady=20, padx=2)
            operational_events_button.button.grid_configure(sticky="nsew")

            """ Create DPR Template Email"""
            create_dpr_button = ButtonsFunction.CreateDprEmail(button_frame)
            create_dpr_button.button.grid(row=9, column=0, columnspan=2, pady=10, padx=10, sticky="we")
            create_dpr_button.button.grid_configure(sticky="nsew")

            self.update_labels()
            root.mainloop()
            

        def update_title(self, root):
            # Get the current time and date
            now = datetime.now()
            current_time = now.strftime('%H:%M:%S')
            current_date = now.strftime('%Y-%m-%d')

            # set the window title with the current time and date
            root.title(f"QC Reports Generator - {VERSION} - {current_date} - {current_time}")

            # Schedule the update_title function to run every second
            root.after(1000, self.update_title, root)

        def update_labels(self):
            self.update_number_method2()
            # Schedule the update_labels function to be called every 5 minutes
            self.label_update_id = self.root.after(300000, self.update_labels)    

        def initiate_count(self, type):
            # Check if the cumulative spreadsheet has been updated recently
            if copier_method1.is_updated():
                # Copy the updated spreadsheet to the temp drive
                copier_method1.copy_table()

            # Filter data based on the current date (filer_by_date_and_operatio already reads the df)
            today = reportgen_method1.today()
            df_today = reportgen_method1.filter_by_date_and_operation(today, type)

            # Count the number of nodes deposited today
            return len(df_today)

        def update_number_method2(self):
            # Initializing paths and files 
            destination_directory = r'C:\Users\mta1.nv1.qccnslt\Documents\QC\Real_time_Prod'
            navview_path = r'Z:\06_SURVEY\Real-Time_Prod'
            navview_files = glob.glob(os.path.join(navview_path, '*_Fixes__*.txt'))
            
            # Creaing today and yesterdays dates 
            today = dtime.date.today()
            yesterday = today - dtime.timedelta(days=1)
            
            # Filter the files based on their creation time
            filtered_files = [
                file
                for file in navview_files
                if (yesterday <= dtime.date.fromtimestamp(os.path.getctime(os.path.join(navview_path, file))) <= today)        
            ]

            # Copy the filtered files to the destination directory
            for file in filtered_files:
                shutil.copy(os.path.join(navview_path, file), destination_directory)

            # Read all the .txt files in the destination directory into a DataFrame
            dataframes = []

            for file in os.listdir(destination_directory):
                file_path = os.path.join(destination_directory, file)
                if file.endswith('.txt') and os.path.getsize(file_path) > 0:
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
        
            # Update the lable with Live node count
            num_nodes_today = len(all_data_today)
            self.deployed_label.config(text=f'{LABEL_NODE_LIVE}' + str(num_nodes_today) + '\n')
    except Exception as e:  # Handle any exception and assign it to variable e
                # Log the error to a file for debugging
                with open('error_log.txt', 'a') as log_file:
                    log_file.write(f"Error: {e}\n")  # Use f-string for Python 3.6+
                print("ERROR", f"ERROR - {e}")

      