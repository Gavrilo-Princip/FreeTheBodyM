#!/usr/bin/env python3

#
#   This file is part of FreeTheBodyM/bm_gui
#   FreeTheBodyM/src/bm_gui/bm_gui.py
#
#
#   Load the mainapplication
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


import sys


from PyQt5.QtWidgets import QApplication
from src.gui.mainwindow import MainWindow


def main():
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
