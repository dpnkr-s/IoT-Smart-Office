#!/usr/bin/env python
# -*- coding: utf-8 -*-
from array import *
import paho.mqtt.client as mqtt
import json
import time
import random
import urllib2
from pres import pre
from pylab import *
from datetime import datetime
import math
from datetime import date
import calendar
from pyswarm import pso
dweet = 'ventlab'
d=[]
ventState = 0 # on=off status of ventilation system
heatState = 0 # on-off status of heating system
Vfr_opt = 0
Dra = 0
Dea = 0
np = 0 # number of people after 5 min from NN prediction
npp = 0 # number of people at present in the room froms sensors
temp_out = 0 # outside air temperature
E_current_timeslot=0
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
ipBroker = "172.20.240.121"
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
        self.Tsupply = 0
        
    def set_Tsupply(self, Tset=0):
        self.Tsupply = Tset + 273.15
    
    def add_VOCsurface(self, femission=0, surfarea=0):
        
        EK = ((femission*surfarea)/(self.volume*0.9))
        self.objectsEK.append(EK)
        
    def update_RoomTemp(self, timeslot=0, supply_flow_rate=0):
        
        tk = (supply_flow_rate*timeslot)/self.volume
        self.room_temp = tk*self.Tsupply + (1-tk)*self.room_temp        
        
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



def __init__(self,ts):
	self.ts=ts
		
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("$ICTFORSMARTBUILDINGSDAN/sensor")
		
def on_message(client, userdata, msg):
	print day
	now = datetime.utcnow()
	dat = datetime.now()
	hora=dat.hour
	print(msg.topic+" "+str(msg.payload))
	dict = json.loads(str(msg.payload))
	print dict
	d.append(str(msg.payload)) 
	print "hora %s" %hora
	zn1=int(dict["z1"])
	zn2=int(dict["z2"])
	zn3=int(dict["z3"])
	zn4=int(dict["z4"])
	zn5=int(dict["z5"])
	zn6=int(dict["z6"])
	zn7=int(dict["z7"])
	zn8=int(dict["z8"])
	zn9=1
	temp_out=int(dict["tempt"])
	npp=int(zn1)+int(zn2)+int(zn3)+int(zn4)+int(zn5)+int(zn6)+int(zn7)+int(zn8)+int(zn9)
	
	d1.append(zn2)
	d2.append(zn2)
	d3.append(zn3)
	d4.append(zn4)
	d5.append(zn5)
	d6.append(zn6)
	d7.append(zn7)
	d8.append(zn8)
	d9.append(zn9)
	
	#evaluate on a 2 degree grid

	
	if(hora>= 9 and hora <= 18):
		month=dat.month
		dia=dat.day
		ano=dat.year
		hora=str(dat.hour)+":" + str(dat.minute)
		dataT= (str(dia) + "/"+ str(month) + "/" +str(ano))
		tme = (dat.day + (1+(dat.hour-9)))
		np = npp
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
				np=np-1
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
				np=np-1
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
				np=np-1
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
				np=np-1
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
				np=np-1
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
				np=np-1
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
				np=np-1
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
				np=np-1
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
				np=np-1
			else:
				#switch off the light after 10 minutes
				print "Switch off if the user wont return in 5 minuts"
		else:
			status9 = 'working' 
			print "zone 9 occupied"
		
		
		if(npp==0):
			heatState = 0
			ventState = 0
			E_current_timeslot = 0
			
			
		else:
			
			vfr_req = office.get_finalACH(npeople=npp, maxVOC=100)
			Toutside = temp_out + 273.15
			Treturn = office.room_temp
			Tsupply = office.Tsupply
			ToC = temp_out
			TrC = Treturn - 273.15
			TrC = round(TrC,2)
			TsC = Tsupply - 273.15

			if (Toutside >= Tsupply):
				Vfr_opt = round(vfr_req,4)
				heatState = 0
				ventState = 1
				Dra = 0
				Dea = 0.85
				office.update_RoomTemp(timeslot=60, supply_flow_rate=Vfr_opt)
				Eff = 2*0.100*(Vfr_opt/0.0944)**3
				E_current_timeslot = (Eff*(1./60))*1000
				print E_current_timeslot
				print Vfr_opt
				print Dra
				print Dea	
			else:    
				heatState = 1
				ventState = 1
				# input parameters for PSO algorithm
				args = (Tsupply, Toutside, Treturn, vfr_req)
				lb = [0.0, 0.0, 0.0]
				ub = [0.0944, 0.88, 0.85]
				xopt, fopt = pso(energy_tot, lb, ub, f_ieqcons=iaq_constraint, args=args, maxiter=500)
				Vfr_opt = round(xopt[0],4)
				Dra = round(xopt[1],2)
				Dea = round(xopt[2],2)
				office.update_RoomTemp(timeslot=60, supply_flow_rate=Vfr_opt)    
				E_current_timeslot = (fopt*(1./60))*1000
				print E_current_timeslot
				print Vfr_opt
				print Dra
				print Dea	
				
	url_tmp = "https://dweet.io:443/dweet/for/ventlab?Vfr_opt=" +str(Vfr_opt) +"&Dra=" +str(Dra)+"&Dea=" +str(Dea)+"&heatState=" +str(heatState)+"&ventState=" +str(ventState)+"&E_current_timeslot=" +str(E_current_timeslot)+"&Tsupply=" +str(TsC)+"&Toutside=" +str(TrC)+"&To=" +str(ToC)     
	response = urllib2.urlopen(url_tmp)
	print url_tmp			
				
				
				
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
	
# creating a room object by using given parameters 
office = room_properties(length=8.75, width=6.25, height=3.75, qiaq=39.6, occuphs=8)
office.add_VOCsurface(femission=0.5, surfarea=54.6875) # floor - carpet
office.add_VOCsurface(femission=40, surfarea=112.5) # walls - acrylic paint
office.add_VOCsurface(femission=40, surfarea=54.6875) # ceiling - acrylic paint
vfr_req = office.get_finalACH(npeople=9, maxVOC=100) # minimum req. volume flow rate
office.set_Tsupply(Tset=24) # setting desired temperature to 24 C

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
     
client.connect(ipBroker,portBroker,60)
client.loop_forever()
