import shutil
import pandas as pd
# load variables from .conf file
from config_path import config

class CopyPiesTable:
    def __init__(self):
        self.source_path = config.get('PATHS', 'PIES_SOURCE_FILE')
        self.destination_path = config.get('PATHS', 'PIES_DESTINATION_FILE')
        self.df_pies = None

    def copy_table(self):
        # Copy the source table to the destination
        shutil.copyfile(self.source_path, self.destination_path)

    def read_table(self):
        # Read the table from the destination path
        try:
            self.df_pies = pd.read_csv(self.destination_path)
        except Exception:
            self.df_pies = pd.read_excel(self.destination_path)

    def write_new_pies(self):
        if self.df_pies is not None and not self.df_pies.empty:
            # Replace NaN values with empty strings
            filled_df = self.df_pies.fillna('')  # Replace NaN with blank values
            
            # Write the updated DataFrame to the destination file
            filled_df.to_csv(self.destination_path, index=False)
        else:
            # Log the error to a file
            with open('error_log.txt', 'a') as log_file:
                log_file.write("Error: DataFrame is not loaded or is empty.\n")

                
# Usage Debug
"""
from tkinter import messagebox
try:
    piescopier = CopyPiesTable()
    piescopier.copy_table()  # Copy the source file to the destination
    piescopier.read_table()   # Read the table into self.df_pies
    piescopier.write_new_pies()  # Write the cleaned DataFrame to the destination
    messagebox.showinfo("PIES Table Copy", "PIES Table Copied Successfully")
    print(piescopier)
except Exception as e:  # Handle any exception and assign it to variable e
    # Log the error to a file for debugging
    with open('error_log.txt', 'a') as log_file:
        log_file.write(f"Error: {e}\n")  # Use f-string for Python 3.6+
    print("ERROR", f"ERROR - {e}")
"""