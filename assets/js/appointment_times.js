$(document).ready(function () {
    $('#make_appointment').click(function (event) {
        event.preventDefault();
        var url = $('#appointment_time option:selected').data('url');
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