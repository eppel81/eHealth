var session;
var publisher;
var subscriber
var archiveID = null;
var connectionCount = 0;
var subscriberProps;
var publisherProps;
var screenSharingPublisher;
var myId = "";

////////////// Checking user browser support for webRTC ///////////// 
if (OT.checkSystemRequirements() == 1) {
    var session = OT.initSession(apiKey, tokbox_session_id);
    // call handlers for diff events
} else {
    // The client does not support WebRTC.
    $('body').ready(function () {
        $(".err-vid").show();
        $(".error_msg").html("Your browser does not support webRTC.");
    });
}

//////////////// Publisher stream /////////////////
session.connect(token, function (error) {
    if (error) {
        $(".err-vid").show();
        $(".error_msg").html("Error connecting: ", error.code, error.message);
    } else {
        var publisherDiv = document.createElement('div');

        document.getElementById("doctor").appendChild(publisherDiv);
        //Create a div for the publisher to replace
        publisherDiv.setAttribute('id', "doctor_block");
        publisherProps = {width: 160, height: 110, insertMode: "replace", mirror: true};//set the params for my camera video
        publisher = OT.initPublisher(publisherDiv.id, publisherProps, {insertMode: "append"});
        session.publish(publisher);

        publisher.on({
            streamCreated: function (event) {														//publisher handler called when stream created
                //sessionTimer("session_timer", "presenter"); /////////// Start Session Timer /////////////
            },
            streamDestroyed: function (event) {														//publisher handler called when stream distroyed

            },
            accessDialogOpened: function accessDialogOpenedHandler(event) {								//handler when access dialog opened

            },
            accessDialogClosed: function (event) {														//handler when access dialog closed 

            },
            accessAllowed: function (event) {

            },
            accessDenied: function accessDeniedHandler(event) {											//handler when access denied to camera
                $(".error_msg").html('Please allow access to the Camera and Microphone and try publishing again.');
                $(".err-vid").show();
                publisher.destroy();
                publisher = null;
            }
        });
    }
});

//////////////// Subscribing stream /////////////////
session.on('streamCreated', function (event) {

    var subscriberDiv = document.createElement('div');
    document.getElementById("patient").appendChild(subscriberDiv);
    //Create a div for the publisher to replace
    subscriberDiv.setAttribute('id', "patient_block");

    subscriberProps = {width: '99.4%', height: 543, insertMode: "replace", mirror: true};	//set video params for subscribing stream
    session.subscribe(event.stream, subscriberDiv.id, subscriberProps, {insertMode: "append"});

    sessionTimer("session_timer", "doctor"); /////////// Start Session Timer /////////////

    //////// Sending signal for start session to patient ///////
    session.signal({
        type: "start_session",
        data: '1'
    });

});

//////////////// Subscriber stream Destroyed /////////////////	
session.on("streamDestroyed", function (event) {

});

/////// Handler when signal received /////
session.on("signal", function (event) {
    var signalType = event.type;
    if (signalType == 'signal:text_chat') {
        var signalText = event.data;
        if (signalText.my_connection != myId) {
            $(".chat_meg_block ul").append("<li><div class=\"comment-left\"><h6>" + signalText.name + "</h6><p>" + signalText.msg + "</p></div></li>");
            $(".chat_meg_block").scrollTop($(".chat_meg_block")[0].scrollHeight);
        }
    } else if (signalType == 'signal:patient_end_session') {
        $("#refresh_page").hide();
        $(".error_msg_cont span").html('<i class="fa fa-check-circle-o"></i>');
        $(".err-vid").show();
        $(".error_msg").html("Patient has ended session successfully.");

        clearInterval(sessionTimer);
        session.disconnect();
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
    },
    sessionConnected: function (event) {
        myId = event.target.connection.connectionId;
    },
    sessionDisconnected: function sessionDisconnectHandler(event) {
        // The event is defined by the SessionDisconnectEvent class
        // $(".video-person").hide();

        if (event.reason == "networkDisconnected") {
            $(".err-vid").show();
            $(".error_msg").html("Your network connection terminated.");
            $("body").addClass("flow_hidden");
        } else if (event.reason == "clientDisconnected") {
            //$(".err-vid").show();
            //$(".error_msg").html("Disconnected from the session.");
        }

    }
});

