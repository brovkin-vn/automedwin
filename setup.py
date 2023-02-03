# coding: utf-8

from cx_Freeze import setup, Executable

executables = [Executable('testwx.py', targetName='start.exe')]

excludes = ['logging', 'unittest', 'email', 'html', 'http', 'urllib', 'xml',
            'unicodedata', 'bz2', 'select']

#zip_include_packages = ['wx']

options = {
    'build_exe': {
        'include_msvcr': True,
    }
}

setup(name='hello_world',
      version='0.0.2',
      description='My Hello World App!',
      executables=executables,
      options=options)