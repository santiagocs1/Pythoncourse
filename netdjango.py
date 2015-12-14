#!/usr/bin/env python
from netmiko import ConnectHandler
from getpass import getpass
from datetime import datetime
from net_system.models import NetworkDevice, Credentials
import django
import threading    

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
    for i in devices:
        thread = threading.Thread(target=show_ver, args=(i,))
        thread.start()
    main_tread = threading.currentThread()
    for some_thread in threadin.enumerate():
        if some_thread != main_tread:
            some_thread.join()
    
if __name__ == "__main__":
    main()
