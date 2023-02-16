#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pysolar.solar import *
import datetime

def set_north_hemisphere(azimuth):

	if (abs(azimuth) > 180):
		azimuth = abs(azimuth) - 180
	else: 
		azimuth = abs(azimuth) + 180

	return azimuth

class Sun():

	def __init__(self, latitude, longitude):
		self.latitude = latitude
		self.longitude = longitude

	def compute_elevation_azimuth(self, now):
		self.elevation = get_altitude(self.latitude, self.longitude, now)
		self.azimuth = set_north_hemisphere(get_azimuth(self.latitude, self.longitude, now))

	def print_elevation_azimuth(self):
		print ('Solar_elevation: '+str(self.elevation))
		print ('Solar_azimuth: '+str(self.azimuth))
