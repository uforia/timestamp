## Generic Timestamp Converter for Windows

Windows is a mess of timestamp conventions, and we were getting pretty annoyed with having to
mess around with a plethora of tooling to convert them into something resembling a human-
readable format. Hence, this poorly cobbled-together script was born. It should work fine under
most versions of Python (tested with 2.7/3.x).

If you like this, good for you!
If you don't like this, I don't wanna hear about it!

# What it does

This script is capable of detecting and converting Windows' Registry-, NTFS- and FAT-timestamps
into something human readable. You can run it interactively, directly from the command-line or
you can pipe / redirect a hex string directly to it. Inter-byte spacing is not important, the
script will automatically compress it into something it will understand.

# Comments

There is some very basic checking done to see if the timestamp appears to be correct.
VAX/VMS timestamps might be working, but there's no way to really check. Feedback welcome!

## Usage

# Interactive mode

... $ ./wintimestamp.py  
Gimme a timestamp: e0 07 0a 00 06 00 0f 00  11 00 2c 00 31 00 7f 00  
Registry timestamp: 2016-10-15 17:44:49.127  
... $

# Command-line mode

... $ ./wintimestamp.py 919e6539  
FAT timestamp: 2008-11-05 19:52:34  
... $

# Pipe/redirect mode

... $ echo "C2 3F 17 B7 2E C9 C7 01" | ./wintimestamp.py  
NTFS timestamp: 2007-07-18 11:28:08.078124  
VAX/VMS timestamp: 2265-06-02 11:28:08.078124  
... $
