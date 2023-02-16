#!/usr/bin/env python
# -*- coding: utf-8 -*-
from array import *
import paho.mqtt.client as mqtt
import json
import time
import random
import urllib2
from stimator import stima
from pres import pre
from pylab import *
from datetime import datetime
import math
from datetime import date
import calendar
d=[]
dweet = 'ictbuildingsl'
d1=[0]
d2=[0]
d3=[0]
d4=[0]
d5=[0]
d6=[0]
d7=[0]
d8=[0]
d9=[0]



#ipBroker = "iot.eclipse.org"
ipBroker = "172.22.53.2"
portBroker = 1883
my_date = date.today()
day=str(calendar.day_name[my_date.weekday()])


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("$ICTFORSMARTBUILDINGSDAN/sensor")

def on_message(client, userdata, msg):
	print "onmessage"
	print day
	print(msg.topic+" "+str(msg.payload))
	dict = json.loads(str(msg.payload))
	print dict
	d.append(str(msg.payload)) 
	now = datetime.utcnow()
	dat = datetime.now()
	hora=dat.hour
	print "hora %s" %hora
	zn1=int(dict["z1"])
	zn2=int(dict["z2"])
	zn3=int(dict["z3"])
	zn4=int(dict["z4"])
	zn5=int(dict["z5"])
	zn6=int(dict["z6"])
	zn7=int(dict["z7"])
	zn8=int(dict["z8"])
	#zn9=int(dict["z9"])
	d1.append(zn1)
	d2.append(zn2)
	d3.append(zn3)
	d4.append(zn4)
	d5.append(zn5)
	d6.append(zn6)
	d7.append(zn7)
	d8.append(zn8)
	zn9=0
	d9.append(zn9)
	ts = int(dict["time"])
	#evaluate on a 2 degree grid
	pres = pre(ts)
	
	if(hora>= 9 and hora <= 18):
		month=dat.month
		dia=dat.day
		ano=dat.year
		hora=str(dat.hour)+":" + str(dat.minute)
		dataT= (str(dia) + "/"+ str(month) + "/" +str(ano))
		tme = (dat.day + (1+(dat.hour-9)))
		stimator = stima(tme)
		stmzone1=stimator.zone1stm()
		stmzone2=stimator.zone2stm()
		stmzone3=stimator.zone3stm()
		stmzone4=stimator.zone4stm()
		stmzone5=stimator.zone5stm()
		stmzone6=stimator.zone6stm()
		stmzone7=stimator.zone7stm()
		stmzone8=stimator.zone8stm()
		stmzone9=stimator.zone9stm() 
		stm1=int(stmzone1)
		stm2=int(stmzone2)
		stm3=int(stmzone3)
		stm4=int(stmzone4)
		stm5=int(stmzone5)
		stm6=int(stmzone6)
		stm7=int(stmzone7)
		stm8=int(stmzone8)
		stm9=int(stmzone9)
		
		print stm1
		print stm2
		print stm3
		print stm4
		print stm5
		print stm6
		print stm7
		print stm8
		print stm9
		
		if(d1[-1]-d1[-2]<0):
			
			status1 = 'leave'
			ts = (dat.hour * 60 + (dat.minute+5))-(9*60) 
			if(day=='Monday'):
				predict=pres.Monday()
			if(day=='Tuesday'):
				predict=pres.Tuesday()
			if(day=='Wednesday'):
				predict=pres.Wednesday()
			if(day=='Thursday'):
				predict=pres.Thursday()
			if(day=='Friday'):
				predict=pres.Friday()
			print "zone1 prediction to return in 5 min is %s" %predict
			if(predict==1):
				#switch of the light after 5 minuts if the user wont return , but hight probability that user wont return
				print "Switch off if the user wont return in 5 minuts"
				#enviar mensagem pro actuator tbem
			elif(predict==0):
				#switch off the light after 10 minutes
				print "Switch off if the user wont return in 5 minuts"
				
		else:
			status1 = 'working'
			print "zone 1 occupied"
			
		if(d2[-1]-d2[-2]<0):
			status2 = 'leave'
			ts = (dat.hour * 60 + (dat.minute+5))-(9*60) 
			if(day=='Monday'):
				predict=pres.Monday()
			if(day=='Tuesday'):
				predict=pres.Tuesday()
			if(day=='Wednesday'):
				predict=pres.Wednesday()
			if(day=='Thursday'):
				predict=pres.Thursday()
			if(day=='Friday'):
				predict=pres.Friday()
			print "zone2 prediction to return in 5 min is %s" %predict
			if(predict==1):
				#switch of the light after 5 minuts if the user wont return , but hight probability that user wont return
				print "Switch off if the user wont return in 5 minuts"
				predict1=1
				#enviar mensagem pro actuator tbem
			elif(predict==0):
				#switch off the light after 10 minutes
				print "Switch off if the user wont return in 5 minuts"
				predict1=0
		else:
			status2 = 'working'
			print "zone 2 occupied"
			
		if(d3[-1]-d3[-2]<0):
			status3 = 'leave'
			ts = (dat.hour * 60 + (dat.minute+5))-(9*60) 
			pres = pre(ts)
			if(day=='Monday'):
				predict=pres.Monday()
			if(day=='Tuesday'):
				predict=pres.Tuesday()
			if(day=='Wednesday'):
				predict=pres.Wednesday()
			if(day=='Thursday'):
				predict=pres.Thursday()
			if(day=='Friday'):
				predict=pres.Friday()
			print "zone3 prediction to return in 5 min is %s" %predict
			if(predict==1):
				#switch of the light after 5 minuts if the user wont return , but hight probability that user wont return
				print "Switch off if the user wont return in 5 minuts"
				#enviar mensagem pro actuator tbem
			elif(predict==0):
				#switch off the light after 10 minutes
				print "Switch off if the user wont return in 5 minuts"
		else:
			status3 = 'working'
			print "zone 3 occupied"
			
			
		if(d4[-1]-d4[-2]<0):
			status4 = 'leave'
			ts = (dat.hour * 60 + (dat.minute+5))-(9*60) 
			pres = pre(ts)
			if(day=='Monday'):
				predict=pres.Monday()
			if(day=='Tuesday'):
				predict=pres.Tuesday()
			if(day=='Wednesday'):
				predict=pres.Wednesday()
			if(day=='Thursday'):
				predict=pres.Thursday()
			if(day=='Friday'):
				predict=pres.Friday()
			print "zone4 prediction to return in 5 min is %s" %predict
			if(predict==1):
				#switch of the light after 5 minuts if the user wont return , but hight probability that user wont return
				print "Switch off if the user wont return in 5 minuts"
				#enviar mensagem pro actuator tbem
			elif(predict==0):
				#switch off the light after 10 minutes
				print "Switch off if the user wont return in 5 minuts"
		else:
			status4 = 'working'
			print "zone 4 occupied"
			
			
		if(d5[-1]-d5[-2]<0):
			status5 = 'leave'
			ts = (dat.hour * 60 + (dat.minute+5))-(9*60) 
			pres = pre(ts)
			if(day=='Monday'):
				predict=pres.Monday()
			if(day=='Tuesday'):
				predict=pres.Tuesday()
			if(day=='Wednesday'):
				predict=pres.Wednesday()
			if(day=='Thursday'):
				predict=pres.Thursday()
			if(day=='Friday'):
				predict=pres.Friday()
			print "zone5 prediction to return in 5 min is %s" %predict
			if(predict==1):
				#switch of the light after 5 minuts if the user wont return , but hight probability that user wont return
				print "Switch off if the user wont return in 5 minuts"
				#enviar mensagem pro actuator tbem
			elif(predict==0):
				#switch off the light after 10 minutes
				print "Switch off if the user wont return in 5 minuts"
		else:
			status5 = 'working'
			print "zone 5 occupied"
			
			
			
		if(d6[-1]-d6[-2]<0):
			status6 = 'leave'
			ts = (dat.hour * 60 + (dat.minute+5))-(9*60) 
			pres = pre(ts)
			if(day=='Monday'):
				predict=pres.Monday()
			if(day=='Tuesday'):
				predict=pres.Tuesday()
			if(day=='Wednesday'):
				predict=pres.Wednesday()
			if(day=='Thursday'):
				predict=pres.Thursday()
			if(day=='Friday'):
				predict=pres.Friday()
			print "zone6 prediction to return in 5 min is %s" %predict
			if(predict==1):
				#switch of the light after 5 minuts if the user wont return , but hight probability that user wont return
				print "Switch off if the user wont return in 5 minuts"
				#enviar mensagem pro actuator tbem
			elif(predict==0):
				#switch off the light after 10 minutes
				print "Switch off if the user wont return in 5 minuts"
		else:
			status6 = 'working'
			print "zone 6 occupied"
			
		
		if(d7[-1]-d7[-2]<0):
			status7 = 'leave'
			ts = (dat.hour * 60 + (dat.minute+5))-(9*60) 
			pres = pre(ts)
			if(day=='Monday'):
				predict=pres.Monday()
			if(day=='Tuesday'):
				predict=pres.Tuesday()
			if(day=='Wednesday'):
				predict=pres.Wednesday()
			if(day=='Thursday'):
				predict=pres.Thursday()
			if(day=='Friday'):
				predict=pres.Friday()
			print "zone7 prediction to return in 5 min is %s" %predict
			if(predict==1):
				#switch of the light after 5 minuts if the user wont return , but hight probability that user wont return
				print "Switch off if the user wont return in 5 minuts"
				#enviar mensagem pro actuator tbem
			elif(predict==0):
				#switch off the light after 10 minutes
				print "Switch off if the user wont return in 5 minuts"
		else:
			status7 = 'working'
			print "zone 7 occupied"
			
			
		if(d8[-1]-d8[-2]<0):
			status8 = 'leave'
			ts = (dat.hour * 60 + (dat.minute+5))-(9*60) 
			pres = pre(ts)
			if(day=='Monday'):
				predict=pres.Monday()
			if(day=='Tuesday'):
				predict=pres.Tuesday()
			if(day=='Wednesday'):
				predict=pres.Wednesday()
			if(day=='Thursday'):
				predict=pres.Thursday()
			if(day=='Friday'):
				predict=pres.Friday()
			print "zone8 prediction to return in 5 min is %s" %predict
			if(predict==1):
				#switch of the light after 5 minuts if the user wont return , but hight probability that user wont return
				print "Switch off if the user wont return in 5 minuts"
				#enviar mensagem pro actuator tbem
			elif(predict==0):
				#switch off the light after 10 minutes
				print "Switch off if the user wont return in 5 minuts"
		else:
			status8 = 'working'
			print "zone 8 occupied"
		
		if(d9[-1]-d9[-2]<0):
			status9 = 'leave'
			ts = (dat.hour * 60 + (dat.minute+5))-(9*60) 
			pres = pre(ts)
			if(day=='Monday'):
				predict=pres.Monday()
			if(day=='Tuesday'):
				predict=pres.Tuesday()
			if(day=='Wednesday'):
				predict=pres.Wednesday()
			if(day=='Thursday'):
				predict=pres.Thursday()
			if(day=='Friday'):
				predict=pres.Friday()
			print "zone9 prediction to return in 5 min is %s" %predict
			if(predict==1):
				#switch of the light after 5 minuts if the user wont return , but hight probability that user wont return
				print "Switch off if the user wont return in 5 minuts"
				#enviar mensagem pro actuator tbem
			else:
				#switch off the light after 10 minutes
				print "Switch off if the user wont return in 5 minuts"
		else:
			status9 = 'working' 
			print "zone 9 occupied" 
			
			
		


