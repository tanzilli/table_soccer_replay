#!/usr/bin/env python3
# https://www.acmesystems.it/table_soccer_replay
# https://picamera.readthedocs.io/en/release-1.13/recipes1.html#recording-to-a-circular-stream

PROGRAM_VERSION="1.04"

#1.04 Salvataggio video su directory di history
#1.03 Server MQTT su bluereplay.local

import io
import os
import random
import picamera
import paho.mqtt.client as mqtt
import time
import socket
from datetime import datetime

replay_request=False

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe("table_soccer/" + socket.gethostname() + "/cmd")
	print(socket.gethostname()) 

def on_message(client, userdata, msg):
	global replay_request
	replay_request=True
	print(msg.payload)
	print("Replay request detected")

def check_replay_request():
	global replay_request

	if replay_request==True:
		replay_request=False
		return True
	else:
		return False

print("Version %s" % (PROGRAM_VERSION))

client = mqtt.Client()
client.connect("bluereplay.local",1883,60)
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()

camera = picamera.PiCamera(resolution=(640,480), framerate=120)
stream = picamera.PiCameraCircularIO(camera, seconds=4)
camera.start_recording(stream, format='h264')

try:
	while True:
		camera.wait_recording(1)
		if check_replay_request():
			#print("Still recording for 1 sec")
			#camera.wait_recording(1)
			print("Copy to file")
			os.system("rm video/*.h264")
			os.system("rm video/*.mp4")

			now = datetime.now()
			basename=socket.gethostname() + "_" + now.strftime("%m%d%Y%H%M%S")

			stream.copy_to("video/" + basename + ".h264")
			stream.clear()
			print("Convert " + basename + ".h264 to " + basename + ".mp4")
			os.system("ffmpeg -v 1 -f h264 -i video/" + basename + ".h264 -c:v copy -y video/" + basename + ".mp4")
			print("Send video ready event to MQTT")
			client.publish("table_soccer/" + socket.gethostname() + "/ready",basename+".mp4");
			os.system("cp video/*.mp4 history")

finally:
	print("Ezit")
	camera.stop_recording()
