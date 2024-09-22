import tkinter as tk
from GenerateReports import GenerateReports
from tkinter import messagebox
from CopyCumulativeTable import CopyCumulativeTable
from GenerateReports import GenerateReports
from datetime import datetime
#from CopyAllNodesQgis_v2 import CopyAllNodesQgisv2
from CopyAllNodesQgis import CopyAllNodesQgis
from CopyPiesTable import CopyPiesTable
from CopySvpTable import CopySvpTable
from OperationEvents_v2 import EventProcessor
from dpr_email_template import DPRSender
# Load images Favicon and Logo
from resources_path import favicon2_path
# load variables from .conf file
from config_path import config

#Initiating CopyCumulativeTable class with PATHS and HEADERS to skip rows
cumulative_source = config.get('PATHS','CUMMULATIVE_SOURCE_FILE')
cumulative_destine = config.get('PATHS','CUMMULATIVE_COPIED_FILE')
copier = CopyCumulativeTable(cumulative_source, cumulative_destine)
copier.copy_table()
header_rows = int(config.get('PARAMS','CUMULATIVE_HEADERS'))

#Initializing GenerateReports Instance
reportgen = GenerateReports(cumulative_destine, header_rows)

#Final Excel with Sumarized events file paths (Desktop)
grouped_df_path = config.get("PATHS", "ACTIVITIES_VENTS")
summary_df_path = config.get("PATHS", "SUMMARY_EVENTS")

"""Initializing PopUp Windows for the Deployed Nodes Count Today and Recovered Nodes Count Today"""
FAVICON = favicon2_path

class PopupWindow:
    def __init__(self, parent, type, on_close_callback=None):
        copier.copy_table() # makung sure the latest cummulative is copied when opening the window
        self.is_closed = False # make sure the status closed is set to False and when close windows this will set to True
        favicon_file = FAVICON

        colorbg = "lightgreen"
        colorfg = "black"
        if type == 'Aslaid Time':
            hlabel = 'D '
            title = 'Deployed Nodes Count Today'
        else:
            title = 'Recovered Nodes Count Today'
            hlabel = 'R '
        self.parent = parent
        self.top = tk.Toplevel(parent)
        self.top.geometry("350x350")
        self.top.iconbitmap(favicon_file)
        self.top.title(title)
        self.top.configure(background=colorbg)
        self.num_nodes_today = self.initial_node_number(type)
        self.number_label = tk.Label(self.top, text=str(hlabel) + str(self.num_nodes_today), font=("Helvetica", 100, "bold"), fg=colorfg, bg=colorbg)
        self.number_label.place(relx=0.5, rely=0.5, anchor="center")
       
        self.chrono_label = tk.Label(self.top, text="00:00", font=("Helvetica", 25, "bold"), fg=colorfg, bg=colorbg)
        self.chrono_label.place(relx=0.8, rely=0.9, anchor="center")

        self.on_close_callback = on_close_callback
        self.top.protocol("WM_DELETE_WINDOW", self.close)
        
        self.number_id = None
        self.chrono_timer_id = None
        self.chrono_seconds = 0

        #self.start_chrono() # Starting Chronometer
        self.check_cumulative_updated(type) # calling function to update lables on Deploy and Recovery Buttons

    def start_chrono(self):
        self.chrono_seconds += 1
        minutes, seconds = divmod(self.chrono_seconds, 60)

        #check if window is visible 
        if self.chrono_label.winfo_exists():
            self.chrono_label.configure(text="{:02d}:{:02d}".format(minutes, seconds))
            self.chrono_timer_id = self.parent.after(1000, self.start_chrono)
    
    def reset_chrono(self):
        self.chrono_seconds = 0
        self.chrono_label.configure(text="00:00")

    def check_cumulative_updated(self, type):
        if self.is_closed:
            return 
        
        # Check if the cumulative spreadsheet has been updated recently
        if copier.is_updated():
            # Copy the updated spreadsheet to the temp drive
            copier.copy_table()
            # Update the number of nodes displayed in the popup window
            self.update_number(type)
            self.reset_chrono()  # Reset the chronometer after updating the node count
        else:
            # Reset the chronometer after updating the node count
            self.number_id = self.parent.after(60000, lambda: self.check_cumulative_updated(type))  # Check every 5 minutes

    def update_number(self, type):
        # Filter data based on the current date (filer_by_date_and_operatio already reads the mumulative into a DataFrame)
        today = reportgen.today()
        df_today = reportgen.filter_by_date_and_operation(today, type)
        # Count the number of nodes deposited today from the cummulative table
        self.num_nodes_today = len(df_today)

        if type == 'Aslaid Time':
            self.number_label.configure(text='D ' + str(self.num_nodes_today))
        else:
            self.number_label.configure(text='R ' + str(self.num_nodes_today))
            
        if not self.is_closed:
            # Schedule check_cumulative_updated() to be called every 5 minutes
            self.number_id = self.parent.after(60000, lambda: self.check_cumulative_updated(type))  # Check every 5 minutes
        

    # Defining a initial node number to be displayed when window is popup for safety, but I dont think its needed    
    def initial_node_number(self, type):
        today = reportgen.today()
        df_today = reportgen.filter_by_date_and_operation(today, type)
        self.num_nodes_today = len(df_today)    

    #closing and destroying the windows pop up when hit X buttom to close.
    def close(self):
        self.is_closed = True
        if self.number_id:
            self.parent.after_cancel(self.number_id)
            self.number_id = None
        if self.chrono_timer_id: #cancel chrono timer
            self.parent.after_cancel(self.chrono_timer_id)
            self.chrono_timer_id = None
        self.top.destroy()
        if self.on_close_callback is not None:
            self.on_close_callback()


