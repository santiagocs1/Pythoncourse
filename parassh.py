#!/usr/bin/env python
import paramiko
from getpass import getpass
import time
ip = '50.76.53.27'
port = 8022
passw = getpass()
#passwd='88newclass' 
conn = paramiko.SSHClient()
conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
conn.connect(ip, username='pyclass', password=passw, look_for_keys=False, allow_agent=False, port=port)
con= conn.invoke_shell()
time.sleep(1)
con.send("terminal length 0\n")
time.sleep(1)
outp = con.recv(5000)
print  outp
con.send("show version\n")
time.sleep(1)
outp = con.recv(5000)
print  outp
con.send("conf t\n")
time.sleep(1)
con.send("logging buffered 40960\n")
time.sleep(1)
outp = con.recv(5000)
print  outp
