#!/usr/bin/env python
# -*- coding: utf-8 -*-
from array import *
import paho.mqtt.client as mqtt
import json
import time
import random
import urllib2
from pylab import *
from sunposition import sunpos
from datetime import datetime
import math
dweet = 'ictbuildingsm'
d=[]

ipBroker = "iot.eclipse.org"
portBroker = 1883
lat= 45.0538607
lon= 7.672202
angle = 0
AP= 0
S=0

###########################3
#Dweet link to see data    https://dweet.io/follow/ictbuildingsm
#non customized dashboard   https://freeboard.io/board/BR7ENV

    
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("$ICTFORSMARTBUILDINGSDAN/sensor")
        
        
def on_message(client, userdata, msg):
	print "onmessage"
	print(msg.topic+" "+str(msg.payload))
	dict = json.loads(str(msg.payload))
	print dict
	d.append(str(msg.payload)) 
	sensorValue=int(dict["reading"])
	temper = float(dict["temp"])
	#evaluate on a 2 degree grid
	now = datetime.utcnow()
	az,zen = sunpos(now,lat,lon,0)[:2] #discard RA, dec, H
	#convert zenith to elevation
	elev = 90 - zen
	time1=str(dict["time"])
	print sensorValue
	print time1
	dat = datetime.now()
	month=dat.month
	dia=dat.day
	ano=dat.year
	hora=str(dat.hour)+":" + str(dat.minute)
	dataT= (str(dia) + "/"+ str(month) + "/" +str(ano))
	
	
	
	#az, al =  solar.get_position(lat,lon,dat)
	# https://github.com/pingswept/pysolar/blob/master/test/testsolar.py
	#livro https://books.google.it/books?id=cfCqBAAAQBAJ&pg=PA79&lpg=PA79&dq=solar.get_altitude&source=bl&ots=LQyWYzdKUQ&sig=UkD_M0pULGBztwQf__6ezlY8-L4&hl=en&sa=X&ved=0ahUKEwiDya-O6anVAhUCLFAKHdtNAK4Q6AEIPzAE#v=onepage&q&f=false
	#paper http://2012.experiencinglight.nl/doc/40.pdf
	
	#Atmosferic condition  		Radiation
		#	Sereno					900
		#	Nuvoloso				350
		#	Appena  percettibele	200
		#	Nebbia Fitta			100
		#	Coperto					50
		
	if(sensorValue>=350):
		atmosfericC = 'Sereno'
	elif(200 < sensorValue and sensorValue < 350):
		atmosfericC = 'Nuvoloso'
	elif(100 < sensorValue and sensorValue <= 200):
		atmosfericC = 'Appena  percettibele'
	elif(50 < sensorValue and sensorValue <= 100):
		atmosfericC = 'Nebbia Fitta'
	elif(sensorValue <= 50):
		atmosfericC = 'Coperto'
		
	print str(atmosfericC)
	
	 #   Month					shadow area
		#1	january					0-36
		#2	february				0-41
		#3	March					0-47
		#4	April					0-53
		#5	May						0-59
		#6	June					64-100
		#7	July					70-100
		#8	August					62-100
		#9	September				54-100
		#10	October					46-100
		#11	November				38-10
		#12	December				0-30
		
		
		

