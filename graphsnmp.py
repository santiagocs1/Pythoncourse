#!/usr/bin/env python
import snmp_helper
import smtplib
import pygal
f4_in_octects = [5269, 5011, 6705, 5987, 5011, 5071, 6451, 5011, 6181, 5281, 5011,5011]
f4_out_octets = [5725, 5783, 7670, 6783, 5398, 5783, 9219, 3402, 5783, 6953, 5668, 5011]
f4_in_packets = [ 24, 21, 40, 32, 21, 21, 49, 54, 21, 34, 34, 32]
f4_out_packets = [ 25, 21, 40, 23, 21, 23, 49, 12, 25, 56, 34, 34]
chart1= pygal.Line()
chart2= pygal.Line()
chart1.title = 'Input/Ouput Octets'
chart1.x_labels = [ '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60']
chart1.add( 'InOctets', f4_in_octects)
chart1.add('OutOctets', f4_out_octets)
chart1.render_to_file('octets.avg')
chart2.title = 'Input/Ouput Packets'
chart2.x_labels = [ '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60']
chart2.add( 'InOctets', f4_in_packets)
chart2.add('OutOctets', f4_out_packets)
chart2.render_to_file('packets.avg')

