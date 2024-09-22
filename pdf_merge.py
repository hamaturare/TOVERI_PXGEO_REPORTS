# Import PyPDF2
from PyPDF2 import PdfReader, PdfWriter

# Open the source and target PDF files
source = PdfReader(open(r'C:\Users\mta1.nv1.qccnslt\Desktop\TEMPLATE_PDF01.pdf', "rb"))
target = PdfReader(open(r'C:\Users\mta1.nv1.qccnslt\Desktop\TESTE PAGE ADDED.pdf', "rb"))

# Create a PdfFileWriter object
output = PdfWriter()

# Copy all the pages from the target file to the output file
for i in range(len(target.numPages)):
    output.addPage(target.getPage(i))

# Append the last page from the source file to the output file
output.addPage(source.getPage(len(source.pages)-1))

# Write the output file to disk
with open(r'C:\Users\mta1.nv1.qccnslt\Desktop\Merged_pdef.pdf', "wb") as f:
    output.write(f)


