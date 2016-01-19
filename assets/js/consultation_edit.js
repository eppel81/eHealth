$(document).ready(function(){
//    $('#id_doctor').chained('#id_appointment_date');
//    $('#id_appointment_date').chained('#id_appointment_time');
//
//    $('#id_doctor').on('change',function(){
//    var id_doctor = $('option:selected', this).val();
//        $.ajax({
//            url: Urls['doctor_date'](id_doctor),
//            method: 'get',
//            success: function(){},
//        });
//    });

    $('#id_appointment_date').remoteChained({
        parents: '#id_doctor',
        url: $('#id_doctor').parent().data('url'),
    });

    $('#id_appointment_time').remoteChained({
        parents: '#id_doctor, #id_appointment_date',
        url: $('#id_appointment_date').parent().data('url'),
    });
});