#colocar um relogio se fora do horario comercial fechar no inverno, abrir no verao
	if(month==1):
		print("January	shadow area 0-36 %")
		#cutt off angle 0 - 32.4degrees
		if(sensorValue<=350):
			angle=0
		elif(sensorValue>=350):
			angle=32.4
	elif(month==2):
		print("February	shadow area 0-41 %")
		#cutt off angle 0 - 36.9degrees
		if(sensorValue<=350):
			angle=0
		elif(sensorValue>=350):
			angle=36
        
	elif(month==3):
		print("March	shadow area 0-47 %")
		#cutt off angle 0 - 42.3degrees
		if(sensorValue<=350):
			angle=0
		elif(sensorValue>=350):
			angle=42.3
           
	elif(month==4):
		print("April	shadow area 0-53 %")
		#cutt off angle 0 - 47.7degrees
		if(sensorValue<=350):
			angle=0
		elif(sensorValue>=350):
			angle=47.70
        
	elif(month==5):
		print("May	shadow area 0-59 %")
		#cutt off angle 0 - 53.1degrees
		if(sensorValue<=350):
			angle=0
		elif(sensorValue>=350):
			angle=53.1
        
	elif(month==6):
		print("June	shadow area 64-100 %")
		#cutt off angle 57.6degrees
		if(sensorValue<=350):
			angle=0
		elif(sensorValue>=350):
			angle=57.6
        
	elif(month==7):
		print("July	shadow area 70-100 %")
		
		#cutt off angle 0 - 63degrees
		if(sensorValue>350):
			angle=0
		elif(sensorValue<=350):
			angle=63
			
		
        
	elif(month==8):
		print("August	shadow area 62-100 %")
		#cutt off angle 55.8degrees
		if(sensorValue<=350):
			angle=0
		elif(sensorValue>=350):
			angle=55.8
			
           
	elif(month==9):
		print("September	shadow area 57-100 %")
		#cutt off angle 51.3degrees
		if(sensorValue<=350):
			angle=0
		elif(sensorValue>=350):
			angle=51.3
        
	elif(month==10):
		print("October	shadow area 46-100 %")
		#cutt off angle 41.4degrees
		if(sensorValue<=350):
			angle=0
		elif(sensorValue>=350):
			angle=41.4
        
	elif(month==11):
		print("November	shadow area 38-100 %")
		#cutt off angle 34.2degrees
		if(sensorValue<=350):
			angle=0
		elif(sensorValue>=350):
			angle=34.2
        
	elif(month==12):
		print("December	shadow area 0-30 %")
		#cutt off angle 0-27degrees
		if(sensorValue<=350):
			angle=0
		elif(sensorValue>=350):
			angle=27
	#######################################################################################		
	# Calculation of profile angle
	
	Wd=5   #orientation of window  5 degrees sud
	W=750  # shutther width
	
	AP = (math.tan(radians(elev))) / (math.cos(radians(az-Wd)))
	########################################################################################
	#http://www.wolframalpha.com/widgets/view.jsp?id=4acbedbe977480d19b7b682d4878cae2
	#A= [((S/W)*cos(B))/(sqrt(1-((S/W)*cos(B))²))]-B
	# Calculate S distance for desired cutoff angle 
	#angle = [(S/W).cos(AP))/ (sqrt(1-((S/W).cos(AP))²))]-AP
	S = (W*(angle+AP)*(1/cos(radians(AP))))/(math.sqrt((angle*angle) + (2*angle*AP)+(AP*AP))+1)
	########################################################################################
	print elev
	print az
	print AP
	print S
	########################################################################################
	
	###########
	#error on  total lenght of url_tmp
		
	#url_tmp = "https://dweet.io:443/dweet/for/ictbuildingsm?weather=" +atmosfericC +"&data=" +dataT +"&hora="+hora +"&SolarRad=" +str(sensorValue)+"&SunElev=" +str(elev) +"&SunAZ=" +str(az) +"&Temp=" +str(temper) +"&angle=" +str(angle) +"&ProfAngle=" +str(AP) 
	#
	#+"&data=" +dataT +"&hora="+hora +"&SolarRad=" +str(sensorValue)+"&SunElev=" +str(elev) +"&SunAZ=" +str(az) +"&Temp=" +str(temper) +"&angle=" +str(angle) +"&ProfAngle=" +str(AP)  
	url_tmp ="https://dweet.io:443/dweet/for/ictbuildingsm?" +"data=" +dataT +"&hora="+hora +"&SolarRad=" +str(sensorValue)+"&SunElev=" +str(elev) +"&SunAZ=" +str(az) +"&Temp=" +str(temper) +"&angle=" +str(angle) +"&ProfAngle=" +str(AP) 
	response = urllib2.urlopen(url_tmp)
	cont= '{"controler": "shutter","control":"' +str(AP)+ '", "time":"'+hora+'"}'
	client.publish("$ICTFORSMARTBUILDINGSDAN/control", cont)
	
	print url_tmp
	print angle

def on_publish(self, attuatorControl, obj, mid):
	print("mid: "+str(mid))
	topic = "$ICTFORSMARTBUILDINGSDAN/control"
	self.client.publish(topic, 'aaa')
        
def on_subscribe(self, attuatorControl, obj, mid, granted_qos):
	print "on_subscribe"
	print("Subscribed: "+str(mid)+" "+str(granted_qos))
        
def on_log(self, attuatorControl, obj, level, string):
	print(string)
    
 

def run(self,ip,port):
	self.client.connect(ipBroker,portBroker,60)
	print "entrou no run"
	self.client.subscribe("$ICTFORSMARTBUILDINGSDAN/sensor", qos=2)
	
	
        
	rc=0
	while rc == 0:
		rc = self.client.loop()
		print"loop"
	return rc


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(ipBroker,portBroker,60)
client.loop_forever()

