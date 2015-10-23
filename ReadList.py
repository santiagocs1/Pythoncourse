#!/usr/bin/env python
import yaml
import json
List=[]
List2=[]





with open("YaMLLIST.yml") as f:
    List=yaml.load(f)
    for i in List:
        print i
with open("JSONLIST.json") as g:
    List2=json.load(g)
    for i in List2:
        print i
