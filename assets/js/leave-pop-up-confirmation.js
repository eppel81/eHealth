$(document).ready(function () {

    $("#pop-up").on("hide.bs.modal", function (event) {
        var url =  $('.add_file').attr('href');
        window.location.href=url;

    });

    //$("#leaveModalCancel").on('click', function () {
    //    $('#pop-up').modal('show');
    //});
});

