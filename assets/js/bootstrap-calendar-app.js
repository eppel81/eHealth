$(function () {

    var appointmentsDate = [];
    var calendarContainer = $("#calendar");
    var doctorId = calendarContainer.attr('data-doctor');
    var url = calendarContainer.attr('data-url');
    var calendar = '';
    var successNextDayHeader = '';
    var failureNextDayHeader = '';
    var eventItem = function (event) {
     event.preventDefault();
            var url = $(this).attr('href');
                $.ajax({
                    url: url,
                    contentType: "text/html",
                    success: function(data){
                        $("#appointment-request").html(data);
                        $('#cur-doctor').modal('hide');
                        $('#appointment-request').modal('show');
                        $('.case').hide();
                }
            });
                    };

    var setCalendarView = function (calendar) {
        $('div.calendar-header').find('h3').text(calendar.getTitle());
        $('.span11.col-xs-11.cal-cell').text('Appointments');
        var cells = $('.pull-left.day-event.day-highlight');
        cells.css({
            'margin-left': '0',
            'margin-right': '0',
            'max-width': '100%',
            'width': '100%'
        });
        var cellWidth = $(cells).first().css('width');
        $('.pull-left.day-event.day-highlight.move-left').css('margin-left', '-' + cellWidth)
        $('.event-item').click(eventItem);

    };
    var date = new Date();
    var showCalendar = function() {
        $.ajax({
            url: url,
            type: "GET",
            data: {"doctor_id": doctorId},
            success: function (data) {
                if (data.success == true) {

                    var eventSource = data.appointments_time;
                    var startDate = data.start_date;
                    var templatePath = calendarContainer.attr('data-template');
                    appointmentsDate = data.appointments_date;
                    successNextDayHeader = data.success_next_day_header;
                    failureNextDayHeader = data.failure_next_day_header;

                    calendar = $(calendarContainer).calendar({
                        tmpl_path: templatePath,
                        view: 'day',
                        time_split: '15',
                        day: startDate,
                        events_source: eventSource,
                        time_start: '00:00',
		                time_end: '23:30'
                    });
                    setCalendarView(calendar);
                    getNextDate(calendar);
                    $('#day-prev, #day-next').removeClass('hidden');


                }
            }
        });



    };

    $('.show-schedule').on('click', showCalendar);



    $('#day-next, #day-prev').on('click', function () {
        var jump = $(this).attr('id');
        var nextDay = getNewDay(calendar.options.day, jump);

        if (nextDay){
            calendar.setOptions({day: nextDay});
            calendar.view();
            setCalendarView(calendar);
            getNextDate(calendar);
        }


    });

    var getNewDay = function (day, jump) {
        var index = 0;
        for (var i=0;i<appointmentsDate.length;i++){
            if (appointmentsDate[i]==day){
                index=i;
            }
        }
        var newDay = '';
        jump = jump.toLowerCase();
        if (jump == 'day-next'){
            newDay = appointmentsDate[index+1];
        }
        else if (jump == 'day-prev')
        {
            newDay = appointmentsDate[index-1]
        }
        return newDay
    };

    var getNextDate = function (calendar) {
        var nextDateString = getNewDay(calendar.options.day, 'day-next');
        var nextDateHeader = '';

        if (nextDateString){
            var nextDate = new Date(nextDateString);
            var nextDateFormat = calendar.locale.title_day.format(calendar.locale['d' + nextDate.getDay()], nextDate.getDate(), calendar.locale['m' + nextDate.getMonth()], nextDate.getFullYear());
            nextDateHeader = successNextDayHeader + nextDateFormat;
        }
        else
        {
            nextDateHeader = failureNextDayHeader;
        }

        $('.when').html('<h4>'+ nextDateHeader +'</h4>');
    };




});






