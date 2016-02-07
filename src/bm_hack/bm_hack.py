#!/usr/bin/env python2
#
# BodyMedia ArmBand Device Library
#
# July 2009 by Centi Benzo centibenzo@gmail.com
#
#
# Code modifyed and shrinked down to the only needed parts
# by bloodywulf in December 2015
#
#
# THIS CODE IS DECLARED BY THE AUTHOR TO BE IN THE PUBLIC DOMAIN.
# NO WARRANTY OF ANY KIND IS PROVIDED.
#
# See blog for notes: bodybugglinux.blogspot.com
#
# LIBRARY VERSION - z718a
#
# BodyMedia Notes
# FCC ID PV8-MF filings provide internal photos
# Interal photos reveal:
#  -Fractus chip antenna
#  -FTDI QFP-32 - from footprint, FT232BL? (8-bit parallel)
#  -8-pin SSC chip
#  -16-pin chip
#  -16-pin chip
#  -64-pin chip, blurred number *161*(?) - ?MSP430F1612? 16-bit MCU, 5120B RAM, 55kB Flash
#  -LiPoly 3.7V 300mAh battery
#


import string
import struct
import serial
import sys
import cPickle
import getopt
import time
import math
from numpy import array, ndarray, fromstring, zeros, resize
import numpy


def ListToByteString(l):
    return struct.pack("B" * len(l), *l)


def OpenSerial(fname="/dev/ttyUSB0"):
    ser=serial.Serial(fname,baudrate=921600,timeout=.01)
    # Device needs some commands to warm up.  Won't always get response to first command (NOT timeout issue)
    fail=0
    while True:
        p=[0x80, 0x01, 0x01]  # simple "register" read
        cmd = CreateSimpleRequest(p)
        try:
            WriteAndReadSerialPacket(ser, cmd)
            break
        except:
            print "Attempting to talk to device, try %i - trying again..." % fail
            fail += 1
        if fail > 5:
            raise Exception("Failed to talk to device!")
    return ser


def ReadSerial(ser, minLen, timeout=3.0, maxLen=2**15):
    """Read at least minLen bytes from serial, with specified timeout.  This
    varies from the Serial.setTimeout() character timeout, since a read may
    return prematurely."""
    s=''
    t0=time.time()
    while True:
        s += ser.read(maxLen - len(s))
        if len(s) >= minLen or len(s) == maxLen:
            return s
        if time.time() - t0 > timeout:
            raise Exception("ReadSerial timeout after %f sec, expected %i bytes, got %i bytes: %s" % (time.time() - t0, minLen, len(s), s))


def WriteAndReadSerialPacket(ser, packet):
    """Write specified packet, and read the response.
        Detects if packet expects a "burst" response, and 
        reads exactly that many response packets.  """
    assert len(packet) == 69, "Exptected a request packet of size 69, not %i" % len(packet)
    parse = ParsePacket2(packet)
    assert parse['type'] == 'Req', "WriteAndReadSerial expect a Req type packet as parameter"
    rlen = parse.get('rlen',1)
    n = int(math.ceil(float(rlen)/44.))
    ser.write(packet)
    return ReadSerial(ser, minLen=n*66, maxLen=n*66)


def CreateMemoryReadPacket(offset, length):
    """Construct a memory request packet for starting address and length"""
    buf = struct.pack('<BBIH', 0x82, 0x0, offset, length)
    return CreateSimpleRequest(buf)


def MemoryDump(ser, offset=0, length=2*(2**20), stopAtFF=True):
    """Produce a memory dump from the serial device.  if stopAtFF==True,
    the stop reading when a response packet of all 0xFF occurs.  length is
    the size of memory to read.  Physical device has a 2MByte address
    space.  GoWearFit software usually reads up until 193,600 bytes."""
    packets=[]
    total=0
    while total < length:
        rlen = min(length - total, 8800)
        pp = CreateMemoryReadPacket(total, rlen)
        packets.append(pp)
        sys.stderr.write(".")
        packets.append(WriteAndReadSerialPacket(ser, pp))
        total += rlen
        if stopAtFF and packets[-1][-66+20:-66+63] == '\xff'*43:
            break
    mem = AssembleDataFromPackets(packets)
    return (packets, mem)


