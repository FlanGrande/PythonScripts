# -*- mode: python ; coding: utf-8 -*-

import sys

# Define the ffmpeg variable based on the operating system
if sys.platform == 'win32':
    ffmpeg = 'ffmpeg.exe'
    ffprobe = 'ffprobe.exe'
else:
    ffmpeg = 'ffmpeg'
    ffprobe = 'ffprobe'

block_cipher = None



a = Analysis(['youtube_downloader_ui.py'],
             pathex=[],
             binaries=[(f'/app/ffmpeg/{ffmpeg}', '.'), (f'/app/ffmpeg/{ffprobe}', '.')],
             datas=[('FlanYDLogo.png', '.'), ('FlanYDLogo.ico', '.')],
             hiddenimports=[],
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
          icon='FlanYDLogo.ico',
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None)
