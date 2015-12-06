#!/usr/bin/env python
import pyeapi
sw3 = pyeapi.connect_to("pynet-sw2")
sw_enable = sw3.enable("show interfaces")
sw_enable1 = sw_enable[0]
sw_enable2 = sw_enable1['result']
sw_enable3 = sw_enable2['interfaces']
for i in sw_enable3:
    if 'interfaceCounters' in sw_enable3[i]:
        print i
        print sw_enable3[i]['interfaceCounters']['inOctets']
        print sw_enable3[i]['interfaceCounters']['outOctets']
