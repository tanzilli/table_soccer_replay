// Doc API Paho: https://www.eclipse.org/paho/files/jsdoc/Paho.MQTT.Client.html

var mqtt_broker="bluereplay.local";
var mqtt_port=1884;
var mqtt_client;
var message_line;

// Genera una stringa random di caratteri
// Viene usata per le funzioni MQTT
var randomString = function(length) {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for(var i = 0; i < length; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}

function mqtt_client_onConnect() {
	mqtt_client.subscribe("table_soccer/#");

	message = new Paho.MQTT.Message("get");
	message.destinationName = "table_soccer/blue/score/cmd";
	mqtt_client.send(message);

	message = new Paho.MQTT.Message("get");
	message.destinationName = "table_soccer/red/score/cmd";
	mqtt_client.send(message);
} 

function zeroFill( number, width ) {
  width -= number.toString().length;
  if ( width > 0 )
  {
    return new Array( width + (/\./.test( number ) ? 2 : 1) ).join( '0' ) + number;
  }
  return number + ""; // always return a string
}

function mqtt_client_onMessageArrived(message) {   

	$("#topic_box").text(message.destinationName);
	$("#message_box").text(message.payloadString);

	// Moviola bluereplay
	if (message.destinationName.includes("bluereplay/input")) {
		
		if (message.payloadString=="left") {
			video = document.getElementById('video_replay_blue');
			video.currentTime-=0.1;
		} 

		if (message.payloadString=="right") {
			video = document.getElementById('video_replay_blue');
			video.currentTime+=0.1;
		} 
	}

	// Fine ripresa Raspicam bluereplay
	if (message.destinationName.includes("bluereplay/ready")) {
		video = document.getElementById('video_replay_blue');
		video.src="http://bluereplay.local/video/" + message.payloadString;
		video.load();
		video.play();	
	}

	// Fine ripresa Raspicam redreplay
	if (message.destinationName.includes("redreplay/ready")) {
		video = document.getElementById('video_replay_red');
		video.src="http://redreplay.local/video/" + message.payloadString;
		video.load();
		video.play();	
	}

	// Legge il punteggio dei rossi
	if (message.destinationName.includes("red/score/value")) {
		red_score.setValue(zeroFill(parseInt(message.payloadString),2));
	}

	// Legge il punteggio dei blu
	if (message.destinationName.includes("blue/score/value")) {
		blue_score.setValue(zeroFill(parseInt(message.payloadString),2));
	}
	
}

var bluescore=0;
var redscore=0;

$(document).ready(function() {
	// Messaggi MQTT gestione punteggi e replay
	mqtt_client = new Paho.MQTT.Client(mqtt_broker, Number(mqtt_port), "/ws",randomString(20));
	mqtt_client.onMessageArrived=mqtt_client_onMessageArrived;
	mqtt_client.connect({
		onSuccess:mqtt_client_onConnect
	});

	// Messaggi MQTT movimenti moviola
	mqtt_client = new Paho.MQTT.Client(mqtt_broker, Number(mqtt_port), "/ws",randomString(20));
	mqtt_client.onMessageArrived=mqtt_client_onMessageArrived;
	mqtt_client.connect({
		onSuccess:mqtt_client_onConnect
	});

	blue_score.setValue(zeroFill(0,2));
	red_score.setValue(zeroFill(0,2));
});
