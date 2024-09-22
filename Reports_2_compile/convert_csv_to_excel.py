import os
import pandas as pd
import glob
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

folder_path =r'C:\Users\mta1.nv1.qccnslt\Documents\QC\Cumulative\Created_Reports\\'
excel_path =r'C:\Users\mta1.nv1.qccnslt\Documents\QC\Cumulative\Created_Reports\excel\\'
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
#Copy Node Stats to local folder and convert to .xlsx

for file in csv_files:
    toveri_report = pd.read_csv(file)
    path = excel_path + os.path.splitext(os.path.basename(file))[0] + ".xlsx"
    toveri_report.to_excel(path, index=False)
