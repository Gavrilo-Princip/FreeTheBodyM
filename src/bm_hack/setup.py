#!/usr/bin/env python

import os
import shutil
from cx_Freeze import setup, Executable

if __name__ == '__main__':
    if os.path.exists('.\\__pycache__'):
        shutil.rmtree('.\\__pycache__')

    if os.path.exists('.\\build'):
        shutil.rmtree('.\\build')

    setup(
        executables=[Executable('.\\bm_hack.py')]
    )

    if os.path.exists('.\\..\\..\\bin\\Windows\\bm_hack'):
        shutil.rmtree('.\\..\\..\\bin\\Windows\\bm_hack')

    # Windows 32bit
    shutil.copytree('.\\build\\exe.win32-2.7', '.\\..\\..\\bin\\Windows\\bm_hack')

    shutil.rmtree('.\\build')
