#https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h

import evdev
import select
import paho.mqtt.client as mqtt
import socket

PROGRAM_VERSION="1.03"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("prova")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

print("Version %s" % (PROGRAM_VERSION))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("bluereplay.local", 1883, 60)

client.loop_start()

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
devices = {dev.fd: dev for dev in devices}

value = 1
print("Value: {0}".format(value))

done = False
while not done:
    r, w, x = select.select(devices, [], [])
    for fd in r:
        for event in devices[fd].read():
            event = evdev.util.categorize(event)
            if isinstance(event, evdev.events.RelEvent):
                if event.event.value==-1:
                    client.publish("table_soccer/" + socket.gethostname() + "/input","left")
                if event.event.value==1:
                    client.publish("table_soccer/" + socket.gethostname() + "/input","right")

                value = value + event.event.value
                print("Value: {0}".format(value))
            elif isinstance(event, evdev.events.KeyEvent):
                print(event)
                if event.keycode == "KEY_PLAY" and event.keystate == event.key_down:
                    client.publish("table_soccer/" + socket.gethostname() + "/input","0")
                if event.keycode == "KEY_F1" and event.keystate == event.key_down:
                    client.publish("table_soccer/" + socket.gethostname() + "/input","1")
                if event.keycode == "KEY_F2" and event.keystate == event.key_down:
                    client.publish("table_soccer/" + socket.gethostname() + "/input","2")
                if event.keycode == "KEY_F3" and event.keystate == event.key_down:
                    client.publish("table_soccer/" + socket.gethostname() + "/input","3")