""" start button classes for Tk buttons in App """

class DeployedNodesButton:
    """Deployed Node count Button to Start Popup Window """
    def __init__(self, parent):
        self.parent = parent
        self.button = tk.Button(parent, text="Deployed Count Today", font=("Helvetica", 20, "bold"), bg="#6699cc", fg="white", bd=2, relief="groove", command=self.click)
        self.popup_window = None

    def click(self):
        if self.popup_window is None:
            self.popup_window = PopupWindow(self.parent, 'Aslaid Time', self.on_popup_close)
            self.popup_window.update_number('Aslaid Time') # start updating the number
            self.popup_window.start_chrono()  # Start the chronometer
            self.button.configure(state="disabled")
            self.popup_window.top.wait_window()
            self.popup_window = None

    def on_popup_close(self):
        self.button.configure(state="normal")
        self.popup_window = None

class RecoveredNodesButton:
    """Deployed Node count Button to Start Popup Window """
    def __init__(self, parent):
        self.parent = parent
        self.button = tk.Button(parent, text="Recovered Count Today", font=("Helvetica", 20, "bold"), bg="#6699cc", fg="white", bd=2, relief="groove", command=self.clickr)
        self.popup_window = None

    def clickr(self):
        copier.copy_table()
        if self.popup_window is None:
            self.popup_window = PopupWindow(self.parent, 'Recovered Time', self.on_popup_close)
            self.popup_window.update_number('Recovered Time') #start updating the number
            self.popup_window.start_chrono()  # Start the chronometer
            self.button.configure(state="disabled")
            self.popup_window.top.wait_window()
            self.popup_window = None

    def on_popup_close(self):
        self.button.configure(state="normal")
        self.popup_window = None

class TodaysButton:
    """Generate Todays Report Button And Initializing the buttons and calling the needed functions for each button"""
    def __init__(self, parent):
         # Create Today's Report button and pack it    
        self.parent = parent
        self.button = tk.Button(parent, text="Today's Report", width=20, height=2, font=("Helvetica", 16, "bold"), bg="orange", fg="white", bd=2, relief="groove", command=self.create_todays_report)
        self.button.configure(activebackground="#3e8e41", activeforeground="white", disabledforeground="#cccccc")

    def create_todays_report(self):
        copier.copy_table()
        try:
            reportgen.create_tovery_reports('today','Aslaid Time')
            reportgen.create_tovery_reports('today','Recovered Time')
            
            #summarygen.save_node_summary_to_file('today','Aslaid Time')
            #summarygen.save_node_summary_to_file('today','Recovered Time')

            messagebox.showinfo("Today's Report", "Today's Report Created Successfully")
        except Exception as e:  # Handle any exception and assign it to variable e
            # Log the error to a file for debugging
            with open('error_log.txt', 'a') as log_file:
                log_file.write(f"Error: {e}\n")  # Use f-string for Python 3.6+
            messagebox.showerror("ERROR", "ERROR - Check Paths or Opended Tables", f"ERROR - {e}")

class YesterdaysButton:
    """Generate Yesterdays Report Button And Initializing the buttons and calling the needed functions for each button"""
    def __init__(self, parent):
        # Create Yesterdays's Report button and pack it
        self.parent = parent
        self.button = tk.Button(parent, text="Yesterdays's Report", width=20, height=2, font=("Helvetica", 16, "bold"), bg="orange", fg="white", bd=2, relief="groove", command=self.create_yesterdays_report)
        self.button.configure(activebackground="#3e8e41", activeforeground="white", disabledforeground="#cccccc")

    def create_yesterdays_report(self):
        copier.copy_table()
        try:
            
            reportgen.create_tovery_reports('yesterday','Aslaid Time')
            reportgen.create_tovery_reports('yesterday','Recovered Time')
            messagebox.showinfo("Yesterday's Report", "Yesterday's Report Created Successfully")  

        except Exception as e:  # Handle any exception and assign it to variable e
            # Log the error to a file for debugging
            with open('error_log.txt', 'a') as log_file:
                log_file.write(f"Error: {e}\n")  # Use f-string for Python 3.6+
            messagebox.showerror("ERROR", "ERROR - Check Paths or Opended Tables", f"ERROR - {e}")


