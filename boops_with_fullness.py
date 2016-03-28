import serial
import os
import subprocess

show_devices = "ls /dev/ | grep cu.usbmodem"
proc = subprocess.Popen(show_devices, stdout=subprocess.PIPE, shell=True)

(out, err) = proc.communicate()
arduino_addresses = out.split("\n")[:-1]

ser_zero = serial.Serial("/dev/" + arduino_addresses[0])
ser_one = serial.Serial("/dev/" + arduino_addresses[1])