import pygame.camera
import pygame.image
import sys
import os

recyclable_labels = ["bottle"]
pygame.camera.init()
cam = pygame.camera.Camera(pygame.camera.list_cameras()[1])
#cam.start()

def take_picture():
	cam.start()
	img = cam.get_image()
	pygame.image.save(img, "photo.bmp")
	os.system("convert photo.bmp photo.jpg")
	cam.stop()

def analyze_picture():
	take_picture()
	a = os.system("python /usr/local/lib/python2.7/dist-packages/tensorflow/models/image/imagenet/classify_image.py --image_file ~/Matt/photo.jpg> ~/Matt/log.txt")
	with open("log.txt", "rb") as f:
		results = f.read()
	#first_guess = results.split(")")[0]
	first_guess = results
	print(first_guess)
	#results = results.split("\n")
	return first_guess
#pygame.camera.quit()
a = analyze_picture()

# def main_loop():



#--image_file ~/Matt/photo.bmp