def ClearMemory(ser):
    """Clear sensor data from memory.
        There may be other memory ranges. I also see a 0x89..0x04 command.
        Returns the response from the device."""
    pac = [0x89, 0x85, 0x02] # 85 is just the dumb sequence number
    ser.write(CreateSimpleRequest(pac))
    return ReadSerial(ser, 66)


def Checksum(pk):
    chk=0
    for x in pk:
        chk += ord(x)
    return chk


def CreateSimpleRequest(addr):
    """Creates a simple request using an address.
        addr should be a list of four address(?) bytes.
        ex: [0x8B, 0x24, 0x1, 0x11]
        Also will accept a string.
    """
    if type(addr) == list:
        addr = ListToByteString(addr)
    # Unchanging header (at least in any data we've seen)
    # Rudy has identified some fields, but we don't need them
    fromAddr= "\x00\x00\x00\x0e"
    toAddr  = "\xff\xff\xff\xff" # this is usually the device HW address
    pk ='\xab\x03\x3c\x00' + fromAddr + toAddr
    pk += addr
    # Zero pad the rest of payload
    pk += ListToByteString([0]*(64-len(pk)))
    checksum = Checksum(pk[1:]) # sync byte not included
    pk += chr(checksum % 256)
    pk += '\xba\xba\xba\xba'
    return pk


def SimpleReq(ser, addr):
    pk = CreateSimpleRequest(addr)
    ser.write(pk)
    a=ReadSerial(ser, 66)
    return a


def SplitBurst(pk):
    """Split a burst packet into its sub-packets.
        Burst packets are always (?) split into 66 byte sub-packets."""
    v=[]
    while len(pk) > 0:
        v.append(pk[0:66])
        pk = pk[66:]
    return v


def ParsePacket2(pk):
    if type(pk) == list:
        return [ParsePacket2(x) for x in pk]
    # Detect and recurse on burst packet
    if len(pk) > 130:
        burst = SplitBurst(pk)
        return dict([("type","Burst"), ("burst", [ParsePacket2(x) for x in burst])])
    d={}
    # split the end and start padding
    if pk[-4:] == '\xba\xba\xba\xba':
        pk = pk[:-4]
    elif pk[-1] == '\xba':
        pk = pk[:-1]
    else:
        raise Exception("Unexpected padding "+pk[-4:])
    assert pk[0] == '\xab',"Sync byte not equal to AB"
    pk= pk[1:]
    # Now perform checksum (w/o padding or checksum field)
    checksum = Checksum(pk[:-1])
    if pk[0] == '\x03':
        d['type']='Req'
    elif pk[0] == '\x04':
        d['type']='Ans'
    else:
        raise Exception("Unkown packet type")
    pk= pk[1:]
    d['len']= 256*ord(pk[1]) + ord(pk[0])
    pk= pk[2:]
    assert d['len'] > 59, "Packet len too short"
    d['fromAddr']= pk[:4]
    pk= pk[4:]
    d['toAddr']= pk[:4]
    pk= pk[4:]
    d['reqbit']= (ord(pk[0]) & 0x80)>>7
    d['bank']= 0x7F&ord(pk[0])
    pk= pk[1:]
    d['n']= ord(pk[0])
    pk= pk[1:]
    # Split off body
    d['body']= pk[0:-1]
    # checksum
    d['chk']= ord(pk[-1])
    if d['chk'] != (checksum % 256):
        raise Exception("ERROR: Checksum mismatch %x != %x" % (d['chk'], checksum % 256))
    #### Read Burst Fields
    if d['type'] == 'Req' and d['bank'] == 0x2:
        d['offset']=fromstring(pk[0] + pk[1]+ pk[2] + pk[3],'uint32')[0]
        pk= pk[4:]
        d['rlen']= fromstring(pk[0] + pk[1],'uint16')[0]
    if d['type'] == 'Ans' and d['bank'] == 0x2:
        d['offset']=fromstring(pk[0] + pk[1]+ pk[2] + pk[3],'uint32')[0]
        pk= pk[4:]
        d['rlen']= fromstring(pk[1] + pk[0],'uint16')[0]
    return d


