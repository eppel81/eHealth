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
        }
    });


            $('select[name=patient]').select2({});
            $('select[name=reason]').select2({});


});