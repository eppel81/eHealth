$(document).ready(function () {
    $('.send-new').on('click', function (event) {
        event.preventDefault();
        var url = $(this).attr('href');
        $.ajax({
            url: url,
            method: 'GET',

            success: function (data) {
                $('.new-message-container').html(data).parents('.modal').modal('show');
                //var title = $('.postman').find('h1').text();
                //$('.modal-header').find('h2').text(title);
                //$('.postman').find('h1').text('');
                //$('textarea').addClass('form-control');
            }
        })
    })
});