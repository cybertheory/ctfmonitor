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
import atexit
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
      opts, args = getopt.getopt(argv,"u:f:r:h")
   except getopt.GetoptError as err:
      print(helpstr)
      print(err)
      sys.exit(2)
   if '-u' not in opts[0]:
       print("\n\n*No CTF IP or DNS provided*\n\n")
       print(helpstr)
       sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print(helpstr)
         sys.exit(2)
      elif opt == '-u':
         host = arg
      elif opt == '-f':
         if '.ovpn' in arg:
             openvpn = arg
         else:
             print("Invalid Openvpn Config file (not .ovpn)")
      elif opt == '-r':
          try:
              reset = int(arg)
          except:
              print("\n\n*reset argument too large*\n\n")
              sys.exit(2)
   return host,openvpn, reset

if __name__ == "__main__":
   host, openvpn, reset= filterargs(sys.argv[1:])
   if len(openvpn) != 0:
       FNULL = open(os.devnull, 'w')
       if subprocess.call('openvpn ' + openvpn, shell=True,stdout=FNULL) == 0:
           if platform.system().lower()=='windows':
               atexit.register(os.system,'tkill openvpn')
           else:
               atexit.register(os.system,'pkill openvpn')
           print("\n\nopenvpn connected!\n\n")
       else:
           print('\n\n ***COULD NOT FIND OPENVPN*** \n\n')
   count = 0
   received = 0
   print("Connecting to " + host + " *loss cache will reset every " + str(reset) + " pings*")
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