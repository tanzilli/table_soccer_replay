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
	* Flow Node-Red: [flows/biliardino.json](flows/biliardino.json)

## Link utili

* [Recording to a circular stream](https://picamera.readthedocs.io/en/release-1.13/recipes1.html#recording-to-a-circular-stream)
* [Picamera Basic Recipes](https://picamera.readthedocs.io/en/release-1.13/recipes1.html)
* <https://github.com/tanzilli/raspberrypi_camera_streamer>

## Come installare Codiad

Per facilitare l'editing delle pagine html e dei programmi in Pyhton e Javascript ho installato l'editor on-line Codiad 
su ogni Raspberry

Prima di installare Codiad bisogna installare i seguenti pacchetti:

	sudo apt update
	sudo apt-get -y install apache2 php php-zip php-mbstring git

Quindi preparare la directory dove Codiad salverà i file:	

	sudo rm -rfv /var/www/html/*
	cd /var/www/html/
	sudo git clone https://github.com/tanzilli/Codiad
	git checkout php7
	sudo touch config.php
	sudo chown www-data:www-data -R /var/www/html/
	
	sudo service apache2 restart

## Come installare Codiad

Type at command line prompt:

	bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)

Enable the systemd service by typing:

	sudo systemctl enable nodered.service

Then start it:

	sudo systemctl start nodered.service

## Chromium

Contenuto del file __/lib/systemd/system/chromium.service__

	[Unit]
	Description=Launch Chromium
	After=systemd-user-sessions.service
	
	[Service]
	ExecStart=/usr/bin/xinit -bg black -fg black -geometry 132x36 -e "runuser pi -c 'chromium-browser --autoplay-policy=no-user-gesture-required --incognito   -kiosk --disable-pinch --overscroll-history-navigation=0 --window-position=0,0 --window-size=1920,1080 http://biliardino.local/biliardino'" -- -nocursor -s 0 -dpms
	Restart=on-abort
	User=root
	WorkingDirectory=/home/pi
	
	[Install]
	WantedBy=multi-user.target

Abilitare chromium

	sudo systemctl daemon-reload
	sudo systemctl enable chromium.service 
	sudo systemctl start chromium.service 
	
## Conversione h264 in mp4

	ffmpeg -f h264 -i replay_redcam.h264 -c:v copy -y replay_redcam.mp4

## Installare Paho-mqtt per Python3

	sudo apt-get install python3-pip
	sudo pip3 install paho-mqtt
	

	

