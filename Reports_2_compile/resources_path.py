import os
import sys

def get_resource_path(filename):
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        application_path = os.path.join(application_path, 'QC Reports GEN')
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
   
    return os.path.join(application_path, filename)

favicon_path = get_resource_path('Icons\\python-32.ico')
favicon2_path = get_resource_path('Icons\\python-32.ico')
logo_path = get_resource_path('Logo\\ToveriLogoNoBg.png')