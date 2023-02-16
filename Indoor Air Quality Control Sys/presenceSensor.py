#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from array import *
import paho.mqtt.client as PahoMQTT
from datetime import datetime
import time
import sys
import urllib2
from bs4 import BeautifulSoup
import re
import csv
quote_page1 ='http://www.comune.torino.it/meteo/'
#ipBroker = "172.21.42.175"
ipBroker = "iot.eclipse.org"
portBroker = 1883
dweet = 'ventlab'
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
    '''
    def temp_out(self):
		
		
        # query the website and return the html page
		page1 = urllib2.urlopen(quote_page1)
		# parse the html using beautiful soap and store in variable soup
		soup1 = BeautifulSoup(page1, 'html.parser')
		# Take out the <div> of name and get its value
		
		#name = name_box.text# strip() is used to remove starting and trailing
		#name = name_box.text.strip() # strip() is used to remove starting and trailing
		name_box1 = soup1.find_all('em')
		name1= str(name_box1)
		# esse valor muda conforme horario do site
		temperat = str(name1[29:33])
		#print hora
		j_temp = '{"id":"A","sensor": "temp", "temp":"'+temperat+'"}'
		#self.client.publish(sensorpub);
		self.client.publish(topic, j_temp)
		print j_temp
		#url_tmp = "https://dweet.io:443/dweet/for/ictbuildingsm?SolarRadiation=" +str(lux3) +"&Time=" +hora_s
		#response = urllib2.urlopen(url_tmp)
		#print url_tmp    '''
    
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
			npeople=int(z1)+int(z2)+int(z3)+int(z4)+int(z5)+int(z6)+int(z7)+int(z8)+int(z9)
			pres = '{"id":"A","sensor": "presence","time": "'+str(ts)+'", "z1":"'+str(z1)+'", "z2":"'+str(z2)+'", "z3":"'+str(z3)+'", "z4":"'+str(z4)+'", "z5":"'+str(z5)+'", "z6":"'+str(z6)+'", "z7":"'+str(z7)+'", "z8":"'+str(z8)+'", "z9":"'+str(z9)+'" "npeople":"'+str(npeople)+'"}'
			#, "zone3":"'+str(zone3)+'","zone4":"'+str(zone4)+'", "zone5":"'+str(zone5)+'", "zone6":"'+str(zone6)+'", "zone7":"'+str(zone7)+'", "zone8":"'+str(zone8)+'", "zone9":"'+str(zone9)+'"
			#sensorpub = "$ICTFORSMARTBUILDINGSDAN/sensor/%s" % (lux3)
			#self.client.publish(sensorpub);
			self.client.publish(topic, pres)
			print pres
			#url_tmp = "https://dweet.io:443/dweet/for/ventlab?zone1=" +str(z1) +"&zone2=" +str(z2)+"&zone3=" +str(z3)+"&zone4=" +str(z4)+"&zone5=" +str(z5)+"&zone6=" +str(z6)+"&zone7=" +str(z7)+"&zone8=" +str(z8)+"&zone9=" +str(z9)+"&npeople=" +str(npeople)
			#response = urllib2.urlopen(url_tmp)
			#print url_tmp
			
        

topic = "$ICTFORSMARTBUILDINGSDAN/sensor"
lightSensor = Window(1,"A","sensor/")

while True:
    lightSensor.connection(ipBroker, portBroker)
    lightSensor.presence()
    #lightSensor.temp_out()
    time.sleep(5)
