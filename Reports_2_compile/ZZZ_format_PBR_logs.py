import os
import pandas as pd
import glob
import warnings
from openpyxl import load_workbook

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

folder_path =r'C:\Users\mta1.nv1.qccnslt\Desktop\PBR_Production\\'
formated_path =r'C:\Users\mta1.nv1.qccnslt\Desktop\PBR_Production\Formated\\'

def copy_daily_log(folder_path, formated_path):
    # Get a list of all xlsm files in the folder
    log_files = glob.glob(os.path.join(folder_path, '*.xlsx'))
    log_files = [f for f in log_files if not os.path.basename(f).startswith('~')] # exclude temporary files
    log_files.sort(key=os.path.getctime, reverse=True) # Sorting files by creation time
    log_file = log_files[0] # take the last created log on folder

    #read excel file into df
    df = pd.read_excel(log_file)

    formated_report.to_excel(formated_path, index=False)
