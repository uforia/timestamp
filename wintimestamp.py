#!/usr/bin/env python

# Generic Timestamp Converter for Windows
# ---------------------------------------
#
# Version 0.8 (c) Arnim Eijkhoudt, KPN-CERT
#
# Windows is a mess of timestamp conventions, and we were getting pretty annoyed with having to
# mess around with a plethora of tooling to convert them into something resembling a human-
# readable format. Hence, this poorly cobbled-together script was born. It should work fine under
# most versions of Python (tested with 2.7/3.x).
#
# If you like this, good for you!
# If you don't like this, I don't wanna hear about it!
#
# What it does
# ------------
#
# This script is capable of detecting and converting Windows' Registry-, NTFS- and FAT-timestamps
# into something human readable. You can run it interactively, directly from the command-line or
# you can pipe / redirect a hex string directly to it. Inter-byte spacing is not important, the
# script will automatically compress it into something it will understand.
#
# Interactive mode
# ----------------
# ... $ ./timestamp.py
# Gimme a timestamp: e0 07 0a 00 06 00 0f 00  11 00 2c 00 31 00 7f 00
# Registry timestamp: 2016-06-15 17:44:49.127
# ... $
#
# Command-line mode
# -----------------
# ... $ ./timestamp.py 919e6539
# FAT timestamp: 2008-11-05 19:52:34
# ... $
#
# Pipe/redirect mode
# ------------------
# ... $ echo "01cb17701e9c885a" | ./timestamp.py
# NTFS timestamp: 2010-06-29 09:47:42.754212
# ... $

import sys,datetime
if len(sys.argv)<2:
	if not sys.stdin.isatty():
		for line in sys.stdin:
			dt=line.replace(' ','').strip()
			break
	else:
		dt=''.join(raw_input("Gimme a timestamp: ")).replace(' ','')
else:
	dt=''.join(sys.argv[1:]).replace(' ','')
if len(dt)==16:
	# ZOMG it's NTFS!
	us=int("".join(reversed([dt[i:i+2] for i in range(0, len(dt), 2)])),16)/10.
	print("NTFS timestamp: "+str(datetime.datetime(1601,1,1)+datetime.timedelta(microseconds=us)))
if len(dt)==32:
	# Crikey, a registry timestamp
	year=dt[2:4]+dt[0:2]
	month=dt[6:8]+dt[4:6]
	weekday=dt[10:12]+dt[8:10]
	day=dt[14:16]+dt[12:14]
	hour=dt[18:20]+dt[16:18]
	min=dt[22:24]+dt[20:22]
	sec=dt[26:28]+dt[24:26]
	ms=dt[30:32]+dt[28:30]
	print("Registry timestamp: "+str(int(year,16))+'-'+str(int(month,16)).zfill(2)+'-'+str(int(day,16)).zfill(2)+' '+str(int(hour,16)).zfill(2)+':'+str(int(min,16)).zfill(2)+':'+str(int(sec,16)).zfill(2)+'.'+str(int(ms,16)))
if len(dt)==8:
	# LOL u r so FAT!
	dt="".join(reversed([dt[i:i+2] for i in range(0, len(dt), 2)]))
	dt=int((dt[4:8]+dt[0:4]),16)
	day=dt&0x1f
	month=(dt>>5)&0x0f
	year=(dt>>9)&0x7f
	dt>>=16
	sec=(dt&0x1f)*2
	min=(dt>>5)&0x3f
	hour=(dt>>11)&0x1f
	if sec>59:
		sec=0
	try:
		print("FAT timestamp: "+str(datetime.datetime(1980+year,month,day,hour,min,sec)))
	except ValueError:
		print("Error in FAT timestamp!")
