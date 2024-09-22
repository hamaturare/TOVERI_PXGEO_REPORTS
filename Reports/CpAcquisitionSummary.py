# This is the CpAcquisitionSummary_v2

# import classes
import pandas as pd
import os
import datetime as dtime
from datetime import datetime, timedelta


""" Returns yesterday's date as a string in the format YYY-MM-DD """            
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
today = (datetime.now().strftime("%Y-%m-%d"))
now = datetime.now()
current_hour = now.hour 

# Paths for source and destine files depending on our you create the report
today_dep_report = r'C:\Users\mta1.nv1.qccnslt\Desktop\Todays_Production_Deployed.xlsx'
today_rec_report = r'C:\Users\mta1.nv1.qccnslt\Desktop\Todays_Production_Recovered.xlsx'
yesterday_dep_report = r'C:\Users\mta1.nv1.qccnslt\Desktop\Yesterdays_Production_Deployed.xlsx'
yesterday_rec_report = r'C:\Users\mta1.nv1.qccnslt\Desktop\Yesterdays_Production_Recovered.xlsx'
acq_summary_file = r'C:\Users\mta1.nv1.qccnslt\Desktop\Acquisition_Summary_Day.txt'

if 21 <= current_hour < 24:
    if dtime.date.fromtimestamp(os.path.getmtime(today_dep_report)).day == now.day:    
        input_file_deployment = today_dep_report
        input_file_recovery = today_rec_report
        destination_file = acq_summary_file
    else:
        print('You are running this after 21h but before 0h, make sure you run the Todays report buttom to create report for Todays Prod UTC')    
else:
    if dtime.date.fromtimestamp(os.path.getmtime(yesterday_dep_report)).day == now.day:
        input_file_deployment = yesterday_dep_report
        input_file_recovery = yesterday_rec_report
        destination_file = acq_summary_file
    else: 
        print('You are running this after before 21h after 0h, make sure you run the Yesterdays report buttom to create report for Yesterdays Prod UTC')

def check_file():
    # Verify if table exist or if it's empity for safety give type variable the correpondent value
    df_deploy = pd.DataFrame()
    df_recovery = pd.DataFrame()

    try:
        if os.path.exists(input_file_deployment):
            df_deploy = pd.read_excel(input_file_deployment, header=0)
            print('Deploy File Exist')
        if os.path.exists(input_file_recovery):   
            df_recovery = pd.read_excel(input_file_recovery, header=0)
            print('Recovery File Exist')
    except:
         print('One of the files does not exist')
         print('Verify if the excel sheet Yesterdays_Production_Deplued/Recovered exists on the Desktop')

         return

    if df_deploy.shape[0] != 0 and df_recovery.shape[0] == 0: 
        type = 1 # 1 = Deployment; 2 = Recovery; 3 = Deployment and Recovery
        print('Only Deployment Nodes Production Yesterday')
        return type
    elif df_deploy.shape[0] == 0 and df_recovery.shape[0] != 0:
        type = 2 # 1 = Deployment; 2 = Recovery; 3 = Deployment and Recovery
        print('Only Recovery Nodes Production Yesterday')
        return type
    elif df_deploy.shape[0] != 0 and df_recovery.shape[0] != 0: 
        type = 3 # 1 = Deployment; 2 = Recovery; 3 = Deployment and Recovery
        print('Deployment and Recovery Production Yesterday')  
        return type
    elif df_deploy.shape[0] == 0 and df_recovery.shape[0] == 0:
        print('No Nodes Production Yesterday')
        type = 0
        return type

