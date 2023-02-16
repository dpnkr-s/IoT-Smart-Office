#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from array import *
import paho.mqtt.client as PahoMQTT
import datetime
import time
import sys
import urllib2
from bs4 import BeautifulSoup
import re

ipBroker = "iot.eclipse.org"
portBroker = 1883
# specify the url
quote_page = 'http://www.meteoperugia.altervista.org'
dweet = 'ictbuildingsm'
#https://beta.dweet.io/follow/ictbuildingsm para ver os graficos
#https://beta.dweet.io/dweet/for/ICTFORSMARTBUILDINGSDAN?ddd=5  para enviar dado
quote_page1 ='http://www.comune.torino.it/meteo/'

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
        
    def light(self):
		hora = datetime.datetime.now()
		hora_s=hora.strftime ('%Y-%m-%dT%H:%M:%S+0100')
        # query the website and return the html page
		page = urllib2.urlopen(quote_page)
		page1 = urllib2.urlopen(quote_page1)
		# parse the html using beautiful soap and store in variable soup
		soup  = BeautifulSoup(page, 'html.parser')
		soup1 = BeautifulSoup(page1, 'html.parser')
		# Take out the <div> of name and get its value
		name_box = soup.find_all('marquee') 
		name_box1 = soup1.find_all('em') 
		#name = name_box.text# strip() is used to remove starting and trailing
		#name = name_box.text.strip() # strip() is used to remove starting and trailing
		name= str(name_box)
		name1= str(name_box1)
		
		lux = str(name[560:564])      # esse valor muda conforme horario do site
		temperat = str(name1[29:33])
		lux2=str(re.findall(r'\d+',lux))
		lux3=re.sub(r'[^a-zA-Z0-9 ]',r'',lux2)  #sometimes print wrong values formatation website changes
		if (lux3[0] == '0'):
			lux3=0
		#lux3=lux2[2:4]
		#lux3=lux2[1]
		#print hora
		j_temp = '{"id":"A","sensor": "light","reading":"'+str(lux3)+'", "time":"'+hora_s+'", "temp":"'+temperat+'"}'
		sensorpub = "$ICTFORSMARTBUILDINGSDAN/sensor/%s" % (lux3)
		#self.client.publish(sensorpub);
		self.client.publish(topic, j_temp)
		print j_temp
		#url_tmp = "https://dweet.io:443/dweet/for/ictbuildingsm?SolarRadiation=" +str(lux3) +"&Time=" +hora_s
		#response = urllib2.urlopen(url_tmp)
		#print url_tmp
			
        

topic = "$ICTFORSMARTBUILDINGSDAN/sensor"
lightSensor = Window(1,"A","sensor/")

while True:
    lightSensor.connection(ipBroker, portBroker)
    lightSensor.light()
    time.sleep(15)
