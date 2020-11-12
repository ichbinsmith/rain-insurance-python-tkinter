#build exe: python setup.py build
#build installer msi : python setup.py bdist_msi

from cx_Freeze import setup, Executable
import os

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "RDH",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]rainyDaysHero.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None, # Icon
     0,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]


# Now create the table dictionary
msi_data = dict(Shortcut = shortcut_table)

# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = dict(data = msi_data)
  
executables = [
        Executable(script = "rainyDaysHero.py",icon = os.path.dirname(os.path.realpath(__file__))+"\\img\\rdh.ico", base = "Win32GUI")
]
  
buildOptions = dict( 
        includes = ["pandas","math","tkinter","tkcalendar","PIL","os","requests","fpdf","matplotlib"],
        include_files = [os.path.dirname(os.path.realpath(__file__))+"\\img\\",os.path.dirname(os.path.realpath(__file__))+"\\data\\"]
)
  
setup(
    name = "RDH",
    version = "1.0",
    description = "Rainy Days Hero - Rain Insurance App",
    author = "Smith Djamoura",
    options = dict(build_exe = buildOptions, bdist_msi=bdist_msi_options),
    executables = executables
)