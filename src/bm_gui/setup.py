#!/usr/bin/env python

#
#   This file is part of FreeTheBodyM/bm_gui
#   FreeTheBodyM/src/bm_gui/setup.py
#
#
#   This is the setup module and build the windows binary
#
#   Copyright (C) 2015  Bloody_Wulf
#   Contact: bloody_wulf@mailbox.org
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA,
#   or look here: http://www.gnu.org/licenses/gpl.html
#


import os
import shutil
from cx_Freeze import setup, Executable

if __name__ == '__main__':
    if os.path.exists('./__pycache__'):
        shutil.rmtree('./__pycache__')

    if os.path.exists('./build'):
        shutil.rmtree('./build')

    setup(
        #executables=[Executable('./bm_gui.py', base='Win32GUI')]
        executables=[Executable('./bm_gui.py')]
    )

    if os.path.exists('./../../bin/Windows/bm_gui'):
        shutil.rmtree('./../../bin/Windows/bm_gui')

    # Windows 32bit
    shutil.copytree('./build/exe.win32-3.4', './../../bin/Windows/bm_gui')

    shutil.rmtree('./build')
