import time
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

def run_algo():
	print "not implemented yet"

while True:
	door_open = 1- int(ser.readline()[0])
	if door_open:
		while door_open:
			door_open = 1-int(ser.readline()[0])
		run_algo()