class ToveriReportsButton:
    """Generate Toveri reports for a given date Button And Initializing the buttons and calling the needed functions for each button"""
    def __init__(self, parent):
        self.parent = parent
        self.button = tk.Button(parent, text="Toveri Report By Date", width=20, height=2, font=("Helvetica", 16, "bold"), bg="darkgreen", fg="white", bd=2, relief="groove", command=self.create_toveri_report_by_date)
        # Create an Entry widget for Toveri Report By Date and pack it
        self.entry1 = tk.Entry(parent, width=30, font=("Helvetica", 16, "bold"), borderwidth=3, relief="groove")
        self.entry1.grid(row=5, column=0, padx=20, pady=20)
        self.entry1.configure(background="white", foreground="black", insertbackground="red")
        self.entry1.grid_configure(sticky="nsew")

    def create_toveri_report_by_date(self):
        copier.copy_table()
        date_input = self.entry1.get()
        try:
            # Validate the date format
            datetime.strptime(date_input, "%Y-%m-%d")
            
            # If date is valid, proceed with report generation
            reportgen.create_tovery_reports(date_input, 'Aslaid Time')
            reportgen.create_tovery_reports(date_input, 'Recovered Time')
            messagebox.showinfo("Report for Date " + date_input, date_input + " - Reports Created Successfully")

        except ValueError:
            # If date format is incorrect, handle the exception
            with open('error_log.txt', 'a') as log_file:
                log_file.write(f"Invalid date format entered: {date_input}\n")
            messagebox.showerror("ERROR", "Wrong Date Format Entered. Use YYYY-MM-DD")
        except Exception as e:
            # Handle any other exceptions
            with open('error_log.txt', 'a') as log_file:
                log_file.write(f"Error: {e}\n")
            messagebox.showerror("ERROR", f"An unexpected error occurred: {e}")

class PbrReportsButton:
    """Generate Petrobras reports for a given date Button And Initializing the buttons and calling the needed functions for each button"""
    def __init__(self, parent):
        self.parent = parent
        self.button = tk.Button(parent, text="PBR Report By Date", width=20, height=2, font=("Helvetica", 16, "bold"), bg="darkgreen", fg="white", bd=2, relief="groove", command=self.create_pbr_reports)
        # Create an Entry widget for PBR Report By Date and pack it
        self.entry2 = tk.Entry(parent, width=30, font=("Helvetica", 16, "bold"), borderwidth=3, relief="groove")
        self.entry2.grid(row=5, column=1, padx=20, pady=20)
        self.entry2.configure(background="white", foreground="black", insertbackground="red")
        self.entry2.grid_configure(sticky="nsew")
 
    def create_pbr_reports(self):
        copier.copy_table()
        date_input = self.entry2.get()
        try:
            # Validate the date format
            datetime.strptime(date_input, "%Y-%m-%d")

            # If date is valid, proceed with report generation
            reportgen.create_pbr_report(date_input, 'Aslaid Time')
            reportgen.create_pbr_report(date_input, 'Recovered Time')
            messagebox.showinfo("Report for PBR - Date: " + date_input , date_input + " - PBR Report Created Successfully")
        except ValueError:
            # If date format is incorrect, handle the exception
            with open('error_log.txt', 'a') as log_file:
                log_file.write(f"Invalid date format entered: {date_input}\n")
            messagebox.showerror("ERROR", "Wrong Date Format Entered. Use YYYY-MM-DD")
        except Exception as e:
            # Handle any other exceptions
            with open('error_log.txt', 'a') as log_file:
                log_file.write(f"Error: {e}\n")
            messagebox.showerror("ERROR", f"An unexpected error occurred: {e}")

