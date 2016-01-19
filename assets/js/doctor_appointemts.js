$(document).ready(function(){
    $('#info_modal').on('show.bs.modal', function (e) {
        var button = $(e.relatedTarget);
        var appointment = button.data('appointment');

        var modal = $(this)
        $.get(info_url+appointment+'/', function(data){
            modal.find('.modal-body').html(data);
            $('#info_modal').modal('handleUpdate');
        });
    });
});