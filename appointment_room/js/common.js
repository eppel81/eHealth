// Tokbox Details
var apiKey = "45143532";
var tokbox_session_id = "1_MX40NTE0MzUzMn5-MTQ1MTYzMzc2MDcyMH5MTC92OXdJMmNER2xMMmdLaXlLVi9VNWV-UH4";
var token = "T1==cGFydG5lcl9pZD00NTE0MzUzMiZzaWc9ODkzODc4ZTU0Njk3N2Q5NmVhM2E0NmI1ZDY2YzQ3YjY2OWQ4MzQ0ZDpyb2xlPXB1Ymxpc2hlciZzZXNzaW9uX2lkPTFfTVg0ME5URTBNelV6TW41LU1UUTFNVFl6TXpjMk1EY3lNSDVNVEM5Mk9YZEpNbU5FUjJ4TU1tZExhWGxMVmk5Vk5XVi1VSDQmY3JlYXRlX3RpbWU9MTQ1MTYzMzc4OSZub25jZT0wLjIxMTE4MDgzMzcwNDg0MTg2JmV4cGlyZV90aW1lPTE0NTQyMjU3MzMmY29ubmVjdGlvbl9kYXRhPQ==";
var sessionMinutes = "30";
var sessionSeconds = "00";

// Default Website base url
var base_url = "https://vc.modal.es/";

//Doctor Detail
var doctor_info = {
    "Name": "Dr Ramazan Donmez",
    "Speciality": "Consultant Oncologist",
    "Location": "Oxford, UK"
};

//Patient Detail
var patient_info = {
    "Name": "Mr Phil Mitchel",
    "Age": "38 years",
    "Gender": "Male",
    "Weight": "80 kg",
    "Location": "Oxford, UK"
};

// Previous Saved Notes
var notes = [
    "Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum",
    "Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum",
    "Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum",
    "Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum",
    "Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum"
];

// Dicom Files
var dicom_files = [
    "brain_001.dcm",
    "brain_002.dcm",
    "1439364438.dcm",
];

$(window).load(function () {

    // Showing Doctor and Patient Detail 
    $(".doctor_name").html(doctor_info.Name);
    $(".doctor_short_detail").html(doctor_info.Speciality + ", " + doctor_info.Location);
    $(".patient_short_detail").html("Gender: " + patient_info.Gender + ", " + patient_info.Age);
    $.each(patient_info, function (key, value) {
        if (key == "Name") {
            $(".patient_name").html(value);
        } else {
            $("#patient_detail").append("<li>" + key + ": " + value + "</li>");
        }
    });

    // Showing Previous Saved Notes
    $.each(notes, function (key, value) {
        $(".note_msg_block ul").append("<li>" + value + "</li>");
    });

    // Showing DICOM Files
    $.each(dicom_files, function (key, value) {
        $("#dicom_files").append("<li><h1><a href='javascript:void(0);' data-uri='" + value + "' title='Click to view in Dicom Viewer' class='dicom_file'>" + value + "</a></h1><a href='javascript:void(0);' data-uri='" + value + "' class='discuss_dicm_viewer'>Discuss</a></li></li>");
    });

});

