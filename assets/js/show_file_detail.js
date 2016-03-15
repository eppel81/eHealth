
var getFileDetail = function ( id_file) {
    var url = $('#id_view_detail').attr('data-target');
    $.ajax({
        url: url,
        data: {"file": id_file},
        method: 'GET',
        success: function (data) {
            console.log(data);
            $('#id_note_detail').modal('toggle');
            $('#id_note_container').html(data);
        }
    })
};