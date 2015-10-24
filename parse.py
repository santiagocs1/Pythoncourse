#!/usr/bin/env python
from ciscoconfparse import CiscoConfParse
configuration= CiscoConfParse("cisco_ipsec.txt")
crypto=configuration.find_objects(r"^crypto map CRYPTO")
for i in crypto:
    print i.children
pfs=configuration.find_objects_w_child(parentspec=r"^crypto map CRYPTO", childspec=r"set pfs group2")
print "now find the pfs"
for i in pfs:
    print i.children
transform=configuration.find_objects_wo_child(parentspec=r"^crypto map CRYPTO", childspec=r"set transform-set AES-SHA")
print "now print transform no AES"
for i in transform:
    print i.children