def FlattenBurstPackets(packets):
    output=[]
    for p in packets:
        if p['type'] == "Burst":
            output.extend(p['burst'])
        else:
            output.append(p)
    return output


def AssembleDataFromPackets(packets):
    """Create a single data array from a set of packets.
        Will operate on a list of parsed packet dictionaries, or a list of raw
        packets in string form"""
    if len(packets) == 0:
        return []
    if type(packets[0]) == str:
        packets = ParsePacket2(packets)
    packets = FlattenBurstPackets(packets)
    ##memsize = 0x30e61
    ##mem = zeros([memsize],'uint8')
    mem = zeros([0],'uint8')
    for p in packets:
        if p['type'] == 'Ans' and p['bank'] == 0x2:
            o=p['offset']
            sz=p['rlen']
            assert len(p['body']) == sz + 6, Exception("body/length mismatch")
            #assert o + sz < memsize, Exception("Memory overflow: assumed memory size too small")
            if (o + sz) > len(mem):
                mem = numpy.resize(mem, (o+sz))
            mem[o:o+sz] = fromstring(p['body'][6:], dtype='uint8')
    return mem


def HexStringToInt(s):
    """Binary data in MSB string format."""
    n=0
    for x in s:
        n = n*256 + ord(x)
    return n


# struct representation of records
# Number of times the corresponding RecPack record repeats, if any
# second field is initial reading before repeat, if any
RecRepeat={}
# Record structure
RecPack={}
# Type #1 - Advanced Record layouts
RecPack[1] = '<B 9s HB 8B B '
RecRepeat[1] = (5, "")
# Type #6 - Field Names
RecPack[6] = '<B 9s'
RecRepeat[6] = (42, "<BB")
# Type #2 and #3 - Timestamps (whats the difference?)
RecPack[2] = '<I'
RecPack[3] = '<I'
# Type #53 - Timestamp with unknown field (band on, band off?)
RecPack[53] = '<6B I'
# Type #48 - Unknown record discovered by Freak
RecPack[48] = '<I'
# 12-bit field advanced record types (comes from type #1 table)
RecPack[16] = 13
RecPack[17] = 12
RecPack[18] = 12
RecPack[19] = 9


def ReadPacked12Bit(d):
    """Read 12-bit packed array of ints in d"""
    if type(d) == ndarray:
        d=d.tostring()
    h = d.encode('hex')
    v = []
    pos=0
    for pos in range(0, len(h),3):
        if len(h[pos:pos+3]) < 3: # record boundries padded 0xf
            break
        v.append(int("0"+h[pos:pos+3], 16))
    return v


def ReadRecord(d, offset=0x0):
    id = d[0]
    d=d[1:] # Eat id
    if id == 0xff or id == 0x4: # Normal end of Data
        return id, None, None
    sztotal = 1 
    assert RecPack.has_key(id), "Unknown record ID %i at offset %i" % (id, offset)
    if RecRepeat.has_key(id):
        sz = struct.calcsize(RecPack[id])
        init=struct.unpack_from(RecRepeat[id][1], d)
        szinit=struct.calcsize(RecRepeat[id][1])
        d=d[szinit:]
        sztotal += szinit
        res=[]
        for i in range(0, RecRepeat[id][0]):
            res.append(struct.unpack_from(RecPack[id], d))
            d=d[sz:]
            sztotal += sz
    elif type(RecPack[id]) == str:
        sz = struct.calcsize(RecPack[id])
        res = struct.unpack_from(RecPack[id], d)
        sztotal += sz
    elif type(RecPack[id]) == int: # 12-bit field array
        # A padding byte 0xFF may be present
        sz = RecPack[id] - 1
        res = ReadPacked12Bit(d[:sz])
        sztotal += sz
    return id, sztotal, res


