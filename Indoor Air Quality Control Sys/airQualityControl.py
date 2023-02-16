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
from pyswarm import pso

dweet = 'ictbuildingsl'
d=[]
ipBroker = "iot.eclipse.org"
portBroker = 1883
my_date = date.today()
day=str(calendar.day_name[my_date.weekday()])

# ROOM DEFINITION --------------------------------
class room_properties():
   
    # constructor
    def __init__(self, length=0, width=0, height=0, qiaq=39.6, occuphs=0):
        
        self.qiaq = qiaq # unit of qiaq value is 'm^3/h per person'
        
        self.volume = length * width * height # unit of all distances is 'meter'
        
        self.av_occup = occuphs/24.0
        
        self.ach_per_person = (self.qiaq * self.av_occup)/self.volume
        self.room_temp = 22 + 273.15 # default value 22C/295.15 K

        self.objectsEK = []
        self.VOCs = []
        self.VOCtot = sum(self.VOCs)
        
        self.ach_final = 0  
    
    def add_VOCsurface(self, femission=0, surfarea=0):
        
        EK = ((femission*surfarea)/(self.volume*0.9))
        self.objectsEK.append(EK)
        
    def get_RoomTemp(self, timeslot=0, supply_flow_rate=0, Tsupply=0):
        
        tk = (supply_flow_rate*timeslot)/self.volume
        self.room_temp = k*Tsupply + (1-k)*self.room_temp        
        
    def get_finalACH(self, npeople=0, maxVOC=100):         
        
        ach_req = self.ach_per_person*npeople
        
        for i in range(0,len(self.objectsEK)):
                self.VOCs.append(self.objectsEK[i]/ach_req)
        
        self.ach_final = ach_req        
        while (sum(self.VOCs) > maxVOC):
            self.ach_final = self.ach_final + 0.01 
            self.VOCs = []
            for i in range(0,len(self.objectsEK)):
                self.VOCs.append(self.objectsEK[i]/self.ach_final)

        # minimum outside airflow-rate  required in m^3/s           
        vfr_req = (self.ach_final*self.volume)/3600 
        return vfr_req

# PSO for system control

# objective function to be minimized
def energy_tot(x, *args):
    Vr_f, Dra, Dea = x
    # Vr_f = volume flow-rate of fan, same for supply and return
    # Dra, Dea = return air and exhaust air damper ratios
    
    Tsa, Toa, Tra, ach_req = args 
    
    beta = Dra/(Dea+Dra) # ratio of return air vs exhaust air damper
    p = 101325 # pressure = 101.325 kPa
    R = 287.058 # gas constant
    doa = p/(R*Toa) # density of outside air
    dra = p/(R*Tra) # density of return air

    Eh = 1.005*(Vr_f*(1-beta)*doa)*(Tsa-Toa) + beta*1.005*(Vr_f*dra)*(Tsa-Tra)
    # Heat transfer law
    # E (kW) = Cp (kJ/kg-K) * mass_flow_rate (kg/s) * Temp (K)
    
    Ef = 2*0.100*(Vr_f/0.0944)**3
    # Fan affinity law
    # P (kW) = Power_ref(kW)*(flow_rate/ flow_rate_ref)^3        
    
    E_tot = Eh + Ef # kW
    return E_tot 
    
