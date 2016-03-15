var session;
var publisher;
var connectionCount = 0;

////////////// Checking user browser support for webRTC ///////////// 
if (OT.checkSystemRequirements() == 1) {
    var session = OT.initSession(apiKey, tokbox_session_id);
    // call handlers for diff events
} else {

    if (browser == "Internet Explorer") {
        var session = OT.initSession(apiKey, tokbox_session_id);
    } else {
        // The client does not support WebRTC.
        $('body').ready(function () {
            $(".err-vid").show();
            $(".error_msg").html("Your browser does not support webRTC.");
        });
    }
}

//////////////// Creating publisher stream /////////////////
session.connect(token, function (error) {
    if (error) {
        $(".err-vid").show();
        $(".error_msg").html("Error connecting: ", error.code, error.message);
    } else {
        //alert('lin28');
        var publisherDiv = document.createElement('div');
        document.getElementById("user_stream").appendChild(publisherDiv);
        //Create a div for the subscriber to replace
        publisherDiv.setAttribute('id', "user_stream_session");
        var publisherProps = {width: 476, height: 320, insertMode: "replace", mirror: true};//set the params for my camera video
        publisher = OT.initPublisher(publisherDiv.id, publisherProps, {insertMode: "append"});
        session.publish(publisher);

        publisher.on({
            streamCreated: function (event) { //publisher handler called when stream created

                /////// Detecting Audio Level //////////////
                detectAudioLevel();

                /////// Detecting Audio Video devices //////////////
                //checkDevices();
            },
            streamDestroyed: function (event) {														//publisher handler called when stream distroyed
                $(".successpopup").hide();
            },
            accessDialogOpened: function accessDialogOpenedHandler(event) { //handler when access dialog opened
                $(".successpopup").hide();
            },
            accessDialogClosed: function (event) {														//handler when access dialog closed 
                $(".successpopup").hide();
            },
            accessAllowed: function (event) {
                $(".successpopup").hide();
            },
            accessDenied: function () {
                $(".error_msg").html('Please allow access to the Camera and Microphone and try publishing again.');
                $(".err-vid").show();
                $("body").addClass("flow_hidden");
                publisher.destroy();
                publisher = null;
            }
        });
    }
});

////////////// Session connections handling //////////////////// 
session.on({
    connectionCreated: function (event) {
        connectionCount++;
        //alert(connectionCount + " connections.");
    },
    connectionDestroyed: function (event) {
        connectionCount--;
        //alert(connectionCount + " connections.");
        //$(".successpopup").hide();
    },
    streamPropertyChanged: function (event) {
        //alert(event)
    },
    sessionDisconnected: function sessionDisconnectHandler(event) {
        // The event is defined by the SessionDisconnectEvent class
        //$(".err-vid").show();
//        $(".error_msg").html("Disconnected from the session.");
//        $(".successpopup").hide();
        //document.getElementById('disconnectBtn').style.display = 'none';
        if (event.reason == "networkDisconnected") {
             $(".err-vid").show();
            $(".error_msg").html("Your network connection terminated.");
        }
    }
});

//Listen for exceptions
OT.on("exception", function (event) {
    $(".successpopup").hide();
    $(".videocheck").removeClass('fa-check').addClass('fa-times');

    if (event.code == "1500") {
        event.message = "We can not connect to your camera/mic. Please make sure your camera/mic is connected and not being used by any other application."
    }
    $(".error_msg").html(event.message);
    $(".err-vid").show();
    $("body").addClass("flow_hidden");
});



///////////// Playing song for checking speeaker level ///////////// 
function StartOrStop(audioFile) {
    var audie = document.getElementById("myAudio");
    if (!audie.src || audie.src !== audioFile)
        audie.src = audioFile;
    //console.log(audie.paused);
    if (audie.paused == false) {
        //console.log('pause');
        audie.pause();
    } else {
        //console.log('play');
        audie.play();
    }
}

// Checking Audio levelX
function detectAudioLevel()
{
    $(".miccheck").removeClass('ntcompt');
    publisher.setStyle('audioLevelDisplayMode', 'off');
    var movingAvg = null;
    publisher.on('audioLevelUpdated', function (event) {
        if (movingAvg === null || movingAvg <= event.audioLevel) {
            movingAvg = event.audioLevel;
        } else {
            movingAvg = 0.7 * movingAvg + 0.3 * event.audioLevel;
        }

        // 1.5 scaling to map the -30 - 0 dBm range to [0,1]
        var logLevel = (Math.log(movingAvg) / Math.LN10) / 1.5 + 1;
        logLevel = Math.min(Math.max(logLevel, 0), 1);
        document.getElementById('chkMikeLevel').value = logLevel;
        //$(".enter_session_link").css('display', 'block');
    });
}

//Stop publishing audio and video stream
function stopPublishing() {
    if (publisher)
    {
        session.unpublish(publisher);
    }
    publisher.destroy();						//destroy publisher object
}

function checkDevices() {
    var audioInputDevices;
    var videoInputDevices;
    OT.getDevices(function (error, devices) {
        audioInputDevices = devices.filter(function (element) {
            return element.kind == "audioInput";
        });
        videoInputDevices = devices.filter(function (element) {
            return element.kind == "videoInput";
        });

        if (audioInputDevices.length > 0 && videoInputDevices.length > 0) {
            /////// Detecting Audio Level //////////////
            detectAudioLevel();
        } else if (videoInputDevices.length === 0) {
            $(".error_msg").html('We can not connect to your camera. Please make sure your camera is connected and not being used by any other application');
            $(".err-vid").show();
            $("body").addClass("flow_hidden");
            publisher.destroy();
        } else if (audioInputDevices.length === 0) {
            $(".error_msg").html('We can not connect to your microphone. Please make sure your microphone is connected and not being used by any other application');
            $(".err-vid").show();
            $("body").addClass("flow_hidden");
            publisher.destroy();
        }

    });
} 