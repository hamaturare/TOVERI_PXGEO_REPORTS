import pandas as pd
import shutil

#Qc Sheets Pxgeo Path
qc_table =r'C:\Users\mta1.nv1.qccnslt\Documents\003023-Sepia\TOVERI Sepia Control_QC_V1.xlsm'

#Path to backup
qc_table_bkp = r'C:\Users\mta1.nv1.qccnslt\Documents\003023-Sepia\TOVERI Sepia Control_QC_bkp_V1.xlsm'

#Path qc table to PBR
qc_table_pbr = r'C:\Users\mta1.nv1.qccnslt\Desktop\NodeQC_Toveri_Sepia.xlsm'

#Copy Qc Sheets to local folder.
shutil.copyfile(qc_table, qc_table_bkp)

#reading QC Table from Pxgeo to use in QGIS
df = pd.read_excel(qc_table_bkp, index_col=None, na_values=['NA'], sheet_name='Node QC', usecols="A:T,W:X,AA:AB")

#Path of PBR qc_table
qc_table_pbr = r'C:\Users\mta1.nv1.qccnslt\Desktop\NodeQC_Toveri_Sepia.xlsx'

#Write qc table to PBR
df.to_excel(qc_table_pbr, index=False, sheet_name='Node QC')
