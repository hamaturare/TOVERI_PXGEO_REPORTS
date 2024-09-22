import pandas as pd
import datetime
from datetime import datetime, timedelta
# load variables from .conf file
from config_path import config

class GenerateReports:
    """ Creates a class to read the cumulative table and generate all necessary reports """
    toveri_reports_path = config.get('PATHS', 'TOVERI_REPORTS_PATH')
    tovery_bydate_path = config.get('PATHS', 'TOVERI_REPORTS_BY_DATE_PATH')
    pbr_reports_path = config.get('PATHS', 'PBR_REPORTS_PATH')
    
    def __init__(self, destination_path, headers, cp_acquisition_summary=None):
        self.destination_path = destination_path
        self.headers = headers
        self.cp_acquisition_summary = cp_acquisition_summary
        """ Defining destination paths for each report """
            
    def read_table(self):
        """ Reads a CSV Table file and returns a data frame """
        return pd.read_csv(self.destination_path, skiprows=self.headers, encoding='latin1')
        
    def today(self):
        """ Returns today's date as a string in the format YYYY-MM-DD """
        return datetime.now().strftime("%Y-%m-%d")
        
    def yesterday(self):
        """ Returns yesterday's date as a string in the format YYYY-MM-DD """
        return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
    def filter_by_date_and_operation(self, date, type):
        """ filters a data frame by the dates and type of operation Deployment(Aslaid) or Recovered """
        self.df = self.read_table()
        return self.df[self.df[str(type)].astype(str).str.startswith(date)]
            
    def create_columns(self, date, type):
        """ Creating new columns DATE and TIME with the desired format to be added to data frame """
        self.df_filtered = self.filter_by_date_and_operation(date, type).copy()  # Make a copy to avoid the SettingWithCopyWarning
        
        # Create the DATE and TIME columns with the desired format
        self.df_filtered.loc[:, 'Date'] = self.df_filtered.loc[:, str(type)].apply(lambda x: x[:10] if isinstance(x, str) else x)
        self.df_filtered.loc[:, 'Time'] = self.df_filtered.loc[:, str(type)].apply(lambda x: x[11:23] if isinstance(x, str) else x)

        return self.df_filtered
        
    def create_tovery_reports(self, date, type):
        """ Defining Columns for Deployment Table or Recovery table for Toveri """
        toveri_deployment_columns = config.get('COLUMNS', 'TOVERI_DEPLOYMENT_COLUMNS').split(',')
        toveri_recovery_columns = config.get('COLUMNS', 'TOVERI_RECOVERY_COLUMNS').split(',')
        
        if date == 'today':
            """ Filter the dates on dataframe that are only from today and create Date and Time columns """
            date = self.today()
            report_today = self.create_columns(date, type)

            if type == 'Aslaid Time':
                """ Select and order the desired columns """
                toveri_report = report_today[toveri_deployment_columns]
                toveri_report.to_excel(self.toveri_reports_path + 'Todays_Production_Deployed.xlsx', index=False)

            elif type == 'Recovered Time':
                """ Select and order the desired columns """
                toveri_report = report_today[toveri_recovery_columns]
                toveri_report.to_excel(self.toveri_reports_path + 'Todays_Production_Recovered.xlsx', index=False) 

        elif date == 'yesterday':
            """ Filter the dates on dataframe that are only from yesterday """
            date = self.yesterday()
            report_yesterday = self.create_columns(date, type)

            if type == 'Aslaid Time':
                """ Select and order the desired columns """
                toveri_report = report_yesterday[toveri_deployment_columns]
                toveri_report.to_excel(self.toveri_reports_path + 'Yesterdays_Production_Deployed.xlsx', index=False)

            elif type == 'Recovered Time':
                """ Select and order the desired columns """
                toveri_report = report_yesterday[toveri_recovery_columns]
                toveri_report.to_excel(self.toveri_reports_path + 'Yesterdays_Production_Recovered.xlsx', index=False)

        else:
            """ Filter the dates on dataframe by given date """
            report_by_date = self.create_columns(date, type)
        
            if type == 'Aslaid Time' and not report_by_date.empty:
                """ Select and order the desired columns """
                toveri_report = report_by_date[toveri_deployment_columns]
                toveri_report.to_excel(self.tovery_bydate_path + date + "_Production_Deployed.xlsx", index=False)

            elif type == 'Recovered Time' and not report_by_date.empty:
                """ Select and order the desired columns """
                toveri_report = report_by_date[toveri_recovery_columns]
                toveri_report.to_excel(self.tovery_bydate_path + date + "_Production_Recovered.xlsx", index=False)
                
    def create_pbr_report(self, date, type):
        """ Filter the dates on dataframe by given date """
        df_format = self.create_columns(date, type)

        """ Establish date, time and index columns formats as PBR request """
        df_format['Date'] = df_format['Date'].apply(lambda x: pd.to_datetime(x).strftime('%d/%m/%Y'))
        df_format['Time'] = df_format['Time'].apply(lambda x: pd.to_datetime(x).strftime('%H:%M:%S'))
        df_format['Index'] = df_format['Index'].apply(lambda x: 'D{}'.format(x) if type == 'Aslaid Time' else 'R{}'.format(x))
        
        """ Create new DataFrame with new columns with PBR format """
        pbr_report_date = df_format

        """ Create new DataFrame with 2 blank columns for PBR format """
        pbr_report_date['BLANK'] = '' 
        
        """ Defining Columns for Deployment Table or Recovery table for PBR """
        pbr_deployment_columns = config.get('COLUMNS', 'PBR_DEPLOYMENT_COLUMNS').split(',')
        pbr_recovery_columns = config.get('COLUMNS', 'PBR_RECOVERY_COLUMNS').split(',')
        pbr_renamed_columns = config.get('COLUMNS', 'PBR_RENAMED_COLUMNS').split(',')

        """ Create new DataFrame with PBR format columns only """
        pbr_report_deployed = pbr_report_date[pbr_deployment_columns]
        pbr_report_recovered = pbr_report_date[pbr_recovery_columns]

        if type == 'Aslaid Time' and not pbr_report_deployed.empty:
            """ Rename the columns for PBR format """
            pbr_report_deployed.columns = pbr_renamed_columns
            
            """ Output the Excel file with the desired format for PBR Deployment """
            pbr_excel_file = self.pbr_reports_path + "NodeProduction_Deployed_" + date + ".xlsx"
            pbr_report_deployed.to_excel(pbr_excel_file, index=False)
            
        elif type == 'Recovered Time' and not pbr_report_recovered.empty:
            """ Rename the columns for PBR format """
            pbr_report_recovered.columns = pbr_renamed_columns
            
            """ Output the Excel file with the desired format for PBR Recovery """
            pbr_excel_file = self.pbr_reports_path + "NodeProduction_Recovered_" + date + ".xlsx"
            pbr_report_recovered.to_excel(pbr_excel_file, index=False) 

    def handle_errors(self):
        """Handle any exception and log errors"""
        try:
            # Place the code where exceptions might occur
            pass
        except Exception as e:
            # Log the error to a file for debugging
            with open('error_log.txt', 'a') as log_file:
                log_file.write(f"Error: {e}\n")  # Use f-string for Python 3.6+
            print("ERROR", f"ERROR - {e}")
