$(document).ready(function(){
    $.ajax({
        url: $('select[name=doctor]').data('url'),
        method: 'get',
        success: function(data){
//            var all_doctors = [];
//            for(var i=0; i < data.length; i++){
//                var doctor = JSON.parse(data[i]);
//                all_doctors.push(doctor);
//            }
//            $('select[name=doctor]').select2({
            $('select[name=doctor]').select2({
                data: data
            });
            $('.select2.select2-container.select2-container--default').css('width', '100%');
        }
    });


//            $('select[name=patient]').select2({});
//            $('select[name=reason]').select2({});

    $('.input-daterange input').each(function() {

        $(this).datepicker({
                autoclose: true
            }

        );
    });

    $(window).resize(function() {
        var bodywidth = $('.doctor-block').width();
        $(".select2-container").width(bodywidth);
    }).resize();



});