$(document).ready(function () {

    // Reload Page
    $('body').on('click', '#refresh_page', function () {
        window.location.reload(true);
    });

    // Stop or Play Video
    $('body').on('click', '#controllVideo', function () {
        var selected = $(this);
        var action = selected.attr('alt');
        if (action == 'stop')
        {
            turnOffMyVideo();
            selected.children("img").attr('src', 'images/cross0010.png');
            selected.attr({'alt': 'start', 'title': 'Turn on video'});
        }
        else if (action == 'start')
        {
            turnOnMyVideo();
            selected.children("img").attr('src', 'images/cross_001.png');
            selected.attr({'alt': 'stop', 'title': 'Turn off video'});
        }

    });

    // Stop or Play Audio
    $('body').on('click', '#controllAudio', function () {
        var selected = $(this);
        var action = selected.attr('alt');
        if (action == 'stop')
        {
            turnOffMyAudio();
            selected.children("img").attr('src', 'images/cross003.png');
            selected.attr({'alt': 'start', 'title': 'Turn on video'});
        }
        else if (action == 'start')
        {
            turnOnMyAudio();
            selected.children("img").attr('src', 'images/cross0030.png');
            selected.attr({'alt': 'stop', 'title': 'Turn off video'});
        }
    });

    // Making Notes 
    $("#text_msg").bind('keypress', function (e) {
        if (e.which == 13) { // When key pressed is "Enter" key.
            makeNotes();
        }
    });

    $('body').on('click', '#make_note', function () {
        makeNotes();
    });

    // Text Chat
    $('body').on('click', '#send_msg', function () {
        send_chat_msg();
    });

    $("#chat_msg").bind('keypress', function (e) {
        if (e.which == 13) {  // When key pressed is "Enter" key.
            send_chat_msg();
        }
    });

    // Expand Collapse Patient Detail/Notes and DICOM Viewer 
    $('body').on('click', '#chat_blk', function () {
        $('.left_dicom, .dicom_vr').toggleClass('auto_dicom');
        $('.chat_block').slideToggle();
    });

    //Expand Collapse Patient Main Vidoe and Notes/DICOM Viewer  
    $('body').on('click', '.close_penal', function () {
        
        if ($(this).hasClass('rt-close')) {
            $(this).removeClass('rt-close');
            $(this).addClass('lt-open');
            $(this).attr('title', 'Click to show side panel');
        } else {
            $(this).removeClass('lt-open');
            $(this).addClass('rt-close');
            $(this).attr('title', 'Click to hide side panel');
        }
        
        if (!$('.leftscreen01').hasClass('fullwidth')) {
            $('.leftscreen01').css('width', '59.4%');
        }
        $('.leftscreen01').toggleClass('fullwidth');

        if (!$('.left_screen0002').hasClass('fullwidth')) {
            $('.left_screen0002').css('width', '59.4%');
        }
        $('.left_screen0002').toggleClass('fullwidth');

        if (!$('.left_box').hasClass('hiddenpen')) {
            $('.left_box').css('width', '40%');
        }
        $('.left_box').toggleClass('hiddenpen');
    });

    // Show Hide files Div
    $('body').on('click', '#view_investigation', function () {
        if ($('.investigations_sec').is(':visible')) {
            $('.investigations_sec').hide();
        } else {
            $('.investigations_sec').show();
        }
    });

    // View file in DICOM Viewer
    $('body').on('click', '.dicom_file, .discuss_dicm_viewer', function () {
        $('#dicom_viewer_blk').append('<iframe id="dicom_viewer" src=""></iframe>');
        var url = $(this).attr('data-uri');
        $('#dicom_viewer').attr('src', 'dwv-0.10.1/viewers/mobile/index.html?input=' + base_url + url);
    });

    // Full Screen Mode
    $('body').on('click', '#fullscreen', function () {
        var docElement, request;

        //docElement = document.documentElement;
        docElement = document.getElementById("dicom_viewer_blk");
        request = docElement.requestFullScreen || docElement.webkitRequestFullScreen || docElement.mozRequestFullScreen || docElement.msRequestFullScreen;

        if (typeof request != "undefined" && request) {
            request.call(docElement);
            //$('#screen_share').hide();
        }

    });
});

// Reverse Resize divs 
$.ui.plugin.add("resizable", "alsoResizeReverse", {
    start: function () {
        var that = $(this).resizable("instance"),
                o = that.options;

        $(o.alsoResizeReverse).each(function () {
            var el = $(this);
            el.data("ui-resizable-alsoresizeReverse", {
                width: parseInt(el.width(), 10), height: parseInt(el.height(), 10),
                left: parseInt(el.css("left"), 10), top: parseInt(el.css("top"), 10)
            });
        });
    },
    resize: function (event, ui) {
        var that = $(this).resizable("instance"),
                o = that.options,
                os = that.originalSize,
                op = that.originalPosition,
                delta = {
                    height: (that.size.height - os.height) || 0,
                    width: (that.size.width - os.width) || 0,
                    top: (that.position.top - op.top) || 0,
                    left: (that.position.left - op.left) || 0
                };

        $(o.alsoResizeReverse).each(function () {
            var el = $(this), start = $(this).data("ui-resizable-alsoresize-reverse"), style = {},
                    css = el.parents(ui.originalElement[0]).length ?
                    ["width", "height"] :
                    ["width", "height", "top", "left"];

            $.each(css, function (i, prop) {
                var sum = (start[prop] || 0) - (delta[prop] || 0);
                if (sum && sum >= 0) {
                    style[prop] = sum || null;
                }
            });

            el.css(style);
        });
    },
    stop: function () {
        $(this).removeData("resizable-alsoresize-reverse");
    }
});

// Making Notes
function makeNotes() {
    var txt_msg = $.trim($("#text_msg").val());
    $("#text_msg").val("");
    if (txt_msg != "") {
        $(".note_msg_block ul").append("<li>" + txt_msg + "</li>");
        $(".note_msg_block").scrollTop($(".note_msg_block")[0].scrollHeight);
        $("#text_msg").focus();
    } else {
        $("#text_msg").focus();
    }
}

