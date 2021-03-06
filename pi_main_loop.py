# import pygame.camera
import pygame.image
import sys
import os
import time
import serial
import subprocess
import datetime
import struct

# ser = serial.Serial('/dev/ttyACM0', 9600)
# ser = serial.Serial('/dev/cu.usbmodemfd1221', 9600)
# ser_two = serial.Serial('/dev/cu.usbmodemfd1211', 9600)

boops_arduino = '/dev/cu.usbmodemfd1221'
motor_arduino = '/dev/cu.usbmodemfd1211'
ser = serial.Serial(boops_arduino, 9600)






# pygame.camera.init()
# cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])


def open_left():
    ser.write(struct.pack(">B", 101))

def open_right():
    ser.write(struct.pack(">B", 103))

def close_left():
    ser.write(struct.pack(">B", 102))

def close_right():
    ser.write(struct.pack(">B", 104))

def turn_left(ser_two):
    ser_two.write(struct.pack(">B", 105))

def turn_right(ser_two):
    ser_two.write(struct.pack(">B", 106))

def reset_motor(ser_two):
	ser_two = serial.Serial(motor_arduino, 9600)
	try:
		ser_two.close()
	except:
		time.sleep(3)
		ser_two.close()
	ser_two = serial.Serial(motor_arduino, 9600)


def dump_left():
	ser_two = serial.Serial(motor_arduino, 9600)
	time.sleep(1)
	open_left()
	time.sleep(3)
	turn_left(ser_two)
	time.sleep(1)
	turn_left(ser_two)
	time.sleep(1)
	turn_left(ser_two)
	time.sleep(1)
	turn_right(ser_two)
	time.sleep(1)
	turn_right(ser_two)
	time.sleep(1)
	turn_right(ser_two)
	time.sleep(1)
	turn_right(ser_two)
	time.sleep(1)
	close_left()
	time.sleep(1)
	ser_two.close()
	time.sleep(1)
	ser_two = serial.Serial(motor_arduino, 9600)


def dump_right():
	ser_two = serial.Serial(motor_arduino, 9600)
	time.sleep(1)
	open_right()
	time.sleep(3)
	turn_right(ser_two)
	time.sleep(1)
	turn_right(ser_two)
	time.sleep(1)
	turn_right(ser_two)
	time.sleep(1)
	turn_left(ser_two)
	time.sleep(1)
	turn_left(ser_two)
	time.sleep(1)
	turn_left(ser_two)
	time.sleep(1)
	turn_left(ser_two)
	time.sleep(1)
	close_right()
	time.sleep(1)
	ser_two.close()
	time.sleep(1)
	ser_two = serial.Serial(motor_arduino, 9600)

def read_door():
	try:
		return int(ser.readline()[0])
	except:
		time.sleep(1)
		return read_door()


def main_loop():
	while True:
		try:
			door_open = int(ser.readline()[0])
			door_open = int(ser.readline()[0])
		except:
			print "arduino not ready yet"
		door_open = int(ser.readline()[0])
		if door_open:
			print "opened"
			while door_open:
				door_open = int(ser.readline()[0])
			print "testing"
			test_roundtrip

def take_picture():
	cam.start()
	img = cam.get_image()
	current = datetime.datetime.now()
	timestamp = []
	timestamp.append(str(current.year))
	timestamp.append(str(current.month))
	timestamp.append(str(current.day))
	timestamp.append(str(current.hour))
	timestamp.append(str(current.minute))
	timestamp.append(str(current.second))
	timestamp = "_".join(timestamp)
	pygame.image.save(img, "photo_{0}.bmp".format(timestamp))
	os.system("convert photo_{0}.bmp photo_{1}.jpg".format(timestamp, timestamp))
	cam.stop()
	return timestamp

def send_picture(timestamp):
	proc=subprocess.Popen('tar -c photo_{0}.jpg | ssh ubuntu@40.122.47.160 "tar -x -C tf_files/"'.format(timestamp), shell=True, stdout=subprocess.PIPE, )
	proc.communicate()
def get_results(timestamp):
	proc=subprocess.Popen('ssh ubuntu@40.122.47.160 "cat tf_files/log.txt"', shell=True, stdout=subprocess.PIPE, )
	response=proc.communicate()[0]
	print response
	return response

def roundtrip():
	timestamp = take_picture()
	send_picture(timestamp)
	time.sleep(3)
	result = get_results(timestamp)
	if result[:-1] == "recyclable":
		dump_left()
	else:
		dump_right()


def local_roundtrip():
	return "not implemented yet"


def test_roundtrip():
	proc=subprocess.Popen('tar -c coke.jpg | ssh ubuntu@40.122.47.160 "tar -x -C tf_files/"'.format(timestamp), shell=True, stdout=subprocess.PIPE, )
	proc.communicate()
	print "sent picture"
	time.sleep(3)
	proc=subprocess.Popen('ssh ubuntu@40.122.47.160 "cat tf_files/log.txt"', shell=True, stdout=subprocess.PIPE, )
	result=proc.communicate()[0]
	if result[:-1] == "recyclable":
		dump_left()
	else:
		dump_right()


main_loop()