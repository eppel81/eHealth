$(document).ready(function(){
    var $datepicker = $('#sandbox-container');
    function TwoDigitMonth(m) {
        return (m < 9) ? '0' + (m+1) : (m+1);
    }
    function TwoDigitDate(d) {
        return (d < 10) ? '0' + d : d;
    }
    $datepicker.datepicker({
        startDate: "now",
        language: calendar_language,
        daysOfWeekHighlighted: "0,6",
        todayHighlight: true,
        toggleActive: false
    });
    $datepicker.data({date: new Date(calendar_current_date)});
    $datepicker.datepicker('update');
    $datepicker.on('changeDate', function (e) {
        var d=$datepicker.datepicker('getDate');
        var res = d.getFullYear()+'-'+ TwoDigitMonth(d.getMonth())+'-'+ TwoDigitDate(d.getDate());
        window.location.href=calendar_url+res;
    });
    $("#appointment_time").chosen();

});