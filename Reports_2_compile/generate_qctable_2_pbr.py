import pandas as pd
import shutil

#Qc Sheets Pxgeo Path
qc_table =r'C:\Users\mta1.nv1.qccnslt\Documents\001522-Aram\TOVERI ARAM QC Control.xlsm'

#Path to backup
qc_table_bkp = r'C:\Users\mta1.nv1.qccnslt\Documents\001522-Aram\TOVERI ARAM QC Control_bkp.xlsm'

#Path qc table to PBR
qc_table_pbr = r'C:\Users\mta1.nv1.qccnslt\Desktop\NodeQC_Toveri.xlsm'

#Copy Qc Sheets to local folder.
shutil.copyfile(qc_table, qc_table_bkp)

#reading QC Table from Pxgeo to use in QGIS
df = pd.read_excel(qc_table_bkp, index_col=None, na_values=['NA'], sheet_name='Node QC', usecols="A:Z")

#Path of PBR qc_table
qc_table_pbr = r'C:\Users\mta1.nv1.qccnslt\Desktop\NodeQC_Toveri.xlsx'

#Write qc table to PBR
df.to_excel(qc_table_pbr, index=False, sheet_name='Node QC')