// Session Timer
function sessionTimer(element, type)
{
    sessionTimer = setInterval(function () {
        var el = document.getElementById(element);
        sessionMinutes = parseInt(sessionMinutes, 10);
        sessionSeconds = parseInt(sessionSeconds, 10);
        if (sessionMinutes > 0) {
            var minute_text = "0" + sessionMinutes;
        } else {
            var minute_text = "00";
        }
        var second_text = sessionSeconds;
        if (sessionSeconds < 10)
        {
            sessionSeconds = "0" + sessionSeconds;
        }
        if ((sessionMinutes == 0) && (sessionSeconds < 10))
        {

        }
        if (sessionMinutes < 9)
        {
            el.innerHTML = "0" + sessionMinutes + ':' + sessionSeconds;
        }
        else
        {
            el.innerHTML = sessionMinutes + ':' + sessionSeconds;
        }

        if (sessionSeconds == 0) {
            if (sessionMinutes == 0) {
                clearInterval(sessionTimer);
                if (type == "doctor") {
                    //$("#end_session").trigger("click");
                }
                return;
            } else {
                sessionMinutes--;
                sessionSeconds = 60;
            }
        }
        sessionSeconds--;
    }, 1000);
}

// Text Chat
function send_chat_msg() {
    var chat_msg = $.trim($("#chat_msg").val());
    $("#chat_msg").val("");
    var name = $("#display_name").html();
    if (chat_msg != "") {
        $(".chat_meg_block ul").append("<li><div class=\"comment-right\"><h6>" + name + "</h6><p>" + chat_msg + "</p></div></li>");
        $(".chat_meg_block").scrollTop($(".chat_meg_block")[0].scrollHeight);
        $("#chat_msg").focus();
        session.signal({
            type: "text_chat",
            data: {msg: chat_msg, name: name, my_connection: myId}
        });
    } else {
        $("#chat_msg").focus();
    }
}

// Stop Displaying video
function turnOffMyVideo()
{
    publisher.publishVideo(false);
}

// Start Displaying video
function turnOnMyVideo()
{
    publisher.publishVideo(true);
}

// Stop Publishing audio
function turnOffMyAudio()
{
    publisher.publishAudio(false);
}

// Start Publishing audio
function turnOnMyAudio()
{
    publisher.publishAudio(true);
}

// Detect Browser
function detectBrowser() {
    var userAgent = navigator.userAgent.toLowerCase(),
            browser = '',
            version = 0;

    $.browser.chrome = /chrome/.test(navigator.userAgent.toLowerCase());

// Is this a version of IE?
    if ($.browser.msie) {
        userAgent = $.browser.version;
        userAgent = userAgent.substring(0, userAgent.indexOf('.'));
        version = userAgent;
        browser = "Internet Explorer";
    }

// Is this a version of Chrome?
    if ($.browser.chrome) {
        userAgent = userAgent.substring(userAgent.indexOf('chrome/') + 7);
        userAgent = userAgent.substring(0, userAgent.indexOf('.'));
        version = userAgent;
        // If it is chrome then jQuery thinks it's safari so we have to tell it it isn't
        $.browser.safari = false;
        browser = "Chrome";
    }

// Is this a version of Safari?
    if ($.browser.safari) {
        userAgent = userAgent.substring(userAgent.indexOf('safari/') + 7);
        userAgent = userAgent.substring(0, userAgent.indexOf('.'));
        version = userAgent;
        browser = "Safari";
    }

// Is this a version of Mozilla?
    if ($.browser.mozilla) {
        //Is it Firefox?
        if (navigator.userAgent.toLowerCase().indexOf('firefox') != -1) {
            userAgent = userAgent.substring(userAgent.indexOf('firefox/') + 8);
            userAgent = userAgent.substring(0, userAgent.indexOf('.'));
            version = userAgent;
            browser = "Firefox";
        }
        // If not then it must be another Mozilla
        else {
            //browser = "Mozilla (not Firefox)";
            browser = "Internet Explorer";
        }
    }

// Is this a version of Opera?
    if ($.browser.opera) {
        userAgent = userAgent.substring(userAgent.indexOf('version/') + 8);
        userAgent = userAgent.substring(0, userAgent.indexOf('.'));
        version = userAgent;
        browser = "Opera";
    }

    return browser;
// Now you have two variables, browser and version
// which have the right info

}