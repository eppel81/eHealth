$(function() {

    $('.event-item').click(function (event) {
        console.log('yes');
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
        });

    $("#appointment_time").select2({
        minimumResultsForSearch: Infinity
    });
  });