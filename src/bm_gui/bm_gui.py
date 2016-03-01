#!/usr/bin/env python

#
# January 2016 by Bloody_Wulf	bloody_wulf@mailbox.org
#
# THIS CODE IS DECLARED BY THE AUTHOR TO BE IN THE PUBLIC DOMAIN.
# NO WARRANTY OF ANY KIND IS PROVIDED.
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
  s ='''

THIS CODE IS DECLARED BY THE AUTHOR TO BE IN THE PUBLIC DOMAIN.
NO WARRANTY OF ANY KIND IS PROVIDED.

'''
  print(s)
  main()
