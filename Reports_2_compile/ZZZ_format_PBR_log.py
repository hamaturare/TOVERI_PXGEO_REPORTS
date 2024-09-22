import pandas as pd
import shutil

#Qc Sheets Pxgeo Path
folder_path =r'C:\Users\mta1.nv1.qccnslt\Desktop\PBR_Production\\' 


#Copy Node Stats to local folder and convert to .xlsx
read_file = pd.read_csv(Node_stats)
read_file.to_excel(Node_stats_copy, index=False, header=True, sheet_name='Nodes_Stats')

#reading QC Table from Pxgeo to use in QGIS
df = pd.read_excel(qc_table, skiprows=4, index_col=None, na_values=['NA'], usecols="A,B,D,N,O,R,S,T,U,AL,AM")
df.rename(columns = {'RPS\nRecov\nX' : 'Recovery X', 'RPS\nRecov\nY' : 'Recovery Y', 'Recalc\nX' : 'Seismic X', 'Recalc\nY' : 'Seismic Y' }, inplace=True )
CSV_QC_TABLE = r'C:\Users\mta1.nv1.qccnslt\Documents\001522-Aram\QC\0256_3D_ARAM_QC_node_2export.csv'
df.to_csv(CSV_QC_TABLE, index=False)




