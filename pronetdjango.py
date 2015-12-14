#!/usr/bin/env python
from netmiko import ConnectHandler
from getpass import getpass
from datetime import datetime
from net_system.models import NetworkDevice, Credentials
import django
import threading
from multiprocessing import Process, current_process

def show_ver(i):
    device_type=i.device_type
    port=i.port
    secret=''
    ip=i.ip_address
    creds=i.credentials
    username=creds.username
    password=creds.password
    remote= ConnectHandler(device_type=device_type, ip=ip, username=username, password=password, port=port)
    print remote.send_command("show version")

def main():
    django.setup()
    start_time = datetime.now()
    devices = NetworkDevice.objects.all()
    procs = []
    for i in devices:
        proc = Process(target=show_ver, args=(i,))
        proc.start()
        procs.append(proc)
    
    for a_proc in procs:
        a_proc.join()
if __name__ == "__main__":
    main()
