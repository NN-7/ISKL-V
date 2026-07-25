import os
import PyInstaller.__main__

# For each wanted EXE file make an array, with the first value being an array the path to the script, and its wanted name.
# Any following values are data to added to the EXE. Data should be structured in a subarray as well. [path, directory in the exe data] example: ['.../resources/file.txt', 'data/info']
# If you want an entire folder, you can do ['../resources/folder', 'data/folder'], and all the folder's content will be in data/folder.
# If you don't need any data bundled into the EXE, just put a string containing a path to the script in exes.
# Put each EXE array/path string in the exes array.

starter = [['starter.py', 'starter'], ['resources\\WindowsGeneralManager.xml', 'data'], ['resources\\WinSE.cmd', 'data']]
boot_animation = [['virus-scripts\\boot_animation.py', 'boot_animation'],
                  ['resources\\Windows-Boot-Animation-Frames', 'data\\frames']]
#exes = [starter, boot_animation]
exes = [boot_animation]

def prepare_datas(exe):
    added_files = ''
    for data_info in exe[1:]:
        added_files += f"(r'{data_info[0]}',r'{data_info[1]}'),"
    added_files = added_files[:-1]  # remove the extra comma from added_files
    return added_files

def make_spec_file(exe, added_files):
    with open('instructions.spec', 'w') as file:
        file.write(f'''# -*- mode: python ; coding: utf-8 -*-
added_files = [{added_files}]
a = Analysis(
    [r"{exe[0][0]}"],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,     # <--- Add this line
    a.zipfiles,     # <--- Add this line
    a.datas,        # <--- Add this line
    name='{exe[0][1]}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)''')

def make_exe():
    PyInstaller.__main__.run([
        'instructions.spec'
    ])

for exe in exes:
    added_files = prepare_datas(exe)
    make_spec_file(exe, added_files)
    make_exe()
    os.remove('instructions.spec')



