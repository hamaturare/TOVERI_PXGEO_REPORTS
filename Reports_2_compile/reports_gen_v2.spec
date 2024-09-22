# QC Reports GEN - Pre-Release.spec
# To compile this software cd to the directory of this file and run on the terminal the following comand:
# python -m PyInstaller reports_gen_v2.spec --nonconfirm
# Make sure that the name='QC Reports GEN' on lines 41 and 55 on the code below are the same 
# and also the same and also have name that you have on the config_path.py file (check the config_path file to uncoment or comment stuff before compiling this .spec file)
# Make sure all the paths for the config.ini and the logos and icons are correct as well.
# If you are using pyinstaller==5.9.0 your Config and other folders will be set under the QC Reports GEN which is correct.
# If you are using pyinstaller==6.10.0 yor Config and other folders will be put inside the _internal folder, which does not allow the application to Run so, just copy all the folders to the QC Reports GEN which is correct.

import os
import sys
#import path # uncoment if using pyinstaller==5.9.0
from PyInstaller.building.api import EXE, COLLECT
from PyInstaller.building.build_main import Analysis
spec_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
venv_path = os.path.join(spec_dir, 'venv', 'Lib', 'site-packages')
sys.path.append(venv_path)


block_cipher = None

a = Analysis(['__init__.py'],
             pathex=['C:\\Users\\mta1.nv1.qccnslt\\Documents\\python\\Pxgeo\\Reports_2_compile'],
             binaries=[],
             datas=[('C:\\Users\\mta1.nv1.qccnslt\\Documents\\python\\Pxgeo\\Reports_2_compile\\Config\\config.ini', 'Config'),
                ('C:\\Users\\mta1.nv1.qccnslt\\Documents\\python\\Pxgeo\\Reports_2_compile\\Icons\\python-16_blue.ico', 'Icons'), 
                ('C:\\Users\\mta1.nv1.qccnslt\\Documents\\python\\Pxgeo\\Reports_2_compile\\Icons\\python-16_green.ico', 'Icons'),
				('C:\\Users\\mta1.nv1.qccnslt\\Documents\\python\\Pxgeo\\Reports_2_compile\\Icons\\python-16_redblack.ico', 'Icons'),
				('C:\\Users\\mta1.nv1.qccnslt\\Documents\\python\\Pxgeo\\Reports_2_compile\\Icons\\python-32.ico', 'Icons'),
                ('C:\\Users\\mta1.nv1.qccnslt\\Documents\\python\\Pxgeo\\Reports_2_compile\\Logo\\ToveriLogoNoBg.png', 'Logo')],   
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='QC Reports GEN',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='C:\\Users\\mta1.nv1.qccnslt\\Documents\\python\\Pxgeo\\Reports_2_compile\\Icons\\python-multi-size.ico'
)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='QC Reports GEN')


