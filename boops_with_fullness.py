import serial
import os
import subprocess

show_devices = "ls /dev/ | grep cu.usbmodem"
proc = subprocess.Popen(show_devices, stdout=subprocess.PIPE, shell=True)

(out, err) = proc.communicate()
arduino_addresses = out.split("\n")[:-1]

ser_zero = serial.Serial("/dev/" + arduino_addresses[0])
ser_one = serial.Serial("/dev/" + arduino_addresses[1])

for i in range(3):
	ser_zero_output = ser_zero.readline()
for i in range(3):
	ser_one_output = ser_one.readline()
print "we got here"

if len(ser_zero_output) > 0:
	boops_ser = ser_zero
	motor_ser = ser_one
else:
	boops_ser = ser_one
	motor_ser = ser_zero

while True:
	print(boops_ser.readline())