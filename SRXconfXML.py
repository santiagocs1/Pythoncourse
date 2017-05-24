#!/usr/bin/python
import xmltodict
import netmiko

def safe_raw_input(type_cast, banner):
  is_valid=0
  while not is_valid :
    try :
      choice=type_cast(raw_input(banner))
      is_valid=1
    except ValueError, e :
      print "is not a valid integer"
  return choice

def getrealip(dic, destination):
  real="NOTFOUND"
  if 'nat' in dic['rpc-reply']['configuration']['security'].keys():
    for i in dic['rpc-reply']['configuration']['security']['nat']['destination']['pool']:
      if destination==i['name']:
        real=i['address']['ipaddr']
  return real

def checkifnat(dic , destination):
  real="NONAT"
  if 'nat' in dic['rpc-reply']['configuration']['security'].keys():
    for i in dic['rpc-reply']['configuration']['security']['nat']['destination']['rule-set']['rule']:
      if i['dest-nat-rule-match']['destination-address']['dst-addr']==destination:
        if 'off' not in i['then']['destination-nat'].keys():
          real=i['then']['destination-nat']['pool']['pool-name']
        else:
          real="NATOFF"
  return real

def getaliasip(dic , destination):
  real=[]
  for i in dic['rpc-reply']['configuration']['security']['zones']['security-zone']:
    if 'address-book' in i.keys():
      for j in i['address-book']['address']:
        if 'ip-prefix' in j.keys():
          if j['ip-prefix']==destination:
            real.append(j['name'])
        else:
          if j['dns-name']['name']==destination:
            real.append(j['name'])
      if 'address-set' in i['address-book'].keys():
        for j in i['address-book']['address-set']:
          if type(j['address'])==type([]):
            for x in j['address']:
              if x['name'] in real:
                real.append(j['name'])
          else:
            if j['address']['name'] in real:
              real.append(j['name'])
  return real

def checkpolicy(dic, source , destination, app):
  policy=[]
  for m in destination:
    dest=checkifnat(dic , m)
    if dest=="NONAT" or dest=="NATOFF":
      dest=m
    else:
      dest=getrealip(dic, dest)
    aliasD=getaliasip(dic , dest)
    for n in source:
      aliasS=getaliasip(dic , n)
      if not aliasD:
        print "Destination IP has been not found in any rule"
      else:
        for i in aliasD:
          if type(mydict['rpc-reply']['configuration']['security']['policies']['policy']['policy'])==type([]):
            for j in mydict['rpc-reply']['configuration']['security']['policies']['policy']['policy']:
              if i in j['match']['destination-address'] or 'any' in j['match']['destination-address']:
                for h in aliasS:
                  if h in j['match']['source-address'] or 'any' in j['match']['source-address']:
                    print "Source: %s and Destination: %s Included in policy %s \n the full policy is: %s \n" % (h, i, j['name'], j)		 	
          else:
            if i in mydict['rpc-reply']['configuration']['security']['policies']['policy']['policy']['match']['destination-address'] or 'any' in mydict['rpc-reply']['configuration']['security']['policies']['policy']['policy']['match']['destination-address']:
              for h in aliasS:
                if h in mydict['rpc-reply']['configuration']['security']['policies']['policy']['policy']['match']['source-address'] or 'any' in mydict['rpc-reply']['configuration']['security']['policies']['policy']['policy']['match']['source-address']:
                  print "Source: %s and Destination: %s Included in Policy: %s \n The fullpolicy is: %s \n" % (h, i, mydict['rpc-reply']['configuration']['security']['policies']['policy']['policy']['name'], mydict['rpc-reply']['configuration']['security']['policies']['policy']['policy'])


def execute_command(net_connect, cmd, ret_parsed_xml=True):
  output=net_connect.send_command(cmd)
  if ret_parsed_xml:
    return xmltodict.parse(output)
  return output

def get_policy_and_zones(net_connect, sourceadd, destadd):
  dic = execute_command(net_connect, "show route %s | display xml" % destadd[0].split('/')[0])
  dstzone=dic['rpc-reply']['route-information']['route-table']['rt']['rt-entry']['nh']['via']
  out=str(execute_command(net_connect,
                          "show configuration security zones | match %s | display set" % dstzone,
                          ret_parsed_xml=False)).split()
  dstzone=ou[(ou.index('security-zone') + 1)]
  dic = execute_command(net_connect, "show route %s | display xml" % sourceadd[0].split('/')[0])
  srczone=dic['rpc-reply']['route-information']['route-table']['rt']['rt-entry']['nh']['via']
  out=str(execute_command(net_connect,
                          "show configuration security zones | match %s | display set" % srczone,
                          ret_parsed_xml=False)).split()
  srczone=ou[(ou.index('security-zone') + 1)]
  policyname="Policy_from_" + str(sourceadd[0]) + "_to_" + str(destadd[0])
  return [policyname, srczone, dstzone]

