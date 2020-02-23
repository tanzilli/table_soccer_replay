# Table Soccer Replay

Sistema di conteggio punti e replay video su biliardino tradizionale

* Rilevamento goal tramite barriere IR installate all'interno del biliardino
* Replay automatico del goal da due telecamere
* Tabellone elettronico e replay video su schermo full HD

Schema a blocchi

![Schema a blocchi](/images/diagramma1.jpg)

Le Raspberry usate sono tre:

* Gestione telecamera giocatori rossi
	* Accesso ssh: ssh pi@redcam.local
	* Node-red: [http://redcam.local:1880](http://redcam.local:1880)
	* Streaming video: [http://redcam.local:8001/stream.mjpg](http://redcam.local:8001/stream.mjpg)

* Gestione telecamera giocatori blu
	* Accesso ssh: ssh pi@bluecam.local
	* Node-Red: [http://bluecam.local:1880](http://bluecam.local:1880)
	* Streaming video: [http://bluecam.local:8001/stream.mjpg](http://bluecam.local:8001/stream.mjpg)
	* Programma stream.py: [picamera/stream.py](picamera/stream.py)

* Lettura barriere IR, webserver, broker MQTT
	* Accesso ssh: ssh pi@biliardinocam.local
	* Node-Red: [http://biliardino.local:1880](http://biliardino.local:1880)
	* Codiad: [http://biliardino.local](http://biliardino.local)
	* Flow Node-Red: [flows/biliardino](flows/biliardino)


## Links

* <https://github.com/tanzilli/raspberrypi_camera_streamer>