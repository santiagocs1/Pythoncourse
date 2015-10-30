#!/usr/bin/env python
import telnetlib
import time
rtr1= '50.76.53.27'
username= 'pyclass'
passw= '88newclass'
remote_conn=telnetlib.Telnet(rtr1,23,6)
output=remote_conn.read_until("Username:",6)
remote_conn.write(username + '\n')
output=remote_conn.read_until("Password:",6)
remote_conn.write(passw + '\n')
time.sleep(1)
remote_conn.write('show ip int brief' + '\n')
time.sleep(1)
output=remote_conn.read_very_eager()
print output




