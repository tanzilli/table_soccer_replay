#!/usr/bin/env python3

import io
import os 
import random
import picamera
import paho.mqtt.client as mqtt
import time

goal=False

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe("biliardino/redcam/cmd")
	
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

camera = picamera.PiCamera(resolution=(640,480), framerate=30)
stream = picamera.PiCameraCircularIO(camera, seconds=20)
camera.start_recording(stream, format='h264')

try:
	while True:
		camera.wait_recording(1)
		if goal_detected():
			print("Still recording for 1 sec")
			camera.wait_recording(1)
			print("Copy to file")
			stream.copy_to('replay_redcam.h264')
			print("Convert to mp4")
			os.system("ffmpeg -v 1 -f h264 -i replay_redcam.h264 -c:v copy -y replay_redcam.mp4")
			time.sleep(1);
			print("Send event MQTT")
			client.publish("biliardino/redcam/end","ready");
finally:
    camera.stop_recording()			