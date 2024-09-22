# QC Reports GEN - Pre-Release.spec
# To compile this software cd to the directory of this file and run on the terminal the following comand:
# python -m PyInstaller reports_gen.spec
# Make sure that the name='QC Reports GEN' on lines 41 and 55 on the code below are the same 
# and also the same and also have name that you have on the config_path.py file
# Make sure all the paths for the config.ini and the logos and icons are correct as well.

import os
import sys
import path
from PyInstaller.building.api import EXE, COLLECT
from PyInstaller.building.build_main import Analysis


block_cipher = None

a = Analysis(['__init__.py'],
             pathex=['C:\\Users\\mta1.nv1.qccnslt\\Documents\\python\\Pxgeo\\Reports'],
             binaries=[],
             datas=[('C:\\Users\\mta1.nv1.qccnslt\\Documents\\python\\Pxgeo\\Reports\\Config\\config.ini', 'Config'),
                ('C:\\Users\\mta1.nv1.qccnslt\\Documents\\python\\Pxgeo\\Reports\\Icons\\python-16_blue.ico', 'Icons'), 
                ('C:\\Users\\mta1.nv1.qccnslt\\Documents\\python\\Pxgeo\\Reports\\Icons\\python-16_green.ico', 'Icons'),
				('C:\\Users\\mta1.nv1.qccnslt\\Documents\\python\\Pxgeo\\Reports\\Icons\\python-16_redblack.ico', 'Icons'),
				('C:\\Users\\mta1.nv1.qccnslt\\Documents\\python\\Pxgeo\\Reports\\Icons\\python-32.ico', 'Icons'),
                ('C:\\Users\\mta1.nv1.qccnslt\\Documents\\python\\Pxgeo\\Reports\\Logo\\ToveriLogoNoBg.png', 'Logo')],   
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
          icon='C:\\Users\\mta1.nv1.qccnslt\\Documents\\python\\Pxgeo\\Reports\\Icons\\python-multi-size.ico'
)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='QC Reports GEN')