#calculate dimming % for each zone
# light zone <10 dimming 90%
# light zone 10 <> 20 dimming 80%
# light zone 20 <>30 dimming 60%
# light zone >30 dimming 40%
		if(stm1<=10):
			dim1=90
			print "dim1 %s" %dim1
		elif(stm1>10 and stm1<20):
			dim1=80
			print "dim1 %s" %dim1
		elif(stm1>=20 and stm1<30):
			dim1=60
			print "dim1 %s" %dim1
		elif(stm1>=30):
			dim1=40
			print "dim1 %s" %dim1
			
		if(stm2<=10):
			dim2=90
			print "dim2 %s" %dim1
		elif(stm2>10 and stm2<20):
			dim2=80
			print "dim2 %s" %dim1
		elif(stm2>=20 and stm2<30):
			dim1=60
			print "dim2 %s" %dim2
		elif(stm2>=30):
			dim1=40
			print "dim2 %s" %dim2	
		
		if(stm3<=10):
			dim3=90
			print "dim3 %s" %dim3
		elif(stm3>10 and stm3<20):
			dim3=80
			print "dim3 %s" %dim3
		elif(stm3>=20 and stm3<30):
			dim3=60
			print "dim3 %s" %dim3
		elif(stm3>=30):
			dim3=40
			print "dim3 %s" %dim3		
			
		if(stm4<=10):
			dim4=90
			print "dim4 %s" %dim4
		elif(stm4>10 and stm4<20):
			dim4=80
			print "dim4 %s" %dim4
		elif(stm4>=20 and stm4<30):
			dim4=60
			print "dim4 %s" %dim4
		elif(stm4>=30):
			dim4=40
			print "dim4 %s" %dim4		
			
		if(stm5<=10):
			dim5=90
			print "dim5 %s" %dim5
		elif(stm5>10 and stm5<20):
			dim5=80
			print "dim5 %s" %dim5
		elif(stm5>=20 and stm5<30):
			dim5=60
			print "dim5 %s" %dim5
		elif(stm5>=30):
			dim5=40
			print "dim5 %s" %dim5			
			
		if(stm6<=10):
			dim6=90
			print "dim6 %s" %dim6
		elif(stm6>10 and stm6<20):
			dim6=80
			print "dim6 %s" %dim6
		elif(stm6>=20 and stm6<30):
			dim6=60
			print "dim6 %s" %dim6
		elif(stm6>=30):
			dim6=40
			print "dim6 %s" %dim6			
			
		if(stm7<=10):
			dim4=90
			print "dim7 %s" %dim7
		elif(stm7>10 and stm7<20):
			dim7=80
			print "dim7 %s" %dim7
		elif(stm7>=20 and stm7<30):
			dim7=60
			print "dim7 %s" %dim7
		elif(stm7>=30):
			dim7=40
			print "dim7 %s" %dim7
			
		if(stm8<=10):
			dim8=90
			print "dim8 %s" %dim8
		elif(stm8>10 and stm8<20):
			dim8=80
			print "dim8 %s" %dim8
		elif(stm8>=20 and stm8<30):
			dim8=60
			print "dim8 %s" %dim8
		elif(stm8>=30):
			dim8=40
			print "dim8 %s" %dim8
			
		if(stm9<=10):
			dim9=90
			print "dim9 %s" %dim9
		elif(stm9>10 and stm9<20):
			dim9=80
			print "dim9 %s" %dim9
		elif(stm9>=20 and stm9<30):
			dim9=60
			print "dim9 %s" %dim9
		elif(stm9>=30):
			dim9=40
			print "dim9 %s" %dim9  
			
	else:
		dim1=0
		dim2=0
		dim3=0
		dim4=0
		dim5=0
		dim6=0
		dim7=0
		dim8=0
		dim9=0
		stm1=0
		stm2=0
		stm3=0
		stm4=0
		stm5=0
		stm6=0
		stm7=0
		stm8=0
		stm9=0
	
