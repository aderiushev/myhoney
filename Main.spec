# -*- mode: python -*-

from kivy.deps import sdl2, glew

block_cipher = None


a = Analysis(['Main.py'],
             pathex=['Z:\\home\\aleksei\\my\\myhoney'],
             binaries=None,
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
            Tree('images', prefix='images'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          a.binaries,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='Honey',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='/home/aleksei/my/myhoney/images/system/favicon.ico')
