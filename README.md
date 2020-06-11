# ctfmonitor
A simple tool that allows you to monitor your connection to CTF challenges, it can also connect you to an openvpn network! If you want to end the connection simply ^c the monitor.

## Features
- Minimally Invasive (sends ping slowly 1 per second)
- Cache Resets (resets recieved and total pings every 10 pings by default - can be changed): This allows for more accurate and sensitive monitoring
- Allows you to start an open vpn connection
- Output Fits in one line (small TMUX/Terminator pane will be all you need)

## Useage
***
python ctfmonitor.py -u <CTFmachine> -f <openvpn config file> -r <number of pings till reset (default 10)> -h <help>
MAKE SURE TO RUN AS ADMIN OR WITH SUDO
***

## Install (just download the python script supports Windows and Linux (maybe MacOS no testing done))
