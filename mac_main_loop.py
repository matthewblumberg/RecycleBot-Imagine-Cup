import pygame.camera
import pygame.image
import sys
import os
import time
import serial
import subprocess
import datetime
import struct

pygame.camera.init()
cam = pygame.camera.Camera(pygame.camera.list_cameras()[1])

running_locally = True

# ser = serial.Serial('/dev/ttyACM0', 9600)
# ser = serial.Serial('/dev/cu.usbmodemfd1221', 9600)
# ser_two = serial.Serial('/dev/cu.usbmodemfd1211', 9600)

arduino_directory = "/dev"
arduino_prefix = "ttyACM*"


proc=subprocess.Popen('ls {0} | grep {1}'.format(arduino_directory, arduino_prefix), shell=True, stdout=subprocess.PIPE, )
response=proc.communicate()[0]
response = response.split("\n")[:-1]
response = [arduino_directory + "/" + item for item in response]

# boops_arduino = '/dev/cu.usbmodemfd1221'
# motor_arduino = '/dev/cu.usbmodemfd1211'
# ser = serial.Serial(boops_arduino, 9600)
running_on_mac = False

def identify_arduinos():
	first_responses = []
	second_responses = []
	i = 5
	first_ser = serial.Serial(response[0], 9600)
	time.sleep(1)
	try:
		first_responses.append(int(first_ser.readline()[0]))
	except:
		second_ser = serial.Serial(response[1], 9600)
		try:
			second_responses.append(int(second_ser.readline()[0]))
		except:
			print "fuck"
	i-=1
	print i
	# first_ser.close()
	if len(first_responses) > 0:	
		# return first_ser, response[1]
		return response[0], response[1]
	elif len(second_responses):
		first_ser.close()
		# return second_ser, response[0]
		return response[1], response[0]

	else:
		time.sleep(1)
		first_ser.close()
		second_ser.close()
		return identify_arduinos()

boops_arduino, motor_arduino = identify_arduinos()

# boops_arduino, motor_arduino = response[0], response[1]
# boops_arduino = response[0]
ser = serial.Serial(boops_arduino, 9600, writeTimeout=0)


# ser, motor_arduino = identify_arduinos()

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
	ser = serial.Serial(boops_arduino, 9600)
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
	ser = serial.Serial(boops_arduino, 9600)
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
	close_right()
	time.sleep(1)
	ser_two.close()
	time.sleep(1)
	ser_two = serial.Serial(motor_arduino, 9600)

def read_door():
	try:
		return int(ser.readline()[0])
	except:
		print "arduino not ready yet"
		time.sleep(1)
		return read_door()


def take_picture():
	current = datetime.datetime.now()
	timestamp = []
	timestamp.append(str(current.year))
	timestamp.append(str(current.month))
	timestamp.append(str(current.day))
	timestamp.append(str(current.hour))
	timestamp.append(str(current.minute))
	timestamp.append(str(current.second))
	timestamp = "_".join(timestamp)
	if not running_on_mac and not running_locally:
		cam.start()
		img = cam.get_image()
		pygame.image.save(img, "photo_{0}.bmp".format(timestamp))
		os.system("convert photo_{0}.bmp photo_{1}.jpg".format(timestamp, timestamp))
		cam.stop()
	elif running_locally:
		cam.start()
		img = cam.get_image()
		pygame.image.save(img, "tf_files/photo_{0}.bmp".format(timestamp))
		os.system("convert tf_files/photo_{0}.bmp tf_files/photo_{1}.jpg".format(timestamp, timestamp))
		cam.stop()
	# elif running_on_mac:
	# 	os.system("cp coke.jpg photo_{0}.jpg".format(timestamp))
	return timestamp

def send_picture(timestamp):
	proc=subprocess.Popen('tar -c photo_{0}.jpg | ssh ubuntu@40.122.47.160 "tar -x -C tf_files/"'.format(timestamp), shell=True, stdout=subprocess.PIPE, )
	proc.communicate()

def get_results(timestamp):
	if not running_locally:
		proc=subprocess.Popen('ssh ubuntu@40.122.47.160 "cat tf_files/log.txt"', shell=True, stdout=subprocess.PIPE, )
		response=proc.communicate()[0]
	else:
		proc = subprocess.Popen('cat ./tf_files/log.txt', shell=True, stdout=subprocess.PIPE, )
		response = proc.communicate()[0]
	print response
	return response



def main_loop():
	while True:
		try:
			door_open = read_door()
		except:
			print "arduino not ready yet"
			door_open=read_door()
		if door_open:
			print "opened"
			while door_open:
				door_open = read_door()
			print "door closed"
			roundtrip()
			ser = serial.Serial(boops_arduino, 9600)
			print "ready"


def roundtrip():
	timestamp = take_picture()
	if not running_locally:
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
	proc=subprocess.Popen('tar -c coke.jpg | ssh ubuntu@40.122.47.160 "tar -x -C tf_files/"', shell=True, stdout=subprocess.PIPE, )
	proc.communicate()
	print "sent picture"
	time.sleep(3)
	proc=subprocess.Popen('ssh ubuntu@40.122.47.160 "cat tf_files/log.txt"', shell=True, stdout=subprocess.PIPE, )
	result=proc.communicate()[0]
	if result[:-1] == "recyclable":
		dump_left()
	else:
		dump_right()
#main_loop.py()