#!/usr/bin/env python3

#
#   This file is part of FreeTheBodyM/bm_gui
#   FreeTheBodyM/src/bm_gui/src/file_op.py
#
#
#   This module is for parsing the csv file and write the swd file
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

import math
import time
import datetime
import os
import zipfile

class FileOp:

    #
    #
    #
    def __init__(self, csv, xml, swd, header):
        self.Csv = open(csv, mode='r', encoding='utf-8')
        self.Xml = open(xml, mode='w', encoding='utf-8')
        self.Swd = [swd, xml]
        self.header_values = header
        self.__timelist = []

        self.__timestamp                                        = []
        self.__raw_ee_list                                      = []
        self.__movavg_skin_temp_list                            = []
        self.__movavg_gsr_list                                  = []
        self.__movavg_accelerometer_transverse_list             = []
        self.__movavg_accelerometer_longitudinal_list           = []
        self.__movavg_battery_list                              = []
        self.__movavg_cover_temp_list                           = []
        self.__meandiff_accelerometer_transverse_ff2_list       = []
        self.__meandiff_accelerometer_longitudinal_ff2_list     = []
        self.__meancross_accelerometer_forward_list             = []
        self.__pedometer3_list                                  = []
        self.__plateau_accelerometer_longitudinal_list          = []
        self.__numpeaks_accelerometer_transverse_list           = []
        self.__movtheta_accelerometer_list                      = []
        self.__numpeaks_accelerometer_forward_list              = []
        self.__count_accelerometer_forward_list                 = []
        self.__movavg_accelerometer_forward_list                = []
        self.__meandiff_accelerometer_forward_list              = []
        self.__count_accelerometer_transverse_list              = []
        self.__count_accelerometer_longitudinal_list            = []
        self.__toe_strike3_list                                 = []
        self.__meancross_accelerometer_transverse_list          = []
        self.__meancross_accelerometer_longitudinal_list        = []
        self.__logsweep_accelerometer_list                      = []
        self.__madtheta_accelerometer_list                      = []
        self.__numpeaks_accelerometer_longitudinal_list         = []
        self.__movavg_composite_gsr_list                        = []


    #
    #
    #
    def Run(self):
        r = self.Csv.read()
        self.Csv.close()
        r = r.replace('\t', ';').split('\n')[1:-1]

        for i in range(len(r)):
            x = r[i].split(';')

            if x[2] == '4095':
                x[2] = '0'

            if x[6] == '4095':
                x[6] = '0'

            if x[9] == '4095':
                x[9] = '0'

            if x[27] == '4095':
                x[27] = '0'

            if x[28] == '4095':
                x[28] = '0'

            self.__timestamp.append(x[0])
            self.__movavg_skin_temp_list.append(x[2])
            self.__movavg_accelerometer_transverse_list.append(x[3])
            self.__movavg_accelerometer_longitudinal_list.append(x[4])
            self.__movavg_accelerometer_forward_list.append(x[5])
            self.__movavg_cover_temp_list.append(x[6])
            self.__meandiff_accelerometer_transverse_ff2_list.append(x[7])
            self.__meandiff_accelerometer_longitudinal_ff2_list.append(x[8])
            self.__movavg_composite_gsr_list.append(x[9])
            self.__pedometer3_list.append(x[10])
            self.__plateau_accelerometer_longitudinal_list.append(x[11])
            self.__numpeaks_accelerometer_transverse_list.append(x[12])
            self.__movtheta_accelerometer_list.append(x[13])
            self.__madtheta_accelerometer_list.append(x[14])
            self.__count_accelerometer_transverse_list.append(x[15])
            self.__logsweep_accelerometer_list.append(x[16])
            self.__count_accelerometer_longitudinal_list.append(x[17])
            self.__meancross_accelerometer_transverse_list.append(x[18])
            self.__meancross_accelerometer_longitudinal_list.append(x[19])
            self.__toe_strike3_list.append(x[20])
            self.__numpeaks_accelerometer_longitudinal_list.append(x[21])
            self.__movavg_battery_list.append(x[22])
            self.__meandiff_accelerometer_forward_list.append(x[23])
            self.__count_accelerometer_forward_list.append(x[24])
            self.__meancross_accelerometer_forward_list.append(x[25])
            self.__numpeaks_accelerometer_forward_list.append(x[26])
            self.__movavg_gsr_list.append(x[27])
            self.__raw_ee_list.append(x[28])

        self.Timestamp()
        self.CreateHeader(self.header_values[0], self.header_values[1], self.header_values[2], self.header_values[3], self.header_values[4], self.header_values[5],
                          self.header_values[6], self.header_values[7], self.header_values[8], self.header_values[9])

        self.CreateTagList('raw_ee', self.CreateLists(self.__raw_ee_list))
        self.CreateTagList('movavg_skin_temp', self.CreateLists(self.__movavg_skin_temp_list))
        self.CreateTagList('movavg_gsr', self.CreateLists(self.__movavg_gsr_list))
        self.CreateTagList('movavg_accelerometer_transverse', self.CreateLists(self.__movavg_accelerometer_transverse_list))
        self.CreateTagList('movavg_accelerometer_longitudinal', self.CreateLists(self.__movavg_accelerometer_longitudinal_list))
        self.CreateTagList('movavg_battery', self.CreateLists(self.__movavg_battery_list))
        self.CreateTagList('movavg_cover_temp', self.CreateLists(self.__movavg_cover_temp_list))
        self.CreateTagList('meandiff_accelerometer_transverse_ff2', self.CreateLists(self.__meandiff_accelerometer_transverse_ff2_list))
        self.CreateTagList('meandiff_accelerometer_longitudinal_ff2', self.CreateLists(self.__meandiff_accelerometer_longitudinal_ff2_list))
        self.CreateTagList('meancross_accelerometer_forward', self.CreateLists(self.__meancross_accelerometer_forward_list))
        self.CreateTagList('pedometer3', self.CreateLists(self.__pedometer3_list))
        self.CreateTagList('plateau_accelerometer_longitudinal', self.CreateLists(self.__plateau_accelerometer_longitudinal_list))
        self.CreateTagList('numpeaks_accelerometer_transverse', self.CreateLists(self.__numpeaks_accelerometer_transverse_list))
        self.CreateTagList('movtheta_accelerometer', self.CreateLists(self.__movtheta_accelerometer_list))
        self.CreateTagList('numpeaks_accelerometer_forward', self.CreateLists(self.__numpeaks_accelerometer_forward_list))
        self.CreateTagList('count_accelerometer_forward', self.CreateLists(self.__count_accelerometer_forward_list))
        self.CreateTagList('movavg_accelerometer_forward', self.CreateLists(self.__movavg_accelerometer_forward_list))
        self.CreateTagList('meandiff_accelerometer_forward', self.CreateLists(self.__meandiff_accelerometer_forward_list))
        self.CreateTagList('count_accelerometer_transverse', self.CreateLists(self.__count_accelerometer_transverse_list))
        self.CreateTagList('count_accelerometer_longitudinal', self.CreateLists(self.__count_accelerometer_longitudinal_list))
        self.CreateTagList('toe_strike3', self.CreateLists(self.__toe_strike3_list))
        self.CreateTagList('meancross_accelerometer_transverse', self.CreateLists(self.__meancross_accelerometer_transverse_list))
        self.CreateTagList('meancross_accelerometer_longitudinal', self.CreateLists(self.__meancross_accelerometer_longitudinal_list))
        self.CreateTagList('logsweep_accelerometer', self.CreateLists(self.__logsweep_accelerometer_list))
        self.CreateTagList('madtheta_accelerometer', self.CreateLists(self.__madtheta_accelerometer_list))
        self.CreateTagList('numpeaks_accelerometer_longitudinal', self.CreateLists(self.__numpeaks_accelerometer_longitudinal_list))
        self.CreateTagList('movavg_composite_gsr', self.CreateLists(self.__movavg_composite_gsr_list))

        self.CreateFooter()

        self.Xml.write('</SaveSet>')
        self.Xml.close()
        self.Compress(self.Swd[0], self.Swd[1])
        os.remove(self.Swd[1])

    #
    #
    #
    def Timestamp(self):
        for time in self.__timestamp:
            i_time = int(time)
            end = i_time
            start = i_time - 60
            end_str = datetime.datetime.fromtimestamp(end).strftime('%Y.%m.%d %H:%M:%S:0000')
            start_str = datetime.datetime.fromtimestamp(start).strftime('%Y.%m.%d %H:%M:%S:0000')
            self.__timelist.append([start_str, end_str, start, end])

    #
    #
    #
    def CreateLists(self, list_to_split):
        ret_list = []
        val_list = []
        start_str = self.__timelist[0][0][8:10]
        end_str = self.__timelist[0][1][8:10]
        start = self.__timelist[0][2]
        end = self.__timelist[0][3]
        for i in range(len(self.__timelist)):
            start_str = self.__timelist[i][0][8:10]
            start = self.__timelist[i][2]
            if end_str == start_str:
                if start - end > 60:
                    ret_list.append(val_list)
                    val_list = []
                    val_list.append([self.__timelist[i][0], self.__timelist[i][1], list_to_split[i]])
                else:
                    val_list.append([self.__timelist[i][0], self.__timelist[i][1], list_to_split[i]])

            else:
                ret_list.append(val_list)
                val_list = []
                val_list.append([self.__timelist[i][0], self.__timelist[i][1], list_to_split[i]])
            end_str = start_str
            end = start
        ret_list.append(val_list)
        return ret_list

    #
    #
    #
    def CreateHeader(self, hand, weight, height, sex, smoker, eetarget, steptarget, day, month, year):
        if int(day) < 10:
            day = '0%s' % (day)

        if int(month) < 10:
            month = '0%s' % (month)

        ts = int(time.time())
        date = datetime.datetime.fromtimestamp(ts).strftime('%m/%d/%Y')
        epoch = datetime.datetime.fromtimestamp(ts).strftime('%Y.%m.%d %H:%M:%S:000')
        t = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

        head = '''<?xml version="1.0" encoding="UTF-8"?>
<SaveSet>
<SDK2 Version="2.0">
  <Calibration>
    <AccelerometerX>
      <value input="0" output="2045" />
      <value input="1000" output="2484" />
    </AccelerometerX>
    <AccelerometerY>
      <value input="0" output="2040" />
      <value input="1000" output="2479" />
    </AccelerometerY>
    <AccelerometerF>
      <value input="0" output="2061" />
      <value input="1000" output="2500" />
    </AccelerometerF>
    <GSR>
      <value input="0" output="1361" />
    </GSR>
    <HF />
    <skinTemp>
      <value input="40000" output="2721" />
      <value input="25002" output="2048" />
    </skinTemp>
    <OnBody>
      <value input="0" output="1367" />
    </OnBody>
    <HFCoverTemp>
      <value input="40000" output="2721" />
      <value input="25002" output="2048" />
    </HFCoverTemp>
  </Calibration>
  <Parameter Name="Product Code" Value="164" />
  <Parameter Name="Battery" Value="85%%" />
  <Parameter Name="Handedness" Value="%s" />
  <Parameter Name="modthreshold" Value="3.0" />
  <Parameter Name="Birthdate" Value="%s%s%s" />
  <Parameter Name="Date" Value="%s" />
  <Parameter Name="Epoch" Value="%s" />
  <Parameter Name="secondactivity" Value="1" />
  <Parameter Name="capabilities" Value="44" />
  <Parameter Name="SystemTime" Value="%s" />
  <Parameter Name="Board Number" Value="123456789" />
  <Parameter Name="Version" Value="10.04" />
  <Parameter Name="modtarget" Value="30" />
  <Parameter Name="TimezoneOffset" Value="1" />
  <Parameter Name="eetarget" Value="%s" />
  <Parameter Name="Subject" Value="123456" />
  <Parameter Name="Weight" Value="%s" />
  <Parameter Name="Memory" Value="2097148/34699/98%%" />
  <Parameter Name="vigtarget" Value="15" />
  <Parameter Name="Firmware" Value="10.04.07" />
  <Parameter Name="Height" Value="%s" />
  <Parameter Name="steptarget" Value="%s" />
  <Parameter Name="Time" Value="%s" />
  <Parameter Name="Board Series" Value="17" />
  <Parameter Name="Volume" Value="142" />
  <Parameter Name="vigthreshold" Value="6.0" />
  <Parameter Name="Sex" Value="%s" />
  <Parameter Name="display1224" Value="255" />
  <Parameter Name="Serial Number" Value="123456789" />
  <Parameter Name="Smoker" Value="%s" />
  <Parameter Name="DeviceTime" Value="%s" />
  <Timezone Value="Europe/Berlin" />
  <Researcher name="" organization="" department="" />
  <METS Value="3.0" />
  <Notes notes="This File was created from bm_gui written by bloody_wulf!" />
  <METSLevels>
    <level index="0" label="Sitzend" min="0.0" max="1.5" />
    <level index="1" label="Leicht" min="1.5" max="3.0" />
    <level index="2" label="Moderat" min="3.0" max="6.0" />
    <level index="3" label="Anstrengend" min="6.0" max="9.0" />
    <level index="4" label="Sehr anstrengend" min="9.0" max="12345.6" />
  </METSLevels>
  <Biometric />
</SDK2><History>
  <Retrieve version="8.1.0.22" />
  <Item version="2.0" />
</History>''' % (hand, year, month, day, date, epoch, ts, eetarget, math.ceil((weight * 2.2046) + 0.5), math.ceil((height / 2.54) + 0.5), steptarget, t, sex, smoker, t)
        self.Xml.write(head)

    #
    #
    #
    def CreateFooter(self):
        session = ''
        session_list = []
        start_str = self.__timelist[0][0]
        end_str = self.__timelist[0][1]
        start = self.__timelist[0][2]
        end = self.__timelist[0][3]

        session_list.append(start_str)

        for x in self.__timelist:
            start_str = x[0]
            start = x[2]
            if end_str[8:10] != start_str[8:10] or start - end > 60:
                session_list.append(end_str)
                session_list.append(start_str)
            elif x[0][8:10] != x[1][8:10]:
                continue

            end_str = x[1]
            end = x[3]
        else:
            session_list.append(x[1])

        for i in range(0, len(session_list), 2):
            session = '''<Series type="session" granularity="second" start="%s" end="%s">
 <Event start="%s" end="%s"/>
</Series>\n''' % (session_list[i], session_list[i + 1], session_list[i], session_list[i + 1])
            self.Xml.write(session)


        up = '''<Series type="upload" granularity="second" start="%s" end="%s">
 <Event start="%s" end="%s" serial="123456789" type="17" version="10.04"/>
</Series>\n''' % (self.__timelist[0][0], self.__timelist[-1][1], self.__timelist[0][0], self.__timelist[-1][1])

        self.Xml.write(up)

    #
    #
    #
    def CreateTagList(self, tagname, value_list):
        tags = ''
        content = ''

        for sublist in value_list:
            taghead = '<Series type="%s" granularity="minute" start="%s" end="%s" sample_rate="60000000">\n' % (tagname, sublist[0][0], sublist[-1][1])
            for subsub in sublist:
                tags += ' <Event start="%s" end="%s" anon="%s"/>\n' % (subsub[0], subsub[1], subsub[2])
            else:
                content += taghead + tags + '</Series>\n'
                tags = ''
        self.Xml.write(content)

    #
    #
    #
    def Compress(self, path, path_to_compress):
        z = zipfile.ZipFile(path, mode='w', compression=zipfile.ZIP_DEFLATED)
        z.write(path_to_compress)
        z.close()



#
#
#
def main():
    a = ['test.csv']
    b = ['test.xml']
    c = ['test.swd']

    d = ['right', 98, 186, 'female', '38', 'false', '2100', '5575', '11', '12', '1980']

    for i in range(len(a)):
        f = FileOp(a[i], b[i], c[i], d)
        f.Run()
        f = None

if __name__ == '__main__':
    main()
