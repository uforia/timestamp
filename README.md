# Generic Timestamp Converter

Systems tend to use a mess of timestamp formats, and it can be pretty annoying having to deal with
a plethora of smaller tooling to convert them into something resembling a human-readable format.
Hence, this poorly cobbled-together script was born. It should work fine under most versions of
Python (tested with 2.7/3.x).

Comments, suggestions: arnime < squiggly thing > kpn-cert.nl

## What it does

This script is capable of detecting and converting various forms of hexadecimal timestamps
into something human readable. You can run it interactively, directly from the command-line or
you can pipe / redirect a hex string directly to it. Inter-byte spacing is not important, the
script will automatically compress it into something it will understand.

NOTE: for multiline/-item parsing, use the piping/redirect method.

## Current version's comments and considerations

There is only very basic checking done to see if the timestamp appears to be correct.
VAX/VMS timestamps might be working, but there's no way to really check. Feedback welcome!

# Usage

## Interactive mode

... $ ./timestamp.py  
Gimme a timestamp: e0070a0006000f0011002c0031007f00  
"Registry","2016-10-15 17:44:49.127"  
... $

## Command-line mode

... $ ./timestamp.py 919e6539  
"FAT","2008-11-05 19:52:34"  
... $

## Pipe/redirect mode

... $ echo 1346693048 C23F17B72EC9CB01 5FBF60C54F2CCF01 1346663048.283 1cf23440c2aac701 f975722c abcd|./timestamp.py  
"Integer","2012-09-03 17:24:08"  
"NTFS","2011-02-10 14:27:58.762388"  
"NTFS","2014-02-18 02:18:54.252426"  
"Integer","2012-09-03 09:04:08.283"  
"NTFS","2007-06-09 18:16:08.093750"  
"FAT","2002-03-18 14:47:50"  
"Error","abcd"  
... $
