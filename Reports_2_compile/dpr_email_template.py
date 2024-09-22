import os
import re
import PyPDF2
import pandas as pd
import datetime
import win32com.client as win32
import glob
import locale
import calendar
# load variables from .conf file
from config_path import config

class DPRSender:
    def __init__(self, config):
        self.config = config
    try:
        def get_latest_pdf_file(self, pdf_folder_path):
            
            """
            Given a path to a folder containing PDF files, returns the path to the latest PDF file.
            """
            # Get a list of all PDF files in the folder
            pdf_files = glob.glob(os.path.join(pdf_folder_path, '*.pdf'))
            # Sort the list of files by creation time (most recent first)
            pdf_files.sort(key=os.path.getctime, reverse=True)
            # Return the path to the latest PDF file
            return pdf_files[0]

        # Function to read PDF and extract required data
        def read_pdf(self, file):
            page_shot_pt = config.get("PARAMS", "PDF_PAGE_SOURCE_POINT") # config file to change the page to look for Daily Source Plot on PDF
            deployed_nodes_daily_regex = config.get("PARAMS", "DEPLOYED_DAILY_REGEX")
            recovered_nodes_daily_regex = config.get("PARAMS", "RECOVERED_DAILY_REGEX")
            #print(f'deployed dayly param: {deployed_nodes_daily_regex}',f'recovered dayly param: {recovered_nodes_daily_regex}')
            
            # Initialize PDF reader
            pdf = PyPDF2.PdfReader(file)

            # Initialize extracted information variables
            deployed_nodes_day = 'N/A'
            recovered_nodes_day = 'N/A'
            shot_points = 'N/A'

            # Iterate through PDF pages and extract the required information

            #FOR SOURCE VESSEL SHOT POINT
            search_text1 = config.get("PARAMS", "SEARCH_TEXT1")
            search_text2 = config.get("PARAMS", "SEARCH_TEXT2")

            # FOR NODE VESSEL DEPLOYED AND RECOVERED NODES DAILY
            search_text3 = config.get("PARAMS", "SEARCH_TEXT3")
            search_text4 = config.get("PARAMS", "SEARCH_TEXT4")
            period_index_find = config.get("PARAMS", "PERIOD_INDEX_FIND")
            

            for page_num in range(len(pdf.pages) - 4):
                # Extract text from the current page
                page_text = pdf.pages[page_num].extract_text()
                
                if search_text1 in page_text and search_text2 in page_text: #page_num == int(page_shot_pt): # Find the Total shots of the day on first page
                    start_index = page_text.find(search_text1) 
                    newline_index = page_text.find("\n", start_index) # Find the index of the next newline character after the "Daily" row
                    shot_points = page_text[newline_index+1:].split()[0] # Grabe the Total Production Shots of the day on First page
                
                if search_text3 in page_text and search_text4 in page_text: # and search_text4 in page_text: # Usado dependendo da quebra e pagina
                    receiver_activity_index = page_text.find(search_text3)
                    period_index = page_text.find(period_index_find, receiver_activity_index)
                    daily_index = page_text.find(search_text4, period_index)

                    #IMPORTANT REGEX TO FIND THE CORRECT TEXT
                    deployed_regex = str(deployed_nodes_daily_regex)
                    recovered_regex = str(recovered_nodes_daily_regex)
                    deployed_search = re.search(deployed_regex, page_text[daily_index:]) 
                    recovered_search = re.search(recovered_regex, page_text[daily_index:])

                    if deployed_search:
                        deployed_nodes_day = deployed_search.group(1) # only sores variable if search is successful

                    if recovered_search:
                        recovered_nodes_day = recovered_search.group(1) # only sores variable if search is successful
            
            return deployed_nodes_day, recovered_nodes_day, shot_points

        def load_email_list(self, file):
            if file.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                df = pd.read_csv(file)

            to = df['to'].dropna().tolist()
            cc = df['cc'].dropna().tolist()

            return to, cc

        def create_email(self, deployed_nodes_day, recovered_nodes_day, shot_points, config):
            # Load email addresses and CCs from the email list file
            to, cc = self.load_email_list(self.config['email_list_file'])

            # Initialize an Outlook object for the email
            outlook = win32.Dispatch('outlook.application')
            email_msg = outlook.CreateItem(0)

            # Date Format from pdf file name
            date_match = re.search(r'(\d{4})(\d{2})(\d{2})', os.path.basename(self.config['pdf_file']))
            year = date_match.group(1)
            month = date_match.group(2)
            day = date_match.group(3)
            date_str = f"{year}-{month}-{day}"

            # Set email subject
            locale.setlocale(locale.LC_TIME, 'pt_PT.UTF-8')
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            month_abbr = calendar.month_abbr[date_obj.month].title()
            formatted_date = date_obj.strftime(f'%d {month_abbr} %Y')
            email_msg.Subject = f"{self.config['project_name']} DPR {formatted_date}"
            email_msg.To = "; ".join(to)
            email_msg.CC = "; ".join(cc)

            # Read email body template from the configuration file
            email_body_template = self.config['email_body']
            
            # Replace placeholders in the template with actual values
            email_body = email_body_template.format(
                formatted_date=formatted_date,
                node_boat_name=self.config['node_boat_name'],
                deployed_nodes_day=deployed_nodes_day,
                recovered_nodes_day=recovered_nodes_day,
                node_boat_letters=self.config['node_boat_letters'],
                gun_boat_name=self.config['gun_boat_name'],
                shot_points=shot_points,
                gun_boat_letters=self.config['gun_boat_letters'],
                chase_vessel_name=self.config['chase_vessel_name']
            )
            signature_name = config['signature_name']
            # Get default signatures
            signature_directory = os.path.join(os.environ['APPDATA'], 'Microsoft\\Signatures')
            signature_file = os.path.join(signature_directory, signature_name)
                                            
            with open(signature_file, 'r', encoding='utf-8') as f:
                default_signature = f.read()
            
            # Add default signature to email body
            email_body += f"<br><br>{default_signature}"
            
            email_msg.HTMLBody = email_body
            
            # Attach the PDF file
            filename = self.config['pdf_file']
            outlook_attachment = email_msg.Attachments.Add(Source=filename, DisplayName=os.path.basename(filename))

            return email_msg

        def send_dpr_email(self):
            #self.config = config
            pdf_file = self.get_latest_pdf_file(self.config['pdf_file'])
            deployed_nodes_day, recovered_nodes_day, shot_points = self.read_pdf(pdf_file)
            self.config['pdf_file'] = pdf_file
            email_msg = self.create_email(deployed_nodes_day, recovered_nodes_day, shot_points, self.config)

            # Display the email in the Outlook email editor
            email_msg.Display()
    except Exception as e:  # Handle any exception and assign it to variable e
            # Log the error to a file for debugging
            with open('error_log.txt', 'a') as log_file:
                log_file.write(f"Error: {e}\n")  # Use f-string for Python 3.6+
            print("ERROR",f"ERROR - {e}")

#### Enable to Debug if Needed ####
"""
email_section = dict(config.items('EMAIL'))
emial_template_section = dict(config.items('EMAIL_TEMPLATE'))
config_file = {**email_section, **emial_template_section}
dpr_sender = DPRSender(config_file)
dpr_sender.send_dpr_email()
"""
