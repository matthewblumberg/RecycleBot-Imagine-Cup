import pygame.camera
import pygame.image
import sys
import os

import time
import serial
import subprocess
import datetime

# ser = serial.Serial('/dev/ttyACM0', 9600)

pygame.camera.init()
cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])


def open_left():
	print "send the signal to the left solenoid"

def close_left():
	print "send the close signal to the left solenoid"

def open_right():
	print "send the open signal to the right solenoid"

def close_right():
	print "send the close signal to the left solenoid"

def turn_left():
	print "send the left turn signal to the motors"

def turn_right():
	print "send the right turn signal to the motors"

def dump_left():
	open_left()
	turn_left()
	turn_right()
	turn_right()
	close_left()

def dump_right():
	open_right()
	turn_right()
	turn_left()
	turn_left()
	close_right()



def run_algo():
	print "not implemented yet"

def main_loop():
	while True:
		try:
			door_open = 1- int(ser.readline()[0])
		except:
			print "arduino not ready yet"
		if door_open:
			while door_open:
				door_open = 1-int(ser.readline()[0])
			take_picture()
			analyze_picture()

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

roundtrip()
roundtrip()
roundtrip()