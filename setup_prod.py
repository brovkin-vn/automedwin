# coding: utf-8

from cx_Freeze import setup, Executable

executables = [Executable('automed.py', targetName='automed.exe')]

excludes = ['logging', 'unittest', 'email', 'html', 'http', 'urllib', 'xml',
             'unicodedata', 'bz2', 'select']

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