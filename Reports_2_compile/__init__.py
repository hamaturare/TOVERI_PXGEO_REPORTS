#!/usr/bin/env python
from main import Main

if __name__ == "__main__":
   try:
      
      Main()

   except Exception as e:  # Handle any exception and assign it to variable e
               # Log the error to a file for debugging
               with open('error_log.txt', 'a') as log_file:
                  log_file.write(f"Error: {e}\n")  # Use f-string for Python 3.6+
               print("ERROR", f"ERROR - {e}")