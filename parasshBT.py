#!/usr/bin/env python
import paramiko
import time

def scrip(remote_conn):
    remote_conn.send(cmd + '\n')
    time.sleep(1) 

def main():
devices=[]
port = 22
passw= 'xxxx'
for i in devices:
    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(i, username='608313687', password=passw, look_for_keys=False, allow_agent=False, port=port)
    remote_conn= connection.invoke_shell()
    time.sleep(1)
    script(remote_conn)

if __name__ == "__main__":
    main()

