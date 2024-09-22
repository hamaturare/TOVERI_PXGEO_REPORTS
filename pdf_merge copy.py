import PyPDF2
import tkinter as tk
from tkinter import filedialog

# Create the root window and hide it (we just want the file dialog)
root = tk.Tk()
root.withdraw()

# Ask the user to select the first PDF file
file_path1 = filedialog.askopenfilename(title=r'C:\Users\mta1.nv1.qccnslt\Desktop\TEMPLATE_PDF01.pdf', filetypes=[('PDF Files', '*.pdf')])
if not file_path1:
    print("No file selected. Exiting.")
    exit()

# Ask the user to select the second PDF file
file_path2 = filedialog.askopenfilename(title=r'C:\Users\mta1.nv1.qccnslt\Desktop\TESTE PAGE ADDED.pdf', filetypes=[('PDF Files', '*.pdf')])
if not file_path2:
    print("No file selected. Exiting.")
    exit()

# Ask the user to select the output file path
output_path = filedialog.asksaveasfilename(title=r'C:\Users\mta1.nv1.qccnslt\Desktop\Merged_pdef.pdf', defaultextension=".pdf", filetypes=[('PDF Files', '*.pdf')])
if not output_path:
    print("No output path selected. Exiting.")
    exit()

# Open the selected files in binary read mode
with open(file_path1, 'rb') as file1, open(file_path2, 'rb') as file2:
    # Create PDF reader objects
    reader1 = PyPDF2.PdfReader(file1)
    reader2 = PyPDF2.PdfReader(file2)
    
    # Create a PDF writer object
    writer = PyPDF2.PdfWriter()
    
    # Add pages from the first PDF
    for pageNum in range(len(reader1.numPages)):
        page = reader1.getPage(pageNum)
        writer.addPage(page)
    
    # Add pages from the second PDF
    for pageNum in range(len(reader2.numPages)):
        page = reader2.getPage(pageNum)
        writer.addPage(page)
    
    # Write the merged PDF to the new file
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

print("PDFs Merged Successfully.")