def main_check_policy(net_connect):
  sourceadd = destadd = application = []
  choice = safe_raw_input(int, "How many Source Addresses? specify number ")
  for i in range(0,choice):
    sourceadd.append(str(raw_input("What is the Source Adress? insert one by one ")))
  choice = safe_raw_input(int, "How many destination Addresses? specify number ")
  for i in range(0,choice):
    destadd.append(str(raw_input("What is the Destination Adress? insert one by one ")))
  is_valid=0
  mydict = execute_command(net_connect, "show configuration | display xml")
  checkpolicy(mydict , sourceadd , destadd , application)


def main_generate_policy(net_connect):
  sourceadd = destadd = application = []
  choice = safe_raw_input(int, "How many Source Addresses? specify number ")
  for i in range(0,choice):
    sourceadd.append(str(raw_input("What is the Source Adress? insert one by one ")))
  natchoice = safe_raw_input(int, "Do you need to implement destination NAT? specify the number: 1-YES || 2-NO ")
  if natchoice==1:
    natdstadd = []
    choice = safe_raw_input(int, "How many NAT destination Addresses? specify number ")
    for i in range(0,choice):
      natdstadd.append(str(raw_input("What is the NAT Destination Address? insert one by one ")))
  choice = safe_raw_input(int, "How many Private destination Addresses? specify number ")
  for i in range(0,choice):
    destadd.append(str(raw_input("What is the Destination Address? insert one by one ")))
  choice = safe_raw_input(int, "How many Applications for the new rule? specify number ")
  for i in range(0,choice):
    application.append(str(raw_input("What is the Application Name? insert one by one ")))
  print "We will first check if there is already available rules with this combination source/destination\n"
  mydict = execute_command(net_connect, "show configuration | display xml")
  checkpolicy(mydict , sourceadd , destadd , application)
  print "And this is the rule suggested \n"
  if natchoice==1:
    for i in natdstadd:
      NAT=checkifnat(mydict , i)
      if NAT=="NONAT":
        natrule="NAT_to_" + i
        print "set security nat destination pool %s address %s \n" % (destadd[natdstadd.index(i)],destadd[natdstadd.index(i)])
        sourceaddnat=""
        for h in sourceadd:
          sourceaddnat=sourceaddnat + " " + h
        print "set security nat destination rule-set XXXX rule %s match source-address %s \n" % (natrule , sourceaddnat)
        print "set security nat destination rule-set XXXX rule %s match destination-address %s \n" % (natrule , i)
        print "set security nat destination rule-set XXXX rule %s then destination-nat pool %s \n" % (natrule , destadd[natdstadd.index(i)])
      else:
        print "There is already a NAT rule for: %s this is: %s \n" % (i , NAT)
      policyname, srczone, dstzone = get_policy_and_zones(net_connect, sourceadd, destadd)
      for i in sourceadd:
        print "set security policies from-zone %s to-zone %s policy %s match source-address %s \n" % (srczone , dstzone , policyname, i)
      for i in destadd:
        print "set security policies from-zone %s to-zone %s policy %s match destination-address %s \n" % (srczone , dstzone , policyname, i)
      for i in application:
        print "set security policies from-zone %s to-zone %s policy %s match application %s \n" % (srczone , dstzone , policyname, i)
      print "set security policies from-zone %s to-zone %s policy %s then permit \n" % (srczone , dstzone, policyname)
  else:
    policyname, srczone, dstzone = get_policy_and_zones(net_connect, sourceadd, destadd)
    for i in sourceadd:
      print "set security policies from-zone %s to-zone %s policy %s match source-address %s \n" % (srczone , dstzone , policyname, i)
    for i in destadd:
      print "set security policies from-zone %s to-zone %s policy %s match destination-address %s \n" % (srczone , dstzone , policyname, i)
    for i in application:
      print "set security policies from-zone %s to-zone %s policy %s match application %s \n" % (srczone , dstzone , policyname, i)
    print "set security policies from-zone %s to-zone %s policy %s then permit \n" % (srczone , dstzone, policyname)


juniper_srx = {
    'device_type': 'juniper',
    'ip':   '10.234.160.241',
    'username': 'root',
    'password': 'BsoCisco0',
  }
try:
  net_connect = netmiko.ConnectHandler(**juniper_srx)
  options = { 1 : main_check_policy,
              2 : main_generate_policy }
  option = safe_raw_input(int, "Specify the Action 1-Check if a flow is allowed || 2-Generate a new Policy ")
  options[option](net_connect)
except KeyError, e:
  print "Please give a good option number."
except netmiko.ssh_exception.NetMikoAuthenticationException, e:
  print "Authentication Error. Please check username/password."
except netmiko.ssh_exception.NetMikoTimeoutException, e:
  print "SSH timeout, please check flow, ip or host."
except ValueError, e:
  print e
except:
  print "An error has occured."
finally:
  if (('net_connect' in locals()) and
     (isinstance(net_connect, netmiko.juniper.juniper_ssh.JuniperSSH))):
    net_connect.disconnect()
