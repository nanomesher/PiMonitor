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
    return psutil.virtual_memory().free/1024/1024

def GetCpuPercent():
    return str(psutil.cpu_percent()) + "%"

def GetFreeDisk():
    return psutil.disk_usage('/home/pi').free/1024/1024

def LedOn():
    try:
      
      url = "http://" + sys.argv[1] + "/LedOn"
      response = urllib2.urlopen(url)
      html = response.read()
    except:
      pass

def LedOff():
    try:
      
      url = "http://" + sys.argv[1] + "/LedOff"
      response = urllib2.urlopen(url)
      html = response.read()
    except:
      pass


def PublishToDisplay(text,label_prefix,color):
    try:
      data = {}
      data['p'] = '0'
      data['n'] = label_prefix + sys.argv[2]
      data['v'] = text
      data['fc'] = color
      url_values = urllib.urlencode(data)
      url = "http://" + sys.argv[1] + "/TextSetText?" + url_values
      response = urllib2.urlopen(url)
      html = response.read()
    except:
      pass


while(True):
    tempst = GetTemp()
    PublishToDisplay(tempst,"temp","23555")
    cpupercent = GetCpuPercent()
    PublishToDisplay(cpupercent,"cpu","23555")

    freemem = GetFreeMem()

    if(freemem > 100):
       PublishToDisplay(str(freemem) + "M","mem","23555")
       LedOff()
    else:
       PublishToDisplay(str(freemem) + "M","mem","61455")
       LedOn()
       
    freedisk = GetFreeDisk()

    if(freedisk > 500):
       PublishToDisplay(str(freedisk) + "M","disk","23555")
       LedOff()
    else:
       PublishToDisplay(str(freedisk) + "M","disk","61455")
       LedOn()

    if(freemem > 100 and freedisk > 500):
       LedOff()
    else:
       LedOn()

   

    ip = GetLANIP()
    
    if(ip == ""):
        PublishToDisplay(GetWLANIP(),"ip","23555")
    else:
        PublishToDisplay(ip,"ip","23555")
    
    
    time.sleep(10)
