# -*- coding: utf-8 -*-
import re
import serial
import RPi.GPIO as GPIO
import time
import json

def SerialConnection():	
	ser = serial.Serial("/dev/ttyUSB0", 9600)
	if(ser):
		while 1:
			try:
				data_string = ser.readline()
			except ValueError:
				print("Error found: ", ValueError)
				data_string = '{"temperature": 0, "humidity": 0}'
			
			try:
				data_string = data_string.decode("utf-8")
			except ValueError:
				print("Error found: ", ValueError)
				data_string = '{"temperature": 0, "humidity": 0}'
				
				
			print("coming data: ", data_string)
			
			try:
				data_json = json.loads(data_string)
			except ValueError:
				print("Error found: ", ValueError)
				data_json = '{"temperature": 0, "humidity": 0}'
				
			print("JSON: ",data_json)
			return data_json
	else:
		print("Can't connect to the port")
		exit(0)

