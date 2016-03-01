#!/usr/bin/env python

#
# January 2016 by Bloody_Wulf	bloody_wulf@mailbox.org
#
# THIS CODE IS DECLARED BY THE AUTHOR TO BE IN THE PUBLIC DOMAIN.
# NO WARRANTY OF ANY KIND IS PROVIDED.
#


import time
import datetime
import serial
import serial.tools.list_ports as tools
import struct
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

        self.__SerNum = 0

        self.__lang = 'german'
        self.conf_file = None
        file_exist = False
        try:
            self.conf_file = open('./conf.cfg', mode='r', encoding='utf-8')
            file_exist = True
        except:
            pass

        self.Foo = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        s = '''
    + BodyMeda aktivieren +
==================
Beim aktivieren werden alle aufgezeichneten Sensordaten auf dem Armband gelöscht!


+ Koerperdaten uebertragen +
==================
Beim uebertragen der Koerperdaten werden alle aufgezeichneten Sensordaten auf dem Armband gelöscht!'''

        self.ui.teHints.setReadOnly(False)
        self.ui.teHints.setPlainText(s)
        self.ui.teHints.setReadOnly(True)

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

        #   Weight
        for i in range(40, 251, 1):
            self.ui.cbWeight.addItem(str(i))
        else:
            self.ui.cbWeight.setMaxVisibleItems(20)

        #   Height
        for i in range(100, 221, 1):
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
        for i in range(1940, 1999, 1):
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

        w       = int(self.ui.cbWeight.currentText())
        h       = int(self.ui.cbHeight.currentText())
        ee      = self.ui.cbEeTarget.currentText()
        steps   = self.ui.cbStepTarget.currentText()
        day     = self.ui.cbBDayDay.currentText()
        month   = self.ui.cbBDayMonth.currentText()
        year    = self.ui.cbBDayYear.currentText()

        try:
            self.Foo = src.file_op.FileOp(p, x, s, [hand, w, h, sex, smoker, ee, steps, day, month, year])
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
        self.ui.btnBodyData.setEnabled(False)

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
            self.ui.btnBodyData.setEnabled(True)
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
            self.ui.gbBDay.setTitle('Birthday')
            self.ui.gbHeightWeight.setTitle('Height and Weight')
            self.ui.gbTargets.setTitle('Targets')
            self.ui.gbOthers.setTitle('Others')

            #   labels
            self.ui.lbBirthday.setText('Birthdate:')
            self.ui.lbDay.setText('Day')
            self.ui.lbMonth.setText('Month')
            self.ui.lbYear.setText('Year')
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
            self.ui.btnSeek.setText('Armband not\nfound?\nSeek again')
            self.ui.btnStart.setText('Read\nBodyMedia')
            self.ui.btnClearOnly.setText('Activate BodyMedia')
            self.ui.btnClose.setText('Close')
            self.ui.btnBodyData.setText('Write currently set Bodydata to the BodyMedia')

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

            s = '''
    + Activate BodyMedia +
==================
By activating the BodyMedia all current Sensordata will be deleted!


+ Write Bodydata +
==================
By writing your Bodydata to the BodyMedia all current Sensordata will be deleted!'''
            self.ui.teHints.setReadOnly(False)
            self.ui.groupBox_2.setTitle('Hints')
            self.ui.teHints.setPlainText(s)
            self.ui.teHints.setReadOnly(True)

        else:
            self.__lang = 'german'

            #   group boxes
            self.ui.gbBodyData.setTitle('Koerperdaten')
            self.ui.gbBDay.setTitle('Geburtstag')
            self.ui.gbHeightWeight.setTitle('Groesse und Gewicht')
            self.ui.gbTargets.setTitle('Ziele')
            self.ui.gbOthers.setTitle('Sonstiges')

            #   labels
            self.ui.lbBirthday.setText('Geburtstag:')
            self.ui.lbDay.setText('Tag')
            self.ui.lbMonth.setText('Monat')
            self.ui.lbYear.setText('Jahr')
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
            self.ui.btnSeek.setText('Armband nicht\ngefunden?\nErneut Suchen')
            self.ui.btnStart.setText('BodyMedia\nauslesen')
            self.ui.btnClearOnly.setText('BodyMedia aktivieren')
            self.ui.btnClose.setText('Beenden')
            self.ui.btnBodyData.setText('Aktuell eingestellte Koerperdaten auf das BodyMedia uebertragen')

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

            s = '''
    + BodyMeda aktivieren +
==================
Beim aktivieren werden alle aufgezeichneten Sensordaten auf dem Armband gelöscht!


+ Koerperdaten uebertragen +
==================
Beim uebertragen der Koerperdaten werden alle aufgezeichneten Sensordaten auf dem Armband gelöscht!'''
            self.ui.teHints.setReadOnly(False)
            self.ui.groupBox_2.setTitle('Hinweise')
            self.ui.teHints.setPlainText(s)
            self.ui.teHints.setReadOnly(True)

        self.Seek()

    #
    #
    #
    def PushToBM(self):
        self.SafeBody()

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

        w = int(self.ui.cbWeight.currentText())
        h = int(self.ui.cbHeight.currentText())
        d = int(self.ui.cbBDayDay.currentText())
        m = int(self.ui.cbBDayMonth.currentText())
        y = int(self.ui.cbBDayYear.currentText())

        self.SetBodyData(smoker, sex, hand, d, m, y, h, w)

    #
    #
    #
    def CheckSum(self, c):
        checksum = 0
        for item in c:
            checksum += item
        else:
            checksum = checksum % 256
            return struct.pack('B', checksum)

    #
    #
    #
    def __CreateSerialReq(self):
        sync = b'\xab'
        end= b'\xba\xba\xba\xba'
        s = b'\x03\x3c\x00\x00\x00\x00\x0e\xff\xff\xff\xff\x87\x01\x48\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        s = sync + s + self.CheckSum(s) + end
        return s

    #
    #
    #
    def __GetSerialNum(self):
        x = self.__CreateSerialReq()
        try:
            ser = serial.Serial(self.Port[0], baudrate=921600)
        except:
            print('\n\n  -- ERROR  Could not open Serial-Port! Aborting!')
            return

        ser.write(x)

        ret = b''
        i = 0
        while i < 66:
            ret += ser.read()
            i += 1
        else:
            ser.close()
            ser_num = ret[4:8]
            self.__SerNum = (ser_num[0] << 24) | (ser_num[1] << 16) | (ser_num[2] << 8) | ser_num[3]

    #
    #
    #
    def SetBodyData(self, smoker, sex, hand, d, m, y, h, w):
        self.__GetSerialNum()

        try:
            ser = serial.Serial(self.Port[0], baudrate=921600)
        except:
            print('\n\n  -- ERROR  Could not open Serial-Port! Aborting!')
            return

        t = int(time.time())
        if smoker == 'false':
            smoker =  b'\x02'
        else:
            smoker =  b'\x01'

        if sex == 'female':
            sex =  b'\x02'
        else:
            sex =  b'\x01'

        if hand =='left':
            hand = b'\x01'
        else:
            hand = b'\x02'

        h = int(round((h / 2.54), 0))
        w = int(round((w * 2.2046), 0))

        messages =  [
                b'\x03\x3c\x00\x00\x00\x00\x0e\xff\xff\xff\xff\x81\x01\x00\x00\x00\x00\x00\x00\x00\x00' + struct.pack('<I', self.__SerNum) + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e\xff\xff\xff\xff\x87\x02\x48\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e\xff\xff\xff\xff\x87\x03\x45\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x87\x04\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x87\x05\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x87\x06\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x89\x07\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x8c\x08\x80\x07\x02\x00\x10\x43\x55\x53\x54\x4f\x4d\x00\x00\x00\x08\x09\x0b\x0c\x0e\x10\x11\x12\x0d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x8c\x09\x80\x07\x02\x01\x11\x43\x55\x53\x54\x4f\x4d\x00\x00\x00\x14\x15\x17\x18\x19\x1a\x1b\x1c\x0d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x8c\x0a\x80\x07\x02\x02\x12\x43\x55\x53\x54\x4f\x4d\x00\x00\x00\x1d\x1e\x1f\x22\x23\x25\x26\x27\x0d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x8c\x0b\x80\x07\x02\x03\x13\x43\x55\x53\x54\x4f\x4d\x00\x00\x00\x28\xfe\xfe\xfe\xfe\xfe\xfe\xfe\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x8c\x0c\x00\x00\x02\x04\x14\x43\x55\x53\x54\x4f\x4d\x00\x00\x00\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x8c\x0d\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e\xff\xff\xff\xff\x87\x01\x11\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e\xff\xff\xff\xff\x81\x02\x00\x00\x00\x00\x00\x00\x00\x00' + struct.pack('<I', self.__SerNum) + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e\xff\xff\xff\xff\x87\x03\x48\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e\xff\xff\xff\xff\x87\x04\x45\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x87\x05\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x87\x06\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x87\x07\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x87\x08\x6c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x89\x09\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x0a' + hand + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3d\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x0b\xdc\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x63\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x89\x0c\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x0d' + struct.pack('i', t) + b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x0e' + struct.pack('B', m) + b'\x00\x00\x00' + struct.pack('B', d) + b'\x00\x00\x00' + struct.pack('H', y) + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x41\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x0f\x1a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x23\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x10\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x69\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x11\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x55\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x12\x60\x09\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x54\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x13\x31\x32\x33\x34\x35\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x30\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x14' + struct.pack('H', w) + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x24\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x56\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x16' + struct.pack('B', h) + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x25\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x17\x40\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x53\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x18\xb8\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x64\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x19' + sex + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x26\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x1a\x1a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x23\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x1b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x6a\x00',
                b'\x03\x3c\x00\x00\x00\x00\x0e' + struct.pack('>I', self.__SerNum) + b'\x86\x1c' + smoker + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3e\x00'
                ]

        sync = b'\xab'
        end= b'\xba\xba\xba\xba'
        cnt = 0
        for m in messages:
            s = sync + m + self.CheckSum(m) + end
            print('\nMessages to send remaining: %s' % (len(messages) - cnt))
            print('Send Message to BodyMedia...')
            ser.write(s)
            cnt += 1

            ret = b''
            i = 0
            print('Wait for Response...')
            while i < 66:
                ret = ser.read()
                i += 1
            else:
                print('Got Response...')
        else:
            ser.close()
            print('\n\nSend all Messages!')
