import pygame.camera
import pygame.image
import sys
import os

import time
import serial

# ser = serial.Serial('/dev/ttyACM0', 9600)
recyclable_labels = ["bottle"]
pygame.camera.init()
cam = pygame.camera.Camera(pygame.camera.list_cameras()[1])

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
	pygame.image.save(img, "photo.bmp")
	os.system("convert photo.bmp photo.jpg")
	cam.stop()

def analyze_picture():
	take_picture()
	os.system("python /usr/local/lib/python2.7/dist-packages/tensorflow/models/image/imagenet/classify_image.py --image_file ~/Downloads/RecycleBot-Imagine-Cup/tensorcode/photo.jpg> ~/Downloads/RecycleBot-Imagine-Cup/tensorcode/log.txt")
	with open("log.txt", "rb") as f:
		results = f.read()
	#first_guess = results.split(")")[0]
	first_guess = results
	print(first_guess)
	#results = results.split("\n")
	return first_guess
#pygame.camera.quit()
# a = analyze_picture()

# main_loop()