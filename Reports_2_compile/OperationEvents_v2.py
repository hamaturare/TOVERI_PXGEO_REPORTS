# This is OperationEvents_v2

# Import Class
import pandas as pd
import chardet
# The path for the config file here is passed as an attribute when initializing this class on the ButtonsFuction.py

class EventProcessor:

    try:
        def __init__(self, operation_events, config_file):
            #file_encoding = self.detect_file_encoding(operation_events) #if a csv enable this line
            self.df = pd.read_excel(operation_events) #if a csv enable this --> , sep=',', encoding=file_encoding)
            self.important_remarks, self.exclude_remarks = self.load_config(config_file)

        @staticmethod
        def detect_file_encoding(file_path):
            with open(file_path, 'rb') as file:
                result = chardet.detect(file.read())
            return result['encoding']
        
        @staticmethod
        def load_config(config_file):
            # load variables from .conf file
            important_remarks = config_file.get("REMARKS", "important_remarks").split(',')
            exclude_remarks = config_file.get("REMARKS", "exclude_remarks").split(',')
        
            return important_remarks, exclude_remarks

        def process(self, config_file):
            self.df['Event'] = self.df['Event'].astype(str)
            event_names = dict(config_file.items('EVENT_NAMES'))
            grouped_data = []

            # Initialize variables to keep track of the current event and its start time
            current_event = None
            current_start_time = None

            for index, row in self.df.iterrows():
                if current_event is None:
                    # Set the current event and its start time
                    current_event = row['Event']
                    current_start_time = row['Start']
                elif current_event != row['Event']:
                    # If the event changes, add a row to the grouped data with the start and end times
                    grouped_data.append((current_event, current_start_time, self.df.loc[index - 1, 'End']))
                
                    # Update the current event and its start time
                    current_event = row['Event']
                    current_start_time = row['Start']
        
            # Add the last event to the grouped data
            grouped_data.append((current_event, current_start_time, self.df.loc[self.df.index[-1], 'End']))
        
            grouped_df = pd.DataFrame(grouped_data, columns=['Event', 'Start', 'End'])
        
            # Add the event names using the event_names dictionary
            grouped_df['Event Name'] = grouped_df['Event'].map(event_names).fillna('Other event not mapped')
        
            summary_df = self.create_summary()
            return grouped_df, summary_df
        
        def create_summary(self):
            include_condition = self.df['Remarks'].notna() & self.df['Remarks'].str.contains('|'.join(self.important_remarks))
            exclude_condition = self.df['Remarks'].apply(lambda x: x not in self.exclude_remarks)
            condition = include_condition & exclude_condition
            summary_df = self.df[condition]
            summary_df = summary_df.drop(columns=['Event'])
            return summary_df
    except Exception as e:  # Handle any exception and assign it to variable e
                # Log the error to a file for debugging
                with open('error_log.txt', 'a') as log_file:
                    log_file.write(f"Error: {e}\n")  # Use f-string for Python 3.6+
                print("ERROR", f"ERROR - {e}")
        