class CpAcquisitionSummary():

    def __init__(self, input_file_deployment, input_file_recovery, type):
        self.input_file_deployment = input_file_deployment
        self.input_file_recovery = input_file_recovery
        self.type = type
    
    def index2_msg(self,index,dataframe): # Function to change the Index warning message as needed
        #add_note = f" \t!!! Warnning !!!\t \n Node {dataframe['Line'][int(index)]} - {dataframe['Point'][index]} has Index {dataframe['Index'][int(index)]} \n"
        add_note = f"Node {dataframe['Line'][int(index)]} - {dataframe['Point'][index]} has Index {dataframe['Index'][int(index)]} \n"
        return add_note
    
    def get_node_summary(self):

        # Load data frame with deployment sheet, sort it by line then create total node_couts, and node counts per line
        df_deploy = pd.read_excel(self.input_file_deployment)
        node_count_deploy = len(df_deploy)
        line_counts_deploy = df_deploy['Line'].value_counts()
        line_counts_deploy = line_counts_deploy.sort_index(ascending=False)  

        # Load data frame with recovery sheet, sort it by line then create total node_couts, and node counts per line
        df_recovery = pd.read_excel(self.input_file_recovery)
        node_count_recovery = len(df_recovery)
        line_counts_recovery = df_recovery['Line'].value_counts()
        line_counts_recovery = line_counts_recovery.sort_index(ascending=False)

        """If There was no Node operation on this day """
        if type == 0:
            summary = f"No Nodes Production Today"
            return summary

        """If The operation performed was a Deployment """
        if type == 1:

            #df_filtered = pd.read_excel(self.input_file_deployment)
            #df_filtered = df_filtered.sort_values(by='Line')
            #node_count = len(df_filtered)
            #line_counts = df_filtered['Line'].value_counts()

            # Make a warning if there is any index above 1
            add_note =""
            for x in df_deploy.index:
                if df_deploy['Index'][x] > 1:
                    #add_note += f" \t!!! Warnning !!!\t \n Node {df_deploy['Line'][int(x)]} - {df_deploy['Point'][x]} has Index {df_deploy['Index'][int(x)]} \n"
                    add_note += self.index2_msg(x,df_deploy)

            summary = f"{node_count_deploy} nodes deployed today:\n"
            for line, count in line_counts_deploy.items():
                summary += f"\t RL {line} - {count} nodes deployed\n"
            
            # Add notes to Summary if there is any Index above 1
            summary = summary + "\n" + add_note

            return summary
        
        """If The operation performed was a Recovery"""
        if type == 2:
        
            #df_filtered = pd.read_excel(self.input_file_recovery)
            #node_count = len(df_filtered)
            #line_counts = df_filtered['Line'].value_counts()

            # Make a warning if there is any index above 1
            add_note =""
            for x in df_recovery.index:
                if df_recovery['Index'][x] > 1:
                    #add_note += f" \t!!! Warnning !!!\t \n Node {df_recovery['Line'][int(x)]} - {df_recovery['Point'][x]} has Index {df_recovery['Index'][int(x)]} \n"
                    add_note += self.index2_msg(x,df_recovery)

            summary = f"{node_count_recovery} nodes recovered today:\n"
            for line, count in line_counts_recovery.items():
                summary += f"\t RL {line} - {count} nodes recovered\n"
            
            # Add notes to Summary if there is any Index above 1
            summary = summary + "\n" + add_note

            return summary
        
        """If The operation performed was Deployment and recovery in the same day"""
        if type == 3:
            try:    
                #Deployment Count

                #df_filtered1 = pd.read_excel(self.input_file_deployment)
                #node_count1 = len(df_filtered1)
                #line_counts1 = df_filtered1['Line'].value_counts()

                # Make a warning if there is any index above 1
                add_note1 =""
                for x in df_deploy.index:
                    if df_deploy['Index'][x] > 1:
                        #add_note1 += f" \t!!! Warnning !!!\t \n On deployment - Node {df_deploy['Line'][int(x)]} - {df_deploy['Point'][x]} has Index {df_deploy['Index'][int(x)]} \n"
                        add_note1 += self.index2_msg(x,df_deploy)
                # Recovery Count

                #df_filtered2 = pd.read_excel(self.input_file_recovery)
                #node_count2 = len(df_filtered2)
                #line_counts2 = df_filtered2['Line'].value_counts()

                # Make a warning if there is any index above 1
                add_note2 =""
                for x in df_recovery.index:
                    if df_recovery['Index'][x] > 1:
                        #add_note2 += f" \t!!! Warnning !!!\t \n On recovery - Node {df_recovery['Line'][int(x)]} - {df_recovery['Point'][x]} has Index {df_recovery['Index'][int(x)]} \n"
                        add_note += self.index2_msg(x,df_recovery)
                
                summary = f"{node_count_deploy} nodes deployed today:\n"
                for line, count in line_counts_deploy.items():
                    summary += f"\t RL {line} - {count} nodes deployed\n"

                summary += "\n" + f"{node_count_recovery} nodes recovered today:\n"
                for line, count in line_counts_recovery.items():
                    summary += f"\t RL {line} - {count} nodes recovered\n"

                # Add notes to Summary if there is any Index above 1
                summary = summary + "\n" + add_note1 + "\n" + add_note2

                return summary
            
            except:
                print('Check if your tables exists')
    

    def save_node_summary_to_file(self, destination_file):
        print("Generating Acquisition sumary for: ", yesterday, ' Check the Acquisition_Summary_Day.txt file on Desktop')
        summary = self.get_node_summary()
        with open(destination_file, 'w') as f:
            f.write(summary)


# Initializing instances and calling function
type = check_file()
generate_summary = CpAcquisitionSummary(input_file_deployment, input_file_recovery, type)    
generate_summary.save_node_summary_to_file(destination_file)