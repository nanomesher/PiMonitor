import os
import sys
import urllib
import urllib2
import time
import psutil
from subprocess import *

def GetTemp():
    #cmd = "sudo wifi scan"
    cmd = "/opt/vc/bin/vcgencmd measure_temp | sed -s 's/=/:/g'"
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.replace('\n','').replace('temp:','Temp:').replace("'C","c")

def GetMem():
    #cmd = "sudo wifi scan"
    cmd = "cat /proc/meminfo | grep MemFree | sed -s 's/ //g'"
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.replace('\n','')

def GetFreeMem():
    return "Free:" + str(psutil.virtual_memory().free/1024/1024) + "M"

def GetCpuPercent():
    return "CPU:" + str(psutil.cpu_percent()) + "%"

def PublishToDisplay(text):
      data = {}
      data['p'] = '0'
      data['n'] = sys.argv[2]
      data['v'] = text
      data['fc'] = '12345'
      url_values = urllib.urlencode(data)
      #url = "http://" + sys.argv[1] + "/TextSetText?p=0&n=" + sys.argv[2] + "&v=" + text + "&fc=12345"
      url = "http://" + sys.argv[1] + "/TextSetText?" + url_values
      # Below is sync mode, switchd to async
      # print(url)
      response = urllib2.urlopen(url)
      html = response.read()
      


while(True):
    tempst = GetTemp()
    PublishToDisplay(tempst)
    time.sleep(10)
    cpupercent = GetCpuPercent() + " " + GetFreeMem()
    PublishToDisplay(cpupercent)
    time.sleep(10)
