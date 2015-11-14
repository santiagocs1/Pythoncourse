#!/usr/bin/env python
import time
import pexpect
from getpass import getpass
import re
def main():
    ip='50.76.53.27'
    port=8022
    username= 'pyclass'
    passw= getpass()
    conn= pexpect.spawn('ssh -l {} {} -p {}'.format(username,ip,port))
    conn.timeout = 6
    conn.expect('ssword:')
    conn.sendline(passw)
    conn.expect('#')
    print conn.before
    conn.sendline('show ip int brief')
    conn.expect('pynet-rtr2')
    print conn.before
    conn.sendline('conf t')
    conn.sendline('loggin buffered 409600')
    conn.sendline('end')
    conn.expect('pynet-rtr2#')
    conn.sendline(' show run | sec buffe')
    conn.expect('pynet-rtr2')
    print conn.before
    pattern = re.compile(r'.*buffe.*$', re.MULTILINE)
    conn.sendline('show run')
    conn.expect(pattern)
    print conn.after
if __name__ == "__main__":
    main()
