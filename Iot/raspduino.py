import serial
import RPi.GPIO as GPIO
import time

ser = serial.Serial("/dev/ttyUSB0", 9600)

while 1:
	x = ser.readline()
	print(x)
