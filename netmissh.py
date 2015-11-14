#!/usr/bin/env python
from netmiko import ConnectHandler
from getpass import getpass
passwd=getpass()
pynet1= {
    'device_type': 'cisco_ios',
    'ip': '50.76.53.27',
    'username': 'pyclass',
    'password': passwd,
    }
pynet2= {
    'device_type': 'cisco_ios',
    'ip': '50.76.53.27',
    'username': 'pyclass',
    'password': passwd,
    'port': 8022,
}
juniper_srx= {
    'device_type': 'juniper',
    'ip': '50.76.53.27',
    'username': 'pyclass',
    'password': passwd,
    'port': 9822,
}
pynet_rtr2= ConnectHandler(**pynet2)
pynet_rtr1= ConnectHandler(**pynet1)
pynet_juniper= ConnectHandler(**juniper_srx)
pynet_rtr2.config_mode()
print pynet_rtr2.check_config_mode()
print "sh arp rtr1:\n"
outp=pynet_rtr1.send_command("show arp")
print outp
print "sh arp juniper:\n"
outp=pynet_juniper.send_command("show arp")
print outp
pynet_rtr2.send_command("logging buffered 40960")

    #tim2.sleep(1)
    


