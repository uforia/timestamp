#!/usr/bin/env python

# Version 1.3 (c) Arnim Eijkhoudt, KPN-CERT, arnime < at > kpn-cert.nl
# No license, do whatever you want with this. If you like it, I'd appreciate
# a shoutout though! :-)

import sys,datetime

def parseNTFS(timestamp):
	# ZOMG it's NTFS! Or is it VAX/VMS... *shudder*
	swapped="".join(reversed([timestamp[i:i+2] for i in range(0, len(timestamp), 2)]))
	try:
		ntfs=datetime.datetime(1601,1,1)+datetime.timedelta(microseconds=int(swapped,16)/10.)
		result="\"NTFS\",\""+str(ntfs)+"\""
	except:
		result="\"Error\",\""+str(timestamp)+"\""
	finally:
		return result

def parseRegistry(timestamp):
	try:
		year=timestamp[2:4]+timestamp[0:2]
		month=timestamp[6:8]+timestamp[4:6]
		weekday=timestamp[10:12]+timestamp[8:10]
		day=timestamp[14:16]+timestamp[12:14]
		hour=timestamp[18:20]+timestamp[16:18]
		min=timestamp[22:24]+timestamp[20:22]
		sec=timestamp[26:28]+timestamp[24:26]
		ms=timestamp[30:32]+timestamp[28:30]
		result="\"Registry\",\""+str(int(year,16))+'-'+str(int(month,16)).zfill(2)+'-'+str(int(day,16)).zfill(2)+' '+str(int(hour,16)).zfill(2)+':'+str(int(min,16)).zfill(2)+':'+str(int(sec,16)).zfill(2)+'.'+str(int(ms,16))+"\""
	except:
		result="\"Error\","+str(timestamp)+"\""
	finally:
		return result

def parseInteger(timestamp):
	# Perhaps an integer timestamp, ##########(.###) ?
	try:
		if '.' in timestamp:
			sec=int(timestamp.split('.')[0])
			ms=timestamp.split('.')[1]
			if len(ms)>1:
				ms="."+ms
		else:
			sec=int(timestamp)
			ms=""
		result="\"Integer\",\""+str(datetime.datetime(1970,1,1)+datetime.timedelta(seconds=sec))+ms+"\""
	except:
		result="\"Error\",\""+str(timestamp)+"\""
	finally:
		return result

def parseFAT(timestamp):
	# LOL u r so FAT!
	try:
		timestamp="".join(reversed([timestamp[i:i+2] for i in range(0, len(timestamp), 2)]))
		timestamp=int((timestamp[4:8]+timestamp[0:4]),16)
		day=timestamp&0x1f
		month=(timestamp>>5)&0x0f
		year=(timestamp>>9)&0x7f
		timestamp>>=16
		sec=(timestamp&0x1f)*2
		min=(timestamp>>5)&0x3f
		hour=(timestamp>>11)&0x1f
		if sec>59:
			# Seriously, who thought 2-second precision was a good idea?
			sec=59
		result="\"FAT\",\""+str(datetime.datetime(1980+year,month,day,hour,min,sec))+"\""
	except:
		result="\"Error\",\""+str(timestamp)+"\""
	finally:
		return result

def parseLine(timestamp):
	if len(timestamp)==16:
		print(parseNTFS(timestamp))
	elif len(timestamp)==32:
		print(parseRegistry(timestamp))
	elif len(timestamp)>=10 and len(timestamp)<=14:
		print(parseInteger(timestamp))
	elif len(timestamp)==8:
		print(parseFAT(timestamp))
	else:
		print("\"Error\",\""+str(timestamp)+"\"")

if __name__ == "__main__":
	if len(sys.argv)<2:
		if not sys.stdin.isatty():
			for line in sys.stdin:
				dt=line.split(' ')
				for item in dt:
					parseLine(item.strip())
		else:
			dt=''.join(input("Gimme a timestamp: ")).replace(' ','')
			parseLine(dt)
	else:
		dt=''.join(sys.argv[1:]).replace(' ','')
		parseLine(dt)
