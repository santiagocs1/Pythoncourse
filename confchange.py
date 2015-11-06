#!/usr/bin/env python
import pickle
import snmp_helper
import smtplib
from email.mime.text import MIMEText
import email_helper
recipient= 'santiago_cs1@hotmail.com'
subject = 'Change in the configuration'
message = 'there was a change in the router config'
sender= 'anonymous@anonymous'
snmpIP= '50.76.53.27'
snmpPort= 8061
snmpuser= 'pysnmp'
snmpkey= 'galileo1'
snmpdevice= (snmpIP,snmpPort)
snmpuser= (snmpuser,snmpkey,snmpkey)
snmp_data= snmp_helper.snmp_get_oid_v3(snmpdevice, snmpuser, oid='1.3.6.1.4.1.9.9.43.1.1.1.0')
output= snmp_helper.snmp_extract(snmp_data)
print output
f = open("routervalue.pkl", "rb")
currentvalue= pickle.load(f) 
f.close()
compare = int(currentvalue[0])
print compare
if int(output) == compare:
    print "No changes"
else:
    print"there is a change, i will send a mail"
    email_helper.send_mail(recipient, subject, message, sender)
f= open("routervalue.pkl", "wb")
routerlist= []
routerlist.append(output)
pickle.dump(routerlist,f)
f.close()
