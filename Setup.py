import cx_Freeze

executables = [cx_Freeze.Executable('C:\\Users\\jwhitten\\PycharmProjects\\Top Down Racing\\Main.py')]

cx_Freeze.setup(
    name='A bit Racey',
    options={'build_exe': {'packages': ['pygame'],
                           'include_files': ['C:\\Users\\jwhitten\\Documents\\Python\\Top Down Racing\\sonic.png']}},
    executables=executables
)
