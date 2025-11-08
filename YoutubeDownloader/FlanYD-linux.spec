# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_all, collect_submodules, collect_data_files

# Define the ffmpeg variable based on the operating system
if sys.platform == 'win32':
    ffmpeg = 'ffmpeg.exe'
    ffprobe = 'ffprobe.exe'
else:
    ffmpeg = 'ffmpeg'
    ffprobe = 'ffprobe'

block_cipher = None

# Collect all PyQt6 dependencies
datas = []
binaries = []
hiddenimports = []

# Collect PyQt6
tmp_ret = collect_all('PyQt6')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# Collect yt-dlp
tmp_ret = collect_all('yt_dlp')
datas += tmp_ret[0]
binaries += tmp_ret[1] 
hiddenimports += tmp_ret[2]

# Add additional hidden imports for completeness
hiddenimports += [
    'PyQt6.sip',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'yt_dlp.compat._legacy',
    'yt_dlp.compat._deprecated',
    'yt_dlp.utils._legacy',
    'yt_dlp.utils._deprecated',
    'certifi',
    'brotli',
    'mutagen',
    'websockets',
    'Cryptodome',
]

# Add ffmpeg binaries
binaries += [(f'/app/ffmpeg/{ffmpeg}', '.'), (f'/app/ffmpeg/{ffprobe}', '.')]

# Add branding assets
datas += [('FlanYDLogo.png', '.'), ('FlanYDLogo.ico', '.')]

a = Analysis(['youtube_downloader_ui.py'],
             pathex=[],
             binaries=binaries,
             datas=datas,
             hiddenimports=hiddenimports,
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='FlanYD',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='FlanYDLogo.ico' if sys.platform == 'win32' else 'FlanYDLogo.png',
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None)