  #!/usr/bin/env python
# -*- coding: utf-8 -*- 
from array import *
import paho.mqtt.client as PahoMQTT
from datetime import datetime
import time
import sys
import urllib2
import re
import csv
#ipBroker = "iot.eclipse.org"
ipBroker = "172.22.53.2"
portBroker = 1883

dweet = 'ictbuildingsm'
now = datetime.utcnow()
dat = datetime.now()

class Window:
    
    def __init__(self, sid,name,s_type):
        self.name = name
        self.id = sid
        self.s_type = s_type
    
    def connection(self, ipBroker, portBroker):
		print "def connection"
	
		self.client = PahoMQTT.Client()
		self.client.connect(ipBroker,portBroker)
		self.client.loop(1)
        
    def presence(self):
		hora=dat.hour
		if(hora>= 9 and hora <= 18):
			ts = (dat.hour * 60 + dat.minute)-(9*60) 
			print ts
			z1 = open("presence.csv", "r").readlines()[ts].split(",")[1]
			z2 = open("presence.csv", "r").readlines()[ts].split(",")[2]
			z3 = open("presence.csv", "r").readlines()[ts].split(",")[3]
			z4 = open("presence.csv", "r").readlines()[ts].split(",")[4]
			z5 = open("presence.csv", "r").readlines()[ts].split(",")[5]
			z6 = open("presence.csv", "r").readlines()[ts].split(",")[6]
			z7 = open("presence.csv", "r").readlines()[ts].split(",")[7]
			z8 = open("presence.csv", "r").readlines()[ts].split(",")[8]
			z9 = open("presence.csv", "r").readlines()[ts].split(",")[9]
			pres = '{"id":"A","sensor": "presence","time": "'+str(ts)+'", "z1":"'+str(z1)+'", "z2":"'+str(z2)+'", "z3":"'+str(z3)+'", "z4":"'+str(z4)+'", "z5":"'+str(z5)+'", "z6":"'+str(z6)+'", "z7":"'+str(z7)+'", "z8":"'+str(z8)+'"}'
			#, "zone3":"'+str(zone3)+'","zone4":"'+str(zone4)+'", "zone5":"'+str(zone5)+'", "zone6":"'+str(zone6)+'", "zone7":"'+str(zone7)+'", "zone8":"'+str(zone8)+'", "zone9":"'+str(zone9)+'"
			#sensorpub = "$ICTFORSMARTBUILDINGSDAN/sensor/%s" % (lux3)
			#self.client.publish(sensorpub);
			self.client.publish(topic, pres)
			print pres
			url_tmp = "https://dweet.io:443/dweet/for/ictbuildingsm?zone1=" +str(z1) +"&zone2=" +str(z2)+"&zone3=" +str(z3)+"&zone4=" +str(z4)+"&zone5=" +str(z5)+"&zone6=" +str(z6)+"&zone7=" +str(z7)+"&zone8=" +str(z8)+"&zone9=" +str(z9)
			response = urllib2.urlopen(url_tmp)
			print url_tmp
			
        

topic = "$ICTFORSMARTBUILDINGSDAN/sensor"
lightSensor = Window(1,"A","sensor/")

while True:
    lightSensor.connection(ipBroker, portBroker)
    lightSensor.presence()
    time.sleep(20)
