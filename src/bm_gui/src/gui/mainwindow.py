#
#   This file is part of FreeTheBodyM/bm_gui
#   FreeTheBodyM/src/bm_gui/src/gui/mainwindow.py
#
#
#   This module contains the functions for the gui
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


import time
import datetime
import serial
import serial.tools.list_ports as tools
import os

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

from src.gui.ui.window_ui import Ui_MainWindow

import src.file_op

class MainWindow(QMainWindow):

    #
    #
    #
    def __init__(self):
        QMainWindow.__init__(self)

        self.__lang = 'german'
        self.conf_file = None
        file_exist = False
        try:
            #   first i wanted to name the conf-file like EvilShit.exe/Trojan.exe/Backdoor.exe
            #   and add the the real config as ADS. But i think windows users will
            #   not laughing like me about this easter-egg :-/
            self.conf_file = open('./conf.cfg', mode='r', encoding='utf-8')
            file_exist = True
        except:
            pass

        self.Foo = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ##################################################
        #   prefill comboboxes
        #   sex
        self.ui.cbSex.addItem('Frau')
        self.ui.cbSex.addItem('Mann')

        #   hand
        self.ui.cbHand.addItem('links')
        self.ui.cbHand.addItem('rechts')

        #   smoker
        self.ui.cbSmoker.addItem('nein')
        self.ui.cbSmoker.addItem('ja')

        #   Age
        for i in range(18, 101, 1):
            self.ui.cbAge.addItem(str(i))
        else:
            self.ui.cbAge.setMaxVisibleItems(20)

        #   Weight
        for i in range(20, 301, 1):
            self.ui.cbWeight.addItem(str(i))
        else:
            self.ui.cbWeight.setMaxVisibleItems(20)

        #   Height
        for i in range(70, 251, 1):
            self.ui.cbHeight.addItem(str(i))
        else:
            self.ui.cbHeight.setMaxVisibleItems(20)

        #   ee-Target
        for i in range(1500, 8001, 50):
            self.ui.cbEeTarget.addItem(str(i))
        else:
            self.ui.cbEeTarget.setMaxVisibleItems(20)

        #   step-Target
        for i in range(500, 30001, 50):
            self.ui.cbStepTarget.addItem(str(i))
        else:
            self.ui.cbStepTarget.setMaxVisibleItems(20)

        #   birthdate day
        for i in range(1, 32, 1):
            self.ui.cbBDayDay.addItem(str(i))
        else:
            self.ui.cbBDayDay.setMaxVisibleItems(31)

        #   birthday month
        for i in range(1, 13, 1):
            self.ui.cbBDayMonth.addItem(str(i))
        else:
            self.ui.cbBDayMonth.setMaxVisibleItems(12)

        #   birthday year
        for i in range(1940, 2015, 1):
            self.ui.cbBDayYear.addItem(str(i))
        else:
            self.ui.cbBDayYear.setMaxVisibleItems(20)
        #
        ##################################################

        if file_exist:
            r = self.conf_file.read()
            self.conf_file.close()
            data = r.replace(' ', '').split('\n')
            for line in data:
                line = line.split('=')
                if line[0] == 'sex':
                    if self.__lang == 'german':
                        if line[1] == 'female':
                            self.ui.cbSex.setCurrentText('Frau')
                        else:
                            self.ui.cbSex.setCurrentText('Mann')
                    else:
                        if line[1] == 'female':
                            self.ui.cbSex.setCurrentText('female')
                        else:
                            self.ui.cbSex.setCurrentText('male')

                elif line[0] == 'hand':
                     if self.__lang == 'german':
                        if line[1] == 'left':
                            self.ui.cbHand.setCurrentText('links')
                        else:
                            self.ui.cbHand.setCurrentText('rechts')
                     else:
                        if line[1] == 'left':
                            self.ui.cbHand.setCurrentText('left')
                        else:
                            self.ui.cbHand.setCurrentText('right')

                elif line[0] == 'smoker':
                    if self.__lang == 'german':
                        if line[1] == 'false':
                            self.ui.cbSmoker.setCurrentText('nein')
                        else:
                            self.ui.cbSmoker.setCurrentText('ja')
                    else:
                        if line[1] == 'false':
                            self.ui.cbSmoker.setCurrentText('no')
                        else:
                            self.ui.cbSmoker.setCurrentText('yes')

                elif line[0] == 'age':
                    self.ui.cbAge.setCurrentText(line[1])

                elif line[0] == 'weight':
                    self.ui.cbWeight.setCurrentText(line[1])

                elif line[0] == 'height':
                    self.ui.cbHeight.setCurrentText(line[1])

                elif line[0] == 'cals':
                    self.ui.cbEeTarget.setCurrentText(line[1])

                elif line[0] == 'steps':
                    self.ui.cbStepTarget.setCurrentText(line[1])

                elif line[0] == 'day':
                    self.ui.cbBDayDay.setCurrentText(line[1])

                elif line[0] == 'month':
                    self.ui.cbBDayMonth.setCurrentText(line[1])

                elif line[0] == 'year':
                    self.ui.cbBDayYear.setCurrentText(line[1])

                else:
                    pass

        self.Seek()

    #
    #
    #
    def Proc_Start(self):
        ts = int(time.time())
        year = datetime.datetime.fromtimestamp(ts).strftime('%d_%m_%Y')
        date = datetime.datetime.fromtimestamp(ts).strftime('%H_%M_%S')

        if self.__lang == 'german':
            p = '.\\data\\Ausgelesen_am_%s_um_%s.csv' % (year, date)
            x = '.\\data\\Ausgelesen_am_%s_um_%s.xml' % (year, date)
            s = '.\\data\\Ausgelesen_am_%s_um_%s.swd' % (year, date)
        else:
            p = '.\\data\\Read_at_%s_at_%s.csv' % (year, date)
            x = '.\\data\\Read_at_%s_at_%s.xml' % (year, date)
            s = '.\\data\\Read_at_%s_at_%s.swd' % (year, date)

        c = '%s --fromSerial=%s --toCsv=%s' % (self.BmHackPath, self.Port[0], p)

        if self.ui.cbClear.isChecked():
            c += ' --clear'

        os.system(c)

        if self.ui.cbSex.currentText() == 'Frau' or self.ui.cbSex.currentText() == 'female':
            sex = 'female'
        else:
            sex = 'male'

        if self.ui.cbHand.currentText() == 'links' or self.ui.cbHand.currentText() == 'left':
            hand = 'left'
        else:
            hand = 'right'

        if self.ui.cbSmoker.currentText() == 'nein' or self.ui.cbSmoker.currentText() == 'no':
            smoker = 'false'
        else:
            smoker = 'true'

        age     = self.ui.cbAge.currentText()
        w       = int(self.ui.cbWeight.currentText())
        h       = int(self.ui.cbHeight.currentText())
        ee      = self.ui.cbEeTarget.currentText()
        steps   = self.ui.cbStepTarget.currentText()
        day     = self.ui.cbBDayDay.currentText()
        month   = self.ui.cbBDayMonth.currentText()
        year    = self.ui.cbBDayYear.currentText()

        try:
            self.Foo = src.file_op.FileOp(p, x, s, [hand, w, h, sex, age, smoker, ee, steps, day, month, year])
            self.Foo.Run()
        except:
            if self.__lang == 'german':
                print('\n\nKonnte CSV-Datei nicht oeffnen...\n\n')
            else:
                print('\n\nCould not open CSV-File...\n\n')

    #
    #
    #
    def ClearOnly(self):
        c = '%s --fromSerial=%s --clear' % (self.BmHackPath, self.Port[0])
        os.system(c)

    #
    #
    #
    def Proc_End(self):
        self.close()

    #
    #
    #
    def SafeBody(self):
        self.conf_file = open('./conf.cfg', mode='w', encoding='utf-8')

        if self.ui.cbSex.currentText() == 'Frau' or self.ui.cbSex.currentText() == 'female':
            self.conf_file.write('sex=female\n')
        else:
            self.conf_file.write('sex=male\n')

        if self.ui.cbHand.currentText() == 'links' or self.ui.cbHand.currentText() == 'left':
            self.conf_file.write('hand=left\n')
        else:
            self.conf_file.write('hand=right\n')

        if self.ui.cbSmoker.currentText() == 'nein' or self.ui.cbSmoker.currentText() == 'no':
            self.conf_file.write('smoker=false\n')
        else:
            self.conf_file.write('smoker=true\n')

        self.conf_file.write('age=%s\n' %       (self.ui.cbAge.currentText()))
        self.conf_file.write('weight=%s\n' %    (self.ui.cbWeight.currentText()))
        self.conf_file.write('height=%s\n' %    (self.ui.cbHeight.currentText()))
        self.conf_file.write('cals=%s\n' %      (self.ui.cbEeTarget.currentText()))
        self.conf_file.write('steps=%s\n' %     (self.ui.cbStepTarget.currentText()))
        self.conf_file.write('day=%s\n' %       (self.ui.cbBDayDay.currentText()))
        self.conf_file.write('month=%s\n' %     (self.ui.cbBDayMonth.currentText()))
        self.conf_file.write('year=%s\n' %      (self.ui.cbBDayYear.currentText()))

        self.conf_file.close()

    #
    #
    #
    def Seek(self):
        self.Port = self.FindBodymedia()

        self.ui.cbClear.setEnabled(False)
        self.ui.btnStart.setEnabled(False)
        self.ui.btnClearOnly.setEnabled(False)

        if self.Port == False:
            if self.__lang == 'german':
                self.ui.lbShow.setText('BodyMedia nicht gefunden')
            else:
                self.ui.lbShow.setText('BodyMedia not found')
        else:
            self.ui.lbShow.setText(self.Port[1])
            self.ui.btnStart.setEnabled(True)
            self.ui.cbClear.setEnabled(True)
            self.ui.btnClearOnly.setEnabled(True)
            self.BmHackPath = '.\\bin\\Windows\\bm_hack\\bm_hack.exe'

    #
    #
    #
    def FindBodymedia(self):
        com_ports = tools.comports()
        for port in com_ports:
            if 'BodyMedia' in port[1]:
                return port
        else:
            return False

    #
    #
    #
    def SwitchLanguage(self):
        if self.__lang == 'german':
            self.__lang = 'english'

            #   group boxes
            self.ui.gbBodyData.setTitle('Bodydata')
            self.ui.gbBDay.setTitle('Birthday and Age')
            self.ui.gbHeightWeight.setTitle('Height and Weight')
            self.ui.gbTargets.setTitle('Targets')
            self.ui.gbOthers.setTitle('Others')

            #   labels
            self.ui.lbBirthday.setText('Birthdate:')
            self.ui.lbDay.setText('Day')
            self.ui.lbMonth.setText('Month')
            self.ui.lbYear.setText('Year')
            self.ui.lbAge.setText('Age:')
            self.ui.lbHeight.setText('Height in cm:')
            self.ui.lbWeight.setText('Weight in kg:')
            self.ui.lbKCal.setText('Calories:')
            self.ui.lbSteps.setText('Steps:')
            self.ui.lbSex.setText('Sex:')
            self.ui.lbHand.setText('Handedness:')
            self.ui.lbSmoker.setText('Smoker:')
            #self.ui.lbShow.setText('')

            #   checkboxes
            self.ui.cbClear.setText('Delete device memory after reading')

            #   buttons
            self.ui.btnSafeBody.setText('Safe Bodydata\nin local file')
            self.ui.btnSeek.setText('Armband not\nfound?\nSeek again')
            self.ui.btnStart.setText('Read\nBodyMedia')
            self.ui.btnClearOnly.setText('Clear BodyMedia\nWITHOUT reading')
            self.ui.btnClose.setText('Close')

            #   comboboxes
            #   Sex
            s = self.ui.cbSex.currentText()
            self.ui.cbSex.removeItem(1)
            self.ui.cbSex.removeItem(0)
            self.ui.cbSex.addItem('female')
            self.ui.cbSex.addItem('male')

            if s == 'Frau':
                self.ui.cbSex.setCurrentText('female')
            else:
                self.ui.cbSex.setCurrentText('male')

            #   hand
            h = self.ui.cbHand.currentText()
            self.ui.cbHand.removeItem(1)
            self.ui.cbHand.removeItem(0)
            self.ui.cbHand.addItem('left')
            self.ui.cbHand.addItem('right')

            if h == 'links':
                self.ui.cbHand.setCurrentText('left')
            else:
                self.ui.cbHand.setCurrentText('right')

            #   smoker
            s = self.ui.cbSmoker.currentText()
            self.ui.cbSmoker.removeItem(1)
            self.ui.cbSmoker.removeItem(0)
            self.ui.cbSmoker.addItem('no')
            self.ui.cbSmoker.addItem('yes')

            if s == 'nein':
                self.ui.cbSmoker.setCurrentText('no')
            else:
                self.ui.cbSmoker.setCurrentText('yes')


        else:
            self.__lang = 'german'

            #   group boxes
            self.ui.gbBodyData.setTitle('Koerperdaten')
            self.ui.gbBDay.setTitle('Geburtstag und Alter')
            self.ui.gbHeightWeight.setTitle('Groesse und Gewicht')
            self.ui.gbTargets.setTitle('Ziele')
            self.ui.gbOthers.setTitle('Sonstiges')

            #   labels
            self.ui.lbBirthday.setText('Geburtstag:')
            self.ui.lbDay.setText('Tag')
            self.ui.lbMonth.setText('Monat')
            self.ui.lbYear.setText('Jahr')
            self.ui.lbAge.setText('Alter:')
            self.ui.lbHeight.setText('Groesse in cm:')
            self.ui.lbWeight.setText('Gewicht in kg:')
            self.ui.lbKCal.setText('Kalorien:')
            self.ui.lbSteps.setText('Schritte:')
            self.ui.lbSex.setText('Geschlecht:')
            self.ui.lbHand.setText('Haender:')
            self.ui.lbSmoker.setText('Raucher:')
            #self.ui.lbShow.setText('')

            #   checkboxes
            self.ui.cbClear.setText('Speicher nach dem Auslesen loeschen')

            #   buttons
            self.ui.btnSafeBody.setText('Koerperdaten\nlokal speichern')
            self.ui.btnSeek.setText('Armband nicht\ngefunden?\nErneut Suchen')
            self.ui.btnStart.setText('BodyMedia\nauslesen')
            self.ui.btnClearOnly.setText('BodyMedia loeschen,\nOHNE auslesen!')
            self.ui.btnClose.setText('Beenden')

            #   comboboxes
            #   Sex
            s = self.ui.cbSex.currentText()
            self.ui.cbSex.removeItem(1)
            self.ui.cbSex.removeItem(0)
            self.ui.cbSex.addItem('Frau')
            self.ui.cbSex.addItem('Mann')

            if s == 'female':
                self.ui.cbSex.setCurrentText('Frau')
            else:
                self.ui.cbSex.setCurrentText('Mann')

            #   hand
            h = self.ui.cbHand.currentText()
            self.ui.cbHand.removeItem(1)
            self.ui.cbHand.removeItem(0)
            self.ui.cbHand.addItem('links')
            self.ui.cbHand.addItem('rechts')

            if h == 'left':
                self.ui.cbHand.setCurrentText('links')
            else:
                self.ui.cbHand.setCurrentText('rechts')

            #   smoker
            s = self.ui.cbSmoker.currentText()
            self.ui.cbSmoker.removeItem(1)
            self.ui.cbSmoker.removeItem(0)
            self.ui.cbSmoker.addItem('nein')
            self.ui.cbSmoker.addItem('ja')

            if s == 'no':
                self.ui.cbSmoker.setCurrentText('nein')
            else:
                self.ui.cbSmoker.setCurrentText('ja')

        self.Seek()
