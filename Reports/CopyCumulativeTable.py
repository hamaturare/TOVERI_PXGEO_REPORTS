import shutil
import os

class CopyCumulativeTable:
   
    def __init__ (self, source_path, destination_path):
        self.source_path = source_path
        self.destination_path = destination_path

    def copy_table(self):
        #copy table
        shutil.copyfile(self.source_path, self.destination_path)

    def is_updated(self):
        # Get the modification times of the source and destination files
        source_mtime = os.path.getmtime(self.source_path)
        destination_mtime = os.path.getmtime(self.destination_path)
        
        # Check if the source file has been updated more recently than the destination file
        return source_mtime > destination_mtime    