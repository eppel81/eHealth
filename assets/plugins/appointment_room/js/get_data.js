
$.ajax({
    method: 'get',
    //async: false,

    success: function (data) {

        localStorage.setItem('apiKey', data.api_key);
        localStorage.setItem('tokbox_session_id', data.session_id);
        localStorage.setItem('token', data.token);
        localStorage.setItem('doctor_info', JSON.stringify(data.doctor_info));
        localStorage.setItem('patient_info', JSON.stringify(data.patient_info));
        localStorage.setItem('notes', data.notes);


    }
});