// For Google Chrome only, register your extension by ID,
// You can find it at chrome://extensions once the extension is installed
var extensionId = 'cnimhhbhonafpgpbpfggkjlolfkabhem';
OT.registerScreenSharingExtension('chrome', extensionId);
function screenshare() {
    $('#fullscreen').trigger('click');
    OT.checkScreenSharingCapability(function (response) {
        if (!response.supported || response.extensionRegistered === false) {
            alert('This browser does not support screen sharing.');
        } else if (response.extensionInstalled === false) {
            //alert(JSON.stringify(response));
            alert('Please install the screen sharing extension and load this page over HTTPS.');
        } else {
            // Screen sharing is available. Publish the screen.
            // Create an element, but do not display it in the HTML DOM:
            var screenContainerElement = document.createElement('div');
            screenSharingPublisher = OT.initPublisher(
                    screenContainerElement,
                    {videoSource: 'screen'},
            function (error) {
                if (error) {
                    exitFullscreen();
                    //alert('Something went wrong: ' + error.message);
                } else {
                    session.publish(
                            screenSharingPublisher,
                            function (error) {
                                if (error) {
                                    exitFullscreen();
                                    //alert('Something went wrong: ' + error.message);
                                }
                            });
                    $('#stop_screen_sharing').show();
                }
            });
        }
    });
}

//Listen for exceptions
OT.on("exception", function (event) {
    //alert(event.message);
    if (event.code == "1500") {
        event.message = "We can not connect to your camera/mic. Please make sure your camera/mic is connected and not being used by any other application."
    }
    $(".error_msg").html(event.message);
    $(".err-vid").show();
    $("body").addClass("flow_hidden");
});

$(document).ready(function () {

    $('body').on('click', '#refresh_page', function () {
        window.location.reload(true);
    });

    $('body').on('click', '#close_popup', function () {
        $(".vErrPop").hide();
    });

    $("body").on("click", "#end_session", function () {

        var res = confirm("Are your sure you want to end session?");
        if (res) {

            $("#refresh_page").hide();
            $(".error_msg_cont span").html('<i class="fa fa-check-circle-o"></i>');
            $(".error_msg").html("Session has been completed successfully.");
            $(".err-vid").show();

            clearInterval(sessionTimer);
            //////// Sending signal for end session to patient ///////
            session.signal({
                type: "doctor_end_session",
                data: '1'
            });

            session.disconnect();
        }
    });

    $('body').on('click', '#stop_screen_sharing', function () {
        $('#stop_screen_sharing').hide();
        // Cancel fullscreen for browsers that support it!
        exitFullscreen();
    });
});

// Exit From Full Screen
if (document.addEventListener)
{
    document.addEventListener('webkitfullscreenchange', exitHandler, false);
    document.addEventListener('mozfullscreenchange', exitHandler, false);
    document.addEventListener('fullscreenchange', exitHandler, false);
    document.addEventListener('MSFullscreenChange', exitHandler, false);
}

function exitHandler()
{
    if (!document.fullscreenElement && // alternative standard method
            !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement) {  // current working methods
        // Exit from full screen
        screenSharingPublisher.destroy();
        $('#stop_screen_sharing').hide();
        //$('#screen_share').show();
    } else {
        // Full screen mode
    }
}

// Whack fullscreen
function exitFullscreen() {
    screenSharingPublisher.destroy();
    $('#stop_screen_sharing').hide();
    //$('#screen_share').show();
    if (document.exitFullscreen) {
        document.exitFullscreen();
    } else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
    }
}