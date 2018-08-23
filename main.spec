# -*- mode: python -*-

from  kivy.tools.packaging.pyinstaller_hooks import get_deps_all, hookspath, runtime_hooks

block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\\tmp\\desktopapp'],
             binaries = [ ( 'D:\\bin\\api-ms-win-downlevel-shlwapi-l1-1-0.dll', '.' ) ],
             datas=[],
             #hiddenimports=None,
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False,
             **get_deps_all())
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
