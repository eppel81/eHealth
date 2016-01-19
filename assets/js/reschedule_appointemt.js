$(document).ready(function(){
    $( "#appointment_date" ).change(function() {
        $.ajax({
            dataType: 'json',
            url: time_url+this.value+'/',
            success: function (data, textStatus) {
                $("#appointment_time").find("*").remove();
                $.each(data, function(i, val) {
                    $("#appointment_time").append('<option value="'+i+'">'+val+'</option>');
                });
            }
        });
    });
});