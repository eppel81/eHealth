$(document).ready(function(){
    var doctorSchedule = $('.doctor-link');
    $(doctorSchedule).click(function(event){
        event.preventDefault();
        $.ajax({
            url: $(this).attr('href'),
            contentType: "text/html",
            success: function(data){
                $("#cur-doctor").html(data);
                $('#cur-doctor').modal('show');
            }
        });

    });
    var chosenDoctor = $(doctorSchedule).attr('data-doctor');
    if (chosenDoctor){
        $(doctorSchedule).click();

    }



});