IP=`ifconfig wlan3 | fgrep 'inet addr' |  awk -F: '{print $2}' | awk '{print $1}'`
sudo python proxy.py --proxy-host $IP --if wlan3 --client-host $IP
# sudo python proxy.py --proxy-host $IP --if wlan3 

#usage: proxy.py [-h] [--if INTERFACE] [--proto PROTO] [--proxy-port PPORT]
#                [--proxy-host PHOST] [--client-port CPORT]
#                [--client-host CHOST] [--repeat REPEAT] [--delay DELAY]
#
#Chorus!
#
#optional arguments:
#  -h, --help           show this help message and exit
#  --if INTERFACE       Interface
#  --proto PROTO        Protocol
#  --proxy-port PPORT   Listen Port
#  --proxy-host PHOST   Listen Host
#  --client-port CPORT  Client Port
#  --client-host CHOST  Client Host
#  --repeat REPEAT      Repeats
#  --delay DELAY        Delay
