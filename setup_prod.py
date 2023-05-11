# coding: utf-8

from cx_Freeze import setup, Executable

executables = [Executable('automed.py', targetName='automed.exe')]

excludes = ['logging', 'unittest', 'email', 'html', 'http', 'urllib', 'xml',
             'unicodedata', 'bz2', 'select'
             , 'tcl8'
,'tcl8.6'
,'test'
,'tk8.6'
,'tkinter'
]

includes = ['images']

#zip_include_packages = ['wx', 'pynput']
zip_include_packages = ['wx']



options = {
    'build_exe': {
        'include_msvcr': True,
    }
}

setup(name='Automedapp',
      version='1.0.0',
      description='Automed application',
      executables=executables,
      options=options)