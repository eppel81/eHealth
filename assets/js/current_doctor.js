$(document).ready(function(){
    $('.doctor-link').click(function(event){
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


});