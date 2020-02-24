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

## Come installare Node-Red

La logica di gestione dell gioco e alcune funzioni di sistema sono gestire in Node-Red

Per installarlo al prompt digitare:

	bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)

Per abilitare Node-Red allo startup:

	sudo systemctl enable nodered.service

Per lanciarlo subito:

	sudo systemctl start nodered.service

## Chromium

Chromium viene utilizzato per realizzare il tabellone elettronico:

Per installarlo sulla Raspberry usare i seguenti comandi:

	sudo apt update
	sudo apt install -y chromium-browser xorg

Creare il file per systemd  __/lib/systemd/system/chromium.service__ con l'editor nano:

	sudo nano /lib/systemd/system/chromium.service
	
e inserire il seguente contenuto:	

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

Abilitare Chromium per essere lanciato automaticamente allo startup:

	sudo systemctl daemon-reload
	sudo systemctl enable chromium.service 

Per lanciarlo nella sessione corrente digitare:	
	
	sudo systemctl start chromium.service 

## Software sulle telecacmere

Installare paho-mqtt
	
	sudo apt update
	sudo apt-get -y install python3-pip
	sudo pip3 install paho-mqtt
	
	cd
	mkdir replay_cam
	cd replay_cam
	wget https://raw.githubusercontent.com/tanzilli/table_soccer_replay/master/replay_camera/replay_camera.py

Create il file di lancio allo startup con nano:

	sudo nano /lib/systemd/system/replay_camera.service

con il seguente contenuto:

	[Unit]
	Description=Replay camera
	After=systemd-user-sessions.service
	
	[Service]
	ExecStart=python3 replay_camera.py
	Restart=on-abort
	User=pi
	WorkingDirectory=/home/pi/replay_camera
	
	[Install]
	WantedBy=multi-user.target

Abilitare Chromium per essere lanciato automaticamente allo startup:

	sudo systemctl daemon-reload
	sudo systemctl enable replay_camera.service 	

Creare una directory di lavoro su RAM dove memorizzare i video:

	sudo nano /etc/fstab

Aggiungere la linea:

	tmpfs   /home/pi/replay_camera/video   tmpfs   defaults,nosuid,auto,uid=1000,size=200m  0  0

Creare un link simbolico a questa directory nella documentroot di apache2:

	sudo ln -s /home/pi pi

### Note

Conversione h264 in mp4

	ffmpeg -f h264 -i replay_redcam.h264 -c:v copy -y replay_redcam.mp4

## Link utili

* [Recording to a circular stream](https://picamera.readthedocs.io/en/release-1.13/recipes1.html#recording-to-a-circular-stream)
* [Picamera Basic Recipes](https://picamera.readthedocs.io/en/release-1.13/recipes1.html)
* <https://github.com/tanzilli/raspberrypi_camera_streamer>

	

