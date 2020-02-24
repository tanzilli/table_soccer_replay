#!/usr/bin/env python3
# https://picamera.readthedocs.io/en/release-1.13/recipes1.html#recording-to-a-circular-stream

import io
import os
import random
import picamera
import paho.mqtt.client as mqtt
import time
import socket
from datetime import datetime

goal=False

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe("biliardino/" + socket.gethostname() + "/cmd")

def on_message(client, userdata, msg):
	global goal
	goal=True
	print(msg.payload)
	print("Goal detected")

def goal_detected():
	global goal

	if goal==True:
		goal=False
		return True
	else:
		return False

client = mqtt.Client()
client.connect("biliardino.local",1883,60)
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()

camera = picamera.PiCamera(resolution=(640,480), framerate=120)
stream = picamera.PiCameraCircularIO(camera, seconds=3)
camera.start_recording(stream, format='h264')

try:
	while True:
		camera.wait_recording(1)
		if goal_detected():
			print("Still recording for 1 sec")
			camera.wait_recording(1)
			print("Copy to file")
			os.system("rm video/*.h264")
			os.system("rm video/*.mp4")

			now = datetime.now()
			basename=socket.gethostname() + "_" + now.strftime("%m%d%Y%H%M%S")

			stream.copy_to("video/" + basename + ".h264")
			stream.clear()
			print("Convert " + basename + ".h264 to " + basename + ".mp4")
			os.system("ffmpeg -v 1 -f h264 -i video/" + basename + ".h264 -c:v copy -y video/" + basename + ".mp4")
			time.sleep(1);
			print("Send event MQTT")
			client.publish("biliardino/" + socket.gethostname() + "/ready",basename+".mp4");

finally:
	print("finally")
	camera.stop_recording()