def ReadAllRecords(mem):
    offset=0
    v=[]
    while True:
        r = ReadRecord(mem[offset:], offset)
        if r[0] == 0xff or r[0] == 0x4: # Normal end of data
            return v
        v.append(r)
        offset += r[1]


def WriteTabDelim(t,fhandle=None):
    if fhandle == None:
        fhandle=sys.stdout
    for r in t:
        for f in r:
            fhandle.write(str(f)+"\t")
        fhandle.write("\n")


def GetFields(type1Layout, type6Names):
    """Return a dictionary of field names for all record types listed in
    type1Layout"""
    fields={}
    for r in type1Layout[2]:
        fields[r[0]] = [type6Names[2][i][1].rstrip('\x00') for i in r[3:11] if i != 254]
    return fields


def RecordTable(packets):
    mem=AssembleDataFromPackets(packets)
    recs=ReadAllRecords(mem)
    assert len(recs) > 3, "No sensor data is currently on the device (or dump)"
    # We record the last encountered
    last={}
    lastTimestamp=None
    lastTimestampRow=None
    fields=None
    out=[]
    for r in recs:
        last[r[0]] = r
        # Output line if we have a 16, 17, and 18, and 19
        if len(set([16,17,18,19]) - set(last.keys())) == 0 and lastTimestamp != None:
            t = lastTimestamp + 60*(len(out) - lastTimestampRow)
            ct = time.strftime("%a %m/%d/%y %H:%M:%S", time.localtime(t))
            out.append([t, ct] + last[16][2] + last[17][2] + last[18][2] + last[19][2])
            last.pop(16)
            last.pop(17)
            last.pop(18)
            last.pop(19)
        if r[0] in set([2,3]):
            lastTimestamp = r[2][0]
            lastTimestampRow = len(out)
        elif r[0]==53:
            lastTimestamp = r[2][6]
            lastTimestampRow = len(out)
        if last.has_key(1) and last.has_key(6):
            f = GetFields(last[1], last[6])
            fields = ["EPOCH", "TIME"]
            for x in 16,17,18,19:
                fields.extend(f[x])
    return fields, out


def SaveStructTabDelim3(packets,fname=None):
    fields, records = RecordTable(packets)
    if fname != None:
        # Write out
        f=open(fname,"w")
        WriteTabDelim([fields] + records, f)
        f.flush()
        f.close()
    else:
        WriteTabDelim([fields] + records)


### Main function

def main():
    sys.stderr.write("""\n\nTHIS CODE IS DECLARED BY THE AUTHOR TO BE IN THE PUBLIC DOMAIN.\nNO WARRANTY EXPRESSED OR IMPLIED OF ANY KIND IS PROVIDED.\n\n""")

    opts, args = getopt.getopt(sys.argv[1:], "h", ["help",
        "fromSerial=", "fromSerialFull=", "fromDump=", "fromFSPM=", "toDump=", 
        "toCsv=", "toPackets=", "toMemDump=", "toMemHex=", "toMemHexColor=", 
        "clear"])
    dopts = dict(opts)
	
    if dopts.has_key("--fromSerial"):
        ser = OpenSerial(dopts["--fromSerial"])
        packets, mem = MemoryDump(ser)
        ser.close()

    if dopts.has_key("--toCsv"):
        if dopts['--toCsv'] != '-':
                SaveStructTabDelim3(packets, dopts['--toCsv'])
        else: # stdout
            SaveStructTabDelim3(packets)
        print >>sys.stderr, "Wrote tab-delimited CSV file to "+dopts['--toCsv']

    if dopts.has_key("--clear"):
        ser = OpenSerial(dopts["--fromSerial"])
        ClearMemory(ser)
        print >>sys.stderr, "Cleared logged sensor data from device"
        ser.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
