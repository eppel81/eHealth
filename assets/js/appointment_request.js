$(document).ready(function(){
    var url = '';
    $('.free-time').click(function(event){
        event.preventDefault();
        url = $(this).attr('href');
//        $('#cur-doctor').modal('hide');
//
//    });
//
//    $('#cur-doctor').on('hide.bs.modal', function(){



            $.ajax({
                url: url,
                contentType: "text/html",
                success: function(data){
                    $("#appointment-request").html(data);
                    $('#appointment-request').modal('show');
                }
            });
        });

});