#machine learning occupancy
	url_tmp = "https://dweet.io:443/dweet/for/ictbuildingsl?dim1=" +str(dim1) +"&dim2=" +str(dim2)+"&dim3=" +str(dim3)+"&dim4=" +str(dim4)+"&dim5=" +str(dim5)+"&dim6=" +str(dim6)+"&dim7=" +str(dim7)+"&dim8=" +str(dim8)+"&dim9=" +str(dim9)
	response = urllib2.urlopen(url_tmp)
	print url_tmp
	url_tmp1 = "https://dweet.io:443/dweet/for/ictbuilding?stmzone1=" +str(stm1) +"&stmzone2=" +str(stm2)+"&stmzone3=" +str(stm3)+"&stmzone4=" +str(stm4)+"&stmzone5=" +str(stm5)+"&stmzone6=" +str(stm6)+"&stmzone7=" +str(stm7)+"&stmzone8=" +str(stm8)+"&stmzone9=" +str(stm9)
	response = urllib2.urlopen(url_tmp1)
	print url_tmp1
	#pres = '{"id":"A","sensor": "presence","time": "'+str(ts)+'", "z1":"'+str(z1)+'", "z2":"'+str(z2)+'", "z3":"'+str(z3)+'", "z4":"'+str(z4)+'", "z5":"'+str(z5)+'", "z6":"'+str(z6)+'", "z7":"'+str(z7)+'", "z8":"'+str(z8)+'"}'
	cont= '{"controler": "lights","DIM1":"' +str(dim1)+ '"}'
	client.publish("$ICTFORSMARTBUILDINGSDAN/controlight", cont)
	print 'end'

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
	self.client.subscribe("/ICTFORSMARTBUILDINGSDAN/#", qos=2)
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

