// Doc API Paho: https://www.eclipse.org/paho/files/jsdoc/Paho.MQTT.Client.html
// Esempio Montefusco: https://github.com/AcmeSystemsProjects/toa/blob/montefusco/www/js/controllers_st_sd.js

var mqtt_broker="biliardino.local";
var mqtt_port=1884;
var mqtt_mainpage_client;
var message_line;


// Estrae parametri dalla url che ha chiamato la pagina
// https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
// Uso $.QueryString["param"]
(function($) {
    $.QueryString = (function(paramsArray) {
        let params = {};

        for (let i = 0; i < paramsArray.length; ++i)
        {
            let param = paramsArray[i]
                .split('=', 2);

            if (param.length !== 2)
                continue;

            params[param[0]] = decodeURIComponent(param[1].replace(/\+/g, " "));
        }

        return params;
    })(window.location.search.substr(1).split('&'))
})(jQuery);

function loadVideo(videofile) {
	$("#videoclip").get(0).pause();
    $("#mp4video").attr('src', 'video/' + videofile);
    $("#videoclip").get(0).load();
    $("#videoclip").get(0).play();	
}

// Genera una stringa random di caratteri
// Viane usata per le funzioni MQTT
var randomString = function(length) {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for(var i = 0; i < length; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}

function onConnect() {
	console.log("Connected");
	mqtt_mainpage_client.subscribe("biliardino/#");
}	

function onMessageArrived(message) {
	// Punteggio blu
	console.log(message.destinationName + " " + message.payloadString);
	if (message.destinationName.includes("blue_score")) {
		$("#blue_score").text(message.payloadString);
	}

	// Punteggio rossi
	if (message.destinationName.includes("red_score")) {
		$("#red_score").text(message.payloadString);
	}

	// Fine ripresa redcam
	if (message.destinationName.includes("redcam/ready")) {
		console.log("Load and play replay from red cam");
		console.log(message.payloadString);
		video = document.getElementById('video_replay_red');
		video.src="http://redcam.local/pi/camera/video/" + message.payloadString;
		video.load();
		video.play();	
	}

	// Fine ripresa bluecam
	if (message.destinationName.includes("bluecam/ready")) {
		console.log("Load and play replay from blue cam");
		console.log(message.payloadString);
		video = document.getElementById('video_replay_blue');
		video.src="http://bluecam.local/pi/camera/video/" + message.payloadString;
		video.load();
		video.play();	
	}

	// Show/Hide tabellone
	if (message.destinationName.includes("tabellone")) {
		if (message.payloadString==="show") {
			$("#tabellone").fadeIn();
			$("#setup").fadeOut();
		} else {
			$("#tabellone").fadeOut();
			$("#setup").fadeIn();
		}
	}


	if (message.destinationName.includes("goal")) {
		var x = document.getElementById("audio_goal");
		if (message.payloadString==="true") {
			console.log("Goal ON");
			$("#goal").fadeIn();	
			x.load();	
			//x.play();	
		} else {
			console.log("Goal OFF");
			$("#goal").fadeOut();	
			x.pause();	
		}
	}
}

$(document).ready(function() {
	// Interpretazione messaggi MQTT in arrivo
	mqtt_mainpage_client = new Paho.MQTT.Client(mqtt_broker, Number(mqtt_port), "/ws",randomString(20));
	mqtt_mainpage_client.onMessageArrived=onMessageArrived;
	mqtt_mainpage_client.connect({
		onSuccess:onConnect
	});

});