def iaq_constraint(x, *args):
    Vr_f, Dra, Dea = x
    Tsa, Toa, Tra, ach_req = args
    beta = Dra/(Dea+Dra)
    
    Vr_oa = Vr_f*(1-beta) # volume flow-rate of outside air
    
    return [Vr_oa - ach_req]

    
    
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("$ICTFORSMARTBUILDINGSDAN/#")

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
	
	if(hora>= 9 and hora <= 22):
		zn1=str(dict["z1"])
		zn2=str(dict["z2"])
		zn3=str(dict["z3"])
		zn4=str(dict["z4"])
		zn5=str(dict["z5"])
		zn6=str(dict["z6"])
		zn7=str(dict["z7"])
		zn8=str(dict["z8"])
		#zone9=str(dict["z9"])
		ts = int(dict["time"])
		#evaluate on a 2 degree grid
		zn9=1
				
		month=dat.month
		dia=dat.day
		ano=dat.year
		hora=str(dat.hour)+":" + str(dat.minute)
		dataT= (str(dia) + "/"+ str(month) + "/" +str(ano))
		

		
		if(zn1==1):
			status1 = 'leave'
			ts = (dat.hour * 60 + dat.minute)-(9*60) 
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
			
		if(zn2==1):
			status2 = 'leave'
			ts = (dat.hour * 60 + dat.minute)-(9*60) 
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
				#enviar mensagem pro actuator tbem
			elif(predict==0):
				#switch off the light after 10 minutes
				print "Switch off if the user wont return in 5 minuts"
		else:
			status2 = 'working'
			print "zone 2 occupied"
			
		if(zn3==1):
			status3 = 'leave'
			ts = (dat.hour * 60 + dat.minute)-(9*60) 
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
			
			
		if(zn4==1):
			status4 = 'leave'
			ts = (dat.hour * 60 + dat.minute)-(9*60) 
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
			
			
		if(zn5==1):
			status5 = 'leave'
			ts = (dat.hour * 60 + dat.minute)-(9*60) 
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
			
			
			
		if(zn6==1):
			status6 = 'leave'
			ts = (dat.hour * 60 + dat.minute)-(9*60) 
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
			
		
		if(zn7==1):
			status7 = 'leave'
			ts = (dat.hour * 60 + dat.minute)-(9*60) 
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
			
			
		if(zn8==1):
			status8 = 'leave'
			ts = (dat.hour * 60 + dat.minute)-(9*60) 
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
		
		if(zn9==1):
			status9 = 'leave'
			ts = (dat.hour * 60 + dat.minute)-(9*60) 
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
		if(stmzone1<=10):
			dim1=90
			print "dim1 %s" %dim1
		elif(stmzone1>10 and stmzone1<20):
			dim1=80
			print "dim1 %s" %dim1
		elif(stmzone1>=20 and stmzone1<30):
			dim1=60
			print "dim1 %s" %dim1
		elif(stmzone1>=30):
			dim1=40
			print "dim1 %s" %dim1
			
		if(stmzone2<=10):
			dim2=90
			print "dim2 %s" %dim1
		elif(stmzone2>10 and stmzone2<20):
			dim2=80
			print "dim2 %s" %dim1
		elif(stmzone2>=20 and stmzone2<30):
			dim1=60
			print "dim2 %s" %dim2
		elif(stmzone2>=30):
			dim1=40
			print "dim2 %s" %dim2	
		
		if(stmzone3<=10):
			dim3=90
			print "dim3 %s" %dim3
		elif(stmzone3>10 and stmzone3<20):
			dim3=80
			print "dim3 %s" %dim3
		elif(stmzone3>=20 and stmzone3<30):
			dim3=60
			print "dim3 %s" %dim3
		elif(stmzone3>=30):
			dim3=40
			print "dim3 %s" %dim3		
			
		if(stmzone4<=10):
			dim4=90
			print "dim4 %s" %dim4
		elif(stmzone4>10 and stmzone4<20):
			dim4=80
			print "dim4 %s" %dim4
		elif(stmzone4>=20 and stmzone4<30):
			dim4=60
			print "dim4 %s" %dim4
		elif(stmzone4>=30):
			dim4=40
			print "dim4 %s" %dim4		
			
		if(stmzone5<=10):
			dim5=90
			print "dim5 %s" %dim5
		elif(stmzone5>10 and stmzone5<20):
			dim5=80
			print "dim5 %s" %dim5
		elif(stmzone5>=20 and stmzone5<30):
			dim5=60
			print "dim5 %s" %dim5
		elif(stmzone5>=30):
			dim5=40
			print "dim5 %s" %dim5			
			
		if(stmzone6<=10):
			dim6=90
			print "dim6 %s" %dim6
		elif(stmzone6>10 and stmzone6<20):
			dim6=80
			print "dim6 %s" %dim6
		elif(stmzone6>=20 and stmzone6<30):
			dim6=60
			print "dim6 %s" %dim6
		elif(stmzone6>=30):
			dim6=40
			print "dim6 %s" %dim6			
			
		if(stmzone7<=10):
			dim4=90
			print "dim7 %s" %dim7
		elif(stmzone7>10 and stmzone7<20):
			dim7=80
			print "dim7 %s" %dim7
		elif(stmzone7>=20 and stmzone7<30):
			dim7=60
			print "dim7 %s" %dim7
		elif(stmzone7>=30):
			dim7=40
			print "dim7 %s" %dim7
			
		if(stmzone8<=10):
			dim8=90
			print "dim8 %s" %dim8
		elif(stmzone8>10 and stmzone8<20):
			dim8=80
			print "dim8 %s" %dim8
		elif(stmzone8>=20 and stmzone8<30):
			dim8=60
			print "dim8 %s" %dim8
		elif(stmzone8>=30):
			dim8=40
			print "dim8 %s" %dim8
			
		if(stmzone9<=10):
			dim9=90
			print "dim9 %s" %dim9
		elif(stmzone9>10 and stmzone9<20):
			dim9=80
			print "dim9 %s" %dim9
		elif(stmzone9>=20 and stmzone9<30):
			dim9=60
			print "dim9 %s" %dim9
		elif(stmzone9>=30):
			dim9=40
			print "dim9 %s" %dim9
