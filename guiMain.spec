# -*- mode: python -*-

block_cipher = None


a = Analysis(['guiMain.py', 'design.py', 'ItemsHeldModule.py', 'ItemInfoModule.py', 'ShippingInfoModule.py', 'genericDialog.py', 'dialogModule.py'],
             pathex=['/home/suhussai/ebayApp'],
             binaries=None,
             datas=[("*.json", ".")],
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
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='guiMain',
          debug=False,
          strip=False,
          upx=True,
          console=True )
