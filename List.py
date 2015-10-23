#!/usr/bin/env python
import yaml
import json
List=[]
List.append("Santiago")
List.append("Castro")
List.append("Learns")
List.append("Python")
List.append({})
List[-1]['nombre']='santiago'
List[-1]['surname']='castro'
with open("YaMLLIST.yml", "w") as f:
    f.write(yaml.dump(List, default_flow_style=True))
with open("JSONLIST.json", "w") as g:
    g.write(json.dumps(List))
    