#machine learning occupancy
    
    url_tmp = "https://dweet.io:443/dweet/for/ventlab?zone1=" +str(z1) +"&zone2=" +str(z2)+"&zone3=" +str(z3)+"&zone4=" +str(z4)+"&zone5=" +str(z5)+"&zone6=" +str(z6)+"&zone7=" +str(z7)+"&zone8=" +str(z8)+"&zone9=" +str(z9)
    response = urllib2.urlopen(url_tmp)
    print url_tmp
#	url_tmp = "https://dweet.io:443/dweet/for/ictbuildingsl?zone1=" +str(zn1) +"&zone2=" +str(zn2)+"&zone3=" +str(zn3)+"&zone4=" +str(zn4)+"&zone5=" +str(zn5)+"&zone6=" +str(zn6)+"&zone7=" +str(zn7)+"&zone8=" +str(zn8)
#	response = urllib2.urlopen(url_tmp)
#	print url_tmp
	cont= '{"controler": "lights","DIM1":"' +str(dim1)+ '", "time":"'+hora+'"}'
	client.publish("$ICTFORSMARTBUILDINGSDAN/controlight", cont)
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
	self.client.subscribe("/ICTFORSMARTBUILDINGSDAN/sensor", qos=2)
	rc=0
	while rc == 0:
		rc = self.client.loop()
		print"loop"
	return rc

#client = mqtt.Client()
#client.on_connect = on_connect
#client.on_message = on_message
#client.connect(ipBroker,portBroker,60)
#client.loop_forever()

office = room_properties(length=8.75, width=6.25, height=3.75, qiaq=39.6, occuphs=8)
office.add_VOCsurface(femission=0.5, surfarea=54.6875) # floor - carpet
office.add_VOCsurface(femission=40, surfarea=112.5) # walls - acrylic paint
office.add_VOCsurface(femission=40, surfarea=54.6875) # ceiling - acrylic paint
vfr_req = office.get_finalACH(npeople=9, maxVOC=100) # minimum req. volume flow rate

args = (298.15, 273.15, office.room_temp, vfr_req)
lb = [0.0, 0.0, 0.0]
ub = [0.0944, 0.88, 0.85] # lower and upper bounds for vr_f, dra, dea

xopt, fopt = pso(energy_tot, lb, ub, f_ieqcons=iaq_constraint, args=args, maxiter=500)
print xopt
print fopt