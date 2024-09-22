import pandas as pd
import glob
import os
from datetime import datetime, timedelta

def get_yesterday_date():
    # Get yesterday's date in the format YYYY-MM-DD
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

def get_latest_files(file_folder_path, date):
    try:
        # Get a list of all deployment files for yesterday's date
        latest_files_deployed = glob.glob(os.path.join(file_folder_path, f'NodeProduction_Deployed_{date}*.xlsx'))
        # Sort the list of files by creation time (most recent first)
        latest_files_deployed.sort(key=os.path.getctime, reverse=True)

        # Get a list of all recovery files for yesterday's date
        latest_files_recovered = glob.glob(os.path.join(file_folder_path, f'NodeProduction_Recovered_{date}*.xlsx'))
        # Sort the list of files by creation time (most recent first)
        latest_files_recovered.sort(key=os.path.getctime, reverse=True)

        # Get the most recent file from each category, if available
        deployed_file = latest_files_deployed[0] if latest_files_deployed else None
        recovered_file = latest_files_recovered[0] if latest_files_recovered else None

        return deployed_file, recovered_file
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

# Function to update the RP column
def update_rp(row):
    event_number = row['Event'][1:]  # Extracts the number after 'D' or 'R'
    row['RP'] = str(row['RP']) + event_number  # Concatenates the extracted number to the RP value
    return row

# Temporary function while waiting for PXGEO to change the Index naming convention
def update_event(row):
    event_word = row['Event'][:1]  # Extracts the 'R' or 'D'
    row['Event'] = event_word + "1"  # Appends the number "1"
    return row

file_folder_path = 'C:\\Users\\mta1.nv1.qccnslt\\Desktop\\PBR_Production'
yesterday_date = get_yesterday_date()
deployed_file, recovered_file = get_latest_files(file_folder_path, yesterday_date)

# Process the deployed file if it exists
if deployed_file:
    df_deployed = pd.read_excel(deployed_file)  # Load the DataFrame from the deployed file
    df_deployed = df_deployed.apply(update_rp, axis=1)  # Apply the update_rp function

    # Uncomment when PXGEO fixes the Index naming convention
    df_deployed = df_deployed.apply(update_event, axis=1)  # Apply the update_event function

    # Save the updated DataFrame for deployed file
    updated_deployed_file = os.path.join(
        'C:\\Users\\mta1.nv1.qccnslt\\Desktop\\PBR_Production\\Index_Updated',
        f"{os.path.splitext(os.path.basename(deployed_file))[0]}_Index_Updated.xlsx"
    )
    df_deployed.to_excel(updated_deployed_file, index=False)

    # Check outputs for deployed file
    print("Deployed File:")
    print(df_deployed.head())
    print(len(df_deployed))
else:
    print("No Deployment production Yesterday or no file was generated yet.")

# Process the recovered file if it exists
if recovered_file:
    df_recovered = pd.read_excel(recovered_file)  # Load the DataFrame from the recovered file
    df_recovered = df_recovered.apply(update_rp, axis=1)  # Apply the update_rp function

    # Uncomment when PXGEO fixes the Index naming convention
    df_recovered = df_recovered.apply(update_event, axis=1)  # Apply the update_event function

    # Save the updated DataFrame for recovered file
    updated_recovered_file = os.path.join(
        'C:\\Users\\mta1.nv1.qccnslt\\Desktop\\PBR_Production\\Index_Updated',
        f"{os.path.splitext(os.path.basename(recovered_file))[0]}_Index_Updated.xlsx"
    )
    df_recovered.to_excel(updated_recovered_file, index=False)

    # Check outputs for recovered file
    print("Recovered File:")
    print(df_recovered.head())
    print(len(df_recovered))
else:
    print("No Recovery production Yesterday or no file was generated yet.")
