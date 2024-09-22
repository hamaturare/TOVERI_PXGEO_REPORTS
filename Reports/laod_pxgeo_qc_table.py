import pandas as pd
import shutil

#Qc Sheets Pxgeo Path
qc_table =r'Z:\03_QC\21-Nodes_Stats_and_followup\0256_SEPIA_QC_node.xlsx'
Node_stats = r'Z:\03_QC\21-Nodes_Stats_and_followup\0256_3D_SEPIA_Nodes_Stats.csv'

#Path to copy Qc Sheets
qc_table_copy = r'C:\Users\mta1.nv1.qccnslt\Documents\003023-Sepia\QC\0256_Sepia_QC_node.xlsx'
Node_stats_copy = r'C:\Users\mta1.nv1.qccnslt\Documents\003023-Sepia\QC\0256_Sepia_Nodes_Stats.xlsx'

#Copy Qc Sheets to local folder.
shutil.copyfile(qc_table, qc_table_copy)
shutil.copyfile(Node_stats, Node_stats_copy)

#Copy Node Stats to local folder and convert to .xlsx
read_file = pd.read_csv(Node_stats)
read_file.to_excel(Node_stats_copy, index=False, header=True, sheet_name='Nodes_Stats')

#reading QC Table from Pxgeo to use in QGIS
df = pd.read_excel(qc_table, skiprows=4, index_col=None, na_values=['NA'], usecols="A,B,D,G,N,O,R,S,T,U,AI,AJ")
df.rename(columns = {'RPS\nRecov\nX' : 'Recovery X', 'RPS\nRecov\nY' : 'Recovery Y', 'Recalc\nX' : 'Seismic X', 'Recalc\nY' : 'Seismic Y', 'rcvidx':'Index'}, inplace=True )

filtered_index1_df = df[df['Index'] == 1]

CSV_QC_TABLE = r'C:\Users\mta1.nv1.qccnslt\Documents\003023-Sepia\QC\0256_Sepia_node_2export.csv'
filtered_index1_df.to_csv(CSV_QC_TABLE, index=False)

        
def copyTableColumns(self):
    #SOURCE SHET QC TABLE

    source_file = qc_table_copy
    source_sheet_name = 'AllNodes'
    columns_to_copy = ['QC','DATA_Codes','Blocked','Fault','Comments']

    source_data = pd.read_excel(source_file, sheet_name=source_sheet_name, skiprows=4)
    source_data_subset = source_data[columns_to_copy]


    #TARGET SHEET TOVERI QC 
    target_file = r'C:\Users\mta1.nv1.qccnslt\Documents\003023-Sepia\TOVERI Sepia Control_QC_V1.xlsm'
    target_file_bkp = r'C:\Users\mta1.nv1.qccnslt\Documents\003023-Sepia\TOVERI Sepia Control_QC_V1_bkp.xlsm'
    shutil.copyfile(target_file, target_file_bkp)
    target_sheet_name = 'Node QC'
    target_sheet_columns = ['PX Geo QC Codes ','PxGeo QC Data Code','Node Segregated','Fault','PxGeo Comments']

    target_data = pd.read_excel(target_file, sheet_name=target_sheet_name)

    target_data[target_sheet_columns] = source_data_subset.values
    print(target_data)
    with pd.ExcelWriter(target_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        target_data.to_excel(writer, sheet_name=target_sheet_name, index=False)
        