class CopyPiesButton:
    """Generate CopyPIES Button and initialize the button's command"""
    def __init__(self, parent):
        self.parent = parent
        # Configure the style for the Copy PIES button
        self.button = tk.Button(parent, text="Copy PIES", width=20, height=2, font=("Helvetica", 16, "bold"), bg="darkred", fg="white", bd=2, relief="groove", command=self.copy_pies)
        self.button.configure(activebackground="#3e8e41", activeforeground="white", disabledforeground="#cccccc")

    def copy_pies(self): 
        try:
            piescopier = CopyPiesTable()
            piescopier.copy_table()  # Copy the source file to the destination
            piescopier.read_table()   # Read the table into self.df_pies
            piescopier.write_new_pies()  # Write the cleaned DataFrame to the destination
            messagebox.showinfo("PIES Table Copy", "PIES Table Copied Successfully")
        except Exception as e:
            # Log the error to a file for debugging
            with open('error_log.txt', 'a') as log_file:
                log_file.write(f"Error: {e}\n")
            messagebox.showerror("ERROR", "ERROR - Check Paths or Opened Tables", f"ERROR - {e}")

class CopySvpButton:
    """Generate CopySVP Button And Initializing the buttons and calling the needed functions for each button"""
    def __init__(self, parent):
        self.parent = parent
        # create the Copy SVP button
        self.button = tk.Button(parent, text="Copy SVP", width=20, height=2, font=("Helvetica", 16, "bold"), bg="darkred", fg="white", bd=2, relief="groove", command=self.copy_svp)
        self.button.configure(activebackground="#3e8e41", activeforeground="white", disabledforeground="#cccccc")

    def copy_svp(self): 
        try:
            svpcopier = CopySvpTable()
            svpcopier.copy_table()
            svpcopier.read_table()
            svpcopier.write_new_svp()
            messagebox.showinfo(" SVP Table Copy", "SVP Table Copied Successfully")

        except Exception as e:  # Handle any exception and assign it to variable e
            # Log the error to a file for debugging
            with open('error_log.txt', 'a') as log_file:
                log_file.write(f"Error: {e}\n")  # Use f-string for Python 3.6+
            messagebox.showerror("ERROR", "ERROR - Check Paths or Opended Tables", f"ERROR - {e}")

class CopyNode2QgisButton:
    """Generate Copy All Nodes to QGIS Button And Initializing the buttons and calling the needed functions for each button"""
    def __init__(self, parent):
        self.parent = parent        
        # configure the style for the Copy Nodes to QGIS button
        self.button = tk.Button(parent, text="Copy All Nodes To QGIS", width=20, height=2, font=("Helvetica", 16, "bold"), bg="#4CAF50", fg="white", bd=2, relief="groove", command=self.copy_nodes_2_qgis)
        self.button.configure(activebackground="#3e8e41", activeforeground="white", disabledforeground="#cccccc")
        
    def copy_nodes_2_qgis(self):
        copier.copy_table()
        try:
            qgiscopier = CopyAllNodesQgis()
            qgiscopier.create_tables()
            messagebox.showinfo("PIES Table Copy", "Nodes Copied to QGIS CSV Successfully")
            
        except Exception as e:  # Handle any exception and assign it to variable e
            # Log the error to a file for debugging
            with open('error_log.txt', 'a') as log_file:
                log_file.write(f"Error: {e}\n")  # Use f-string for Python 3.6+
            messagebox.showerror("ERROR", "ERROR - Check Paths or Opended Tables", f"ERROR - {e}")

class OperationEventButton:
    """Generate Create Operational Events Button And Initializing the buttons and calling the needed functions for each button"""
    def __init__(self, parent):    
        self.parent = parent
        self.operation_events = config.get("PATHS", "INPUT_VENTS") #loads .xlsx data
        self.button = tk.Button(parent, text="Create Operational Events", width=20, height=2, font=("Helvetica", 16, "bold"), bg="#4CAF50", fg="white", bd=2, relief="groove", command=self.create_operational_events)
        self.button.configure(activebackground="#3e8e41", activeforeground="white", disabledforeground="#cccccc")

    def create_operational_events(self): 
        #Initiating Event Proccessor Instance
        processor = EventProcessor(self.operation_events, config)
        grouped_df, summary_df = processor.process(config)    
        #write excel files
        grouped_df.to_excel(grouped_df_path, index=False)
        summary_df.to_excel(summary_df_path, index=False)

class CreateDprEmail:
    """Generate Send DPR Email Button And Initializing the buttons and calling the needed functions for each button"""
    def __init__(self, parent):    
        self.parent = parent
        self.button = tk.Button(parent, text="Create DPR Email", font=("Helvetica", 20, "bold"), bg="red", fg="white", bd=2, relief="groove", command=self.click)
        self.button.configure(activebackground="#3e8e41", activeforeground="white", disabledforeground="#cccccc") 
        
    def click(self):
        email_section = dict(config.items('EMAIL'))
        emial_template_section = dict(config.items('EMAIL_TEMPLATE'))
        config_file = {**email_section, **emial_template_section}
        dpr_sender = DPRSender(config_file)
        dpr_sender.send_dpr_email()

