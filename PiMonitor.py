import os
import sys
import urllib
import urllib2
import time
import psutil
from subprocess import *

def GetLANIP():
   cmd = "ip addr show eth0 | grep inet  | grep -v inet6 | awk '{print $2}' | cut -d '/' -f 1"
   p = Popen(cmd, shell=True, stdout=PIPE)
   output = p.communicate()[0]
   return output

def GetWLANIP():
   cmd = "ip addr show wlan0 | grep inet  | grep -v inet6 | awk '{print $2}' | cut -d '/' -f 1"
   p = Popen(cmd, shell=True, stdout=PIPE)
   output = p.communicate()[0]
   return output


def GetTemp():
    cmd = "/opt/vc/bin/vcgencmd measure_temp | sed -s 's/=/:/g'"
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.replace('\n','').replace('temp:','').replace("'C","c")


def GetFreeMem():
    return str(psutil.virtual_memory().free/1024/1024) + "M"

def GetCpuPercent():
    return str(psutil.cpu_percent()) + "%"

def GetFreeDisk():
    return str(psutil.disk_usage('/home/pi').free/1024/1024) + "M"

def PublishToDisplay(text,label_prefix):
    try:
      data = {}
      data['p'] = '0'
      data['n'] = label_prefix + sys.argv[2]
      data['v'] = text
      data['fc'] = '23555'
      url_values = urllib.urlencode(data)
      #url = "http://" + sys.argv[1] + "/TextSetText?p=0&n=" + sys.argv[2] + "&v=" + text + "&fc=12345"
      url = "http://" + sys.argv[1] + "/TextSetText?" + url_values
      # Below is sync mode, switchd to async
      # print(url)
      response = urllib2.urlopen(url)
      html = response.read()
    except:
      pass


while(True):
    tempst = GetTemp()
    PublishToDisplay(tempst,"temp")
    cpupercent = GetCpuPercent()
    PublishToDisplay(cpupercent,"cpu")
    freemem = GetFreeMem()
    PublishToDisplay(freemem,"mem")
    freedisk = GetFreeDisk()
    PublishToDisplay(freedisk,"disk")

    ip = GetLANIP()
    
    if(ip == ""):
        PublishToDisplay(GetWLANIP(),"ip")
    else:
        PublishToDisplay(ip,"ip")
    
    
    time.sleep(10)
