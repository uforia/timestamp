#!/usr/bin/env python

# Version 1.1 (c) Arnim Eijkhoudt, KPN-CERT, arnime < at > kpn-cert.nl

import sys,datetime

if len(sys.argv)<2:
	if not sys.stdin.isatty():
		for line in sys.stdin:
			dt=line.replace(' ','').strip()
			break
	else:
		dt=''.join(input("Gimme a timestamp: ")).replace(' ','')
else:
	dt=''.join(sys.argv[1:]).replace(' ','')
if len(dt)==16:
	# ZOMG it's NTFS! Or is it VAX/VMS... *shudder*
	swapped="".join(reversed([dt[i:i+2] for i in range(0, len(dt), 2)]))
	try:
		ntfs=datetime.datetime(1601,1,1)+datetime.timedelta(microseconds=int(swapped,16)/10.)
		vax=datetime.datetime(1858,11,17)+datetime.timedelta(microseconds=int(swapped,16)/10.)
	except OverflowError:
		print("Timestamp is out of range!")
	else:
		# It's probably NTFS, since VAX wasn't born before 1858...
		print("NTFS timestamp: "+str(ntfs))
		# ...but on the off-chance...
		if int(str(ntfs)[0:4])>1858:
			print("VAX/VMS timestamp: "+str(vax))
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
if len(dt)>=10 and len(dt)<=14:
	# Perhaps an integer timestamp, ##########(.###) ?
	if '.' in dt:
		sec=int(dt.split('.')[0])
		ms=dt.split('.')[1]
		if len(ms)>1:
			ms="."+ms
	else:
		sec=int(dt)
		ms=""
	print("Integer timestamp: "+str(datetime.datetime(1970,1,1)+datetime.timedelta(seconds=sec))+ms)
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
		# Seriously, who thought 2-second precision was a good idea?
		sec=0
	try:
		print("FAT timestamp: "+str(datetime.datetime(1980+year,month,day,hour,min,sec)))
	except ValueError:
		print("Error in FAT timestamp!")
