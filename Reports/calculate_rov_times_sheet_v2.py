import pandas as pd

# Load the data from the provided Excel file
df = pd.read_excel(r'C:\Users\mta1.nv1.qccnslt\Desktop\Yesterdays_Production_Deployed.xlsx')

# Convert Time to a usable format: hours and minutes
df['Time'] = pd.to_datetime(df['Time']).dt.strftime('%H:%M')
df['Decimal'] = df['Time'].apply(lambda x: int(x.split(':')[0]) + int(x.split(':')[1]) / 60)

# Sort by 'Deployed by ROV' and 'Time'
df_sorted = df.sort_values(by=['Deployed by ROV', 'Time'])

# Calculate differences in deployment times and identify gaps over 30 minutes
# For the first entry of each ROV, calculate the difference from the start of the day (00:01)
# For the last entry of each ROV, calculate the difference from the end of the day (24:00)
start_of_day = 1 / 60  # 1 minute in decimal hours
end_of_day = 24  # End of the day in decimal hours
first_rows = df_sorted.groupby('Deployed by ROV').head(1).index
last_rows = df_sorted.groupby('Deployed by ROV').tail(1).index

df_sorted['Difference'] = df_sorted.groupby('Deployed by ROV')['Decimal'].diff().fillna(start_of_day)
df_sorted.loc[first_rows, 'Difference'] = df_sorted.loc[first_rows, 'Decimal'] - start_of_day
df_sorted.loc[last_rows, 'Difference'] = end_of_day - df_sorted.loc[last_rows, 'Decimal']
df_sorted['Gaps'] = df_sorted['Difference'].apply(lambda x: x if x > 0.5 else 0)

# Split the dataframe by ROV
uhd64_df = df_sorted[df_sorted['Deployed by ROV'] == 'UHD64'].copy()
xlx19_df = df_sorted[df_sorted['Deployed by ROV'] == 'XLX19'].copy()

# Function to append the sums to the DataFrame
def append_sums_to_df(df):
    sum_of_I = df['Difference'].sum()
    sum_of_J = df['Gaps'].sum()
    difference_I_J = sum_of_I - sum_of_J
    sums_df = pd.DataFrame({'Time': ['Total'], 'Decimal': [''], 'Difference': [sum_of_I], 'Gaps': [sum_of_J], 'I-J Difference': [difference_I_J]})
    df = pd.concat([df, sums_df], ignore_index=True)
    return df

# Append the sums to each ROV's DataFrame
uhd64_df_with_sums = append_sums_to_df(uhd64_df)
xlx19_df_with_sums = append_sums_to_df(xlx19_df)

# Export each updated DataFrame to a separate Excel file

uhd64_df_with_sums.to_excel(r'C:\Users\mta1.nv1.qccnslt\Desktop\UHD64_Deployment_Time_Summary.xlsx', index=False)
xlx19_df_with_sums.to_excel(r'C:\Users\mta1.nv1.qccnslt\Desktop\XLX19_Deployment_Time_Summary.xlsx', index=False)
