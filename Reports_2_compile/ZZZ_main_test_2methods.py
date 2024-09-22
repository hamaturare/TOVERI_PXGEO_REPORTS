import tkinter as tk
import tkinter.ttk as ttk
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
# load variables from .conf file
from config_path import config

VERSION = 'v7.0'
#Initiating CopyCumulativeTable class with PATHS and HEADERS to skip rows
cumulative_source = config.get('PATHS','CUMMULATIVE_SOURCE_FILE')
cumulative_destine = config.get('PATHS','CUMMULATIVE_COPIED_FILE')
copier_method1 = CopyCumulativeTable(cumulative_source, cumulative_destine)
copier_method1.copy_table()
header_rows = int(config.get('PARAMS','CUMULATIVE_HEADERS'))

#Initializing GenerateReports Instance
reportgen_method1 = GenerateReports(cumulative_destine, header_rows)
LABEL_NODE_LIVE = '\n Node Count Live: \n'
class Main:
 
    def __init__(self):

        self.Markbox = False
        self.method1 = True

        """ tk windows parameters """
        # create the main window
        root = tk.Tk()
        root.geometry("1180x850")
        root.config(bg="white")
        root.iconbitmap(r'C:\Users\mta1.nv1.qccnslt\Documents\python\icons\toveri_icon_python.ico')
        root.resizable(False, False)
        # Set the title with date and clock
        self.update_title(root)
        self.root = root

        """initializing a frame to hold buttons"""
        button_frame = tk.Frame(root, bd=5, bg="lightblue", relief="groove")
        button_frame.grid(padx=10, pady=10)
        root.grid_columnconfigure(0, weight=1)

        # create a frame for the logo
        logo_frame = tk.Frame(button_frame)
        # pack the logo frame into the main window
        logo_frame.grid(row=8, column=2, rowspan=2)  # specify row and column for logo frame
        logo_path = r'C:\Users\mta1.nv1.qccnslt\Pictures\ToveriLogo.png'
        # load the logo image using PIL
        image = Image.open(logo_path)
        new_size = (image.width * 2, image.height * 2)
        logo_image = image.resize(new_size)
        logo_photo = ImageTk.PhotoImage(logo_image)
        # create a label for the logo and display it on the frame
        logo_label = tk.Label(logo_frame, image=logo_photo)
        logo_label.grid(row=9, column=2)  # specify row and column for logo


        ########## Starting Tk's buttons parametrization ###########
        # Add the checkbox for selecting the method
        if self.Markbox:
            self.check_var = tk.BooleanVar()
            self.check_var.trace("w", self.toggle_method)
            self.check_button = tk.Checkbutton(button_frame, text="Real Time Count", variable=self.check_var)
            self.check_button.grid(row=0, column=2)

        # Add Node Count - one Label version
       
        self.deployed_label = tk.Label(button_frame, bd=3, relief="solid", text=f'{LABEL_NODE_LIVE}' + str(self.initiate_count('Aslaid Time')) + '\n', font=("Helvetica", 24, "bold"), fg="black", bg="lightgreen", height=3)
        self.deployed_label.grid(row=0, column=2, padx=10, pady=10, sticky="we")

        # Add the display labels for deployed and recovered nodes
        #self.deployed_label = tk.Label(button_frame, text=f'Deployed Nodes Today: ' + str(self.initiate_count('Aslaid Time')), font=("Helvetica", 16, "bold"), fg="black", bg="lightgreen", height=2)
        #self.deployed_label.grid(row=0, column=0, columnspan=1, pady=10, padx=10, sticky="we")

        #self.recovered_label = tk.Label(button_frame, text=f'Recovered Nodes Today: ' + str(self.initiate_count('Recovered Time')), font=("Helvetica", 16, "bold"), fg="black", bg="lightgreen", height=2)
        #self.recovered_label.grid(row=0, column=1, columnspan=1, pady=10, padx=10, sticky="we")

        """ Deployed Node Count Button Update """
        fancy_button = ButtonsFunction.DeployedNodesButton(button_frame)
        fancy_button.button.grid(row=0, column=0, pady=10, padx=10, sticky="we")
        #fancy_button.button.grid_configure(sticky="nsew")

        """ Recovered Node Count Button Update """
        fancy_button = ButtonsFunction.RecoveredNodesButton(button_frame)
        fancy_button.button.grid(row=0, column=1, pady=10, padx=10, sticky="we")
        #fancy_button.button.grid_configure(sticky="nsew")

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

        root.mainloop()

    def update_title(self, root):
        # Get the current time and date
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        current_date = now.strftime('%Y-%m-%d')

        # set the window title with the current time and date
        root.title(f"QC Reports Generator {VERSION} - {current_date} - {current_time}")

        # Schedule the update_title function to run every second
        root.after(1000, self.update_title, root)

    def toggle_method(self, *args):
        self.method1 = self.check_var.get()
        self.update_labels()

    def update_labels(self):
        # Update the labels depending on the selected method
        if self.Markbox and self.method1:
            self.update_number_method2('Aslaid Time')
            self.update_number_method2('Recovered Time')
        if not self.Markbox and self.method1:
            self.update_number_method2('Aslaid Time')
            self.update_number_method2('Recovered Time')
        if self.Markbox and not self.method1:
            self.update_number_method1('Aslaid Time')
            self.update_number_method1('Recovered Time')
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
    
    def update_number_method1(self, type):
        # Check if the cumulative spreadsheet has been updated recently
        if copier_method1.is_updated():
            # Copy the updated spreadsheet to the temp drive
            copier_method1.copy_table()

        # Update the labels
        if type == 'Aslaid Time':
            num_nodes_today = self.initiate_count(type)
            self.deployed_label.config(text=f'Deployed Nodes Today: ' + str(num_nodes_today))
        #else:
        #    num_nodes_today = self.initiate_count(type)
        #    self.recovered_label.config(text=f'Recovered Nodes Today: ' + str(num_nodes_today))

    def update_number_method2(self, type):
        # Initializing paths and files 
        destination_directory = r'C:\Users\mta1.nv1.qccnslt\Documents\QC\Real_time_Prod'
        navview_path = r'Z:\06_SURVEY\Real-Time_Prod'
        navview_files = glob.glob(os.path.join(navview_path, '*_Fixes__*.txt'))
        
        # Creaing today and yesterdays dates 
        today = dtime.date.today()
        yesterday = today - dtime.timedelta(days=1)
        
        # Filter the files based on their creation time
        #navview_files = sorted(navview_files, key=lambda x: os.path.getctime(os.path.join(navview_path, x)), reverse=True ) # sort file by creation time.
        
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
       
        if type == 'Aslaid Time':
            num_nodes_today = len(all_data_today)
            self.deployed_label.config(text=f'{LABEL_NODE_LIVE}' + str(num_nodes_today) + '\n')
            #num_nodes_today = len(all_data_today)
            #self.deployed_label.config(text=f'Deployed Nodes Today: ' + str(num_nodes_today))
        #else:
        #    num_nodes_today = len(all_data_today)
        #    self.recovered_label.config(text=f'Recovered Nodes Today: ' + str(num_nodes_today))
      