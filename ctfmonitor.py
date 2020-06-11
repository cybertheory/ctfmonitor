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
   reset = '10'
   helpstr = 'python ctfmonitor.py -u <CTFmachine> -f <openvpn config file> -r <number of pings till reset (default 10)> -h <help>\nMAKE SURE TO RUN AS ADMIN OR WITH SUDO' 
   if len(argv) == 0:
      print(helpstr)
      sys.exit(2)
   try:
      opts, args = getopt.getopt(argv,"u:f:h:r")
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
      elif opt == '-r':
          try:
              reset = int(arg)
          except:
              print("reset argument too large")
              sys.exit(2)
   return host,openvpn, reset

if __name__ == "__main__":
   host, openvpn, reset= filterargs(sys.argv[1:])
   if len(openvpn) != 0:
       if subprocess.call('openvpn ' + openvpn, stdout=FNULL) == 0:
           print("Openvpn connection successful")
   count = 0
   received = 0
   print("Connecting to " + host + " *loss cache will reset every " + reset + " pings*")
   time.sleep(5)
   while(1):
       if count == reset:
           count = 0
           received = 0
       if ping(host):
           count += 1
           received += 1
           loss=(count-received)/count
           if loss == 0:
               clear()
               print("Connection at no loss [||||||||||||||||||||||||||||||||]")
           elif loss == 1.0:
               clear()
               print("No Connection No Connection No Connection No Connection")
           else:
               clear()
               print("Connection at some loss: " + str(round(loss,2)))
       else:
           count += 1
           loss=(count-received)/count
           clear()
           if loss == 1.0:
               clear()
               print("No Connection No Connection No Connection No Connection")
           else:
               clear()
               print("Connection at some loss: " + str(round(loss,2)))
       time.sleep(1)