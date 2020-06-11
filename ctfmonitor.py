# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 10:40:44 2020

@author: risha
"""

import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import sys
import getopt
import os
import time

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    FNULL = open(os.devnull, 'w')
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command, stdout=FNULL) == 0

def clear():
    if platform.system().lower()=='windows':
        os.system( 'cls' )
    else:
        os.system('clear')
        
def filterargs(argv):    
   openvpn = ''
   host = ''
   helpstr = 'python ctfmonitor.py -u <CTFmachine> -f <openvpn config file> -h <help>' 
   if len(argv) == 0:
      print(helpstr)
      sys.exit(2)
   try:
      opts, args = getopt.getopt(argv,"u:f:h")
   except getopt.GetoptError as err:
      print(err)
      print(helpstr)
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print(helpstr)
         sys.exit()
      elif opt == '-u':
         host = arg
      elif opt == '-f':
         openvpn = arg
   return host,openvpn 

if __name__ == "__main__":
   host, openvpn= filterargs(sys.argv[1:])
   count = 0
   received = 0
   print("Connecting to " + host)
   time.sleep(2)
   while(1):
       if ping(host):
           count += 1
           received += 1
           loss=(count-received)/count
           if loss == 0:
               clear()
               print("Connection Strong")
           else:
               clear()
               print("Packet Loss: " + str(loss))
       else:
           count += 1
           loss=(count-received)/count
           clear()
           print("Packet Loss: " + str(loss))
       time.sleep(1)