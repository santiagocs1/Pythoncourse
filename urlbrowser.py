#!/usr/bin/env python
import urllib
fhand= urllib.urlopen('http://www.cisco.com/')
for line in fhand:
    print line.strip()
