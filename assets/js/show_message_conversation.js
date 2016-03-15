$(document).ready(function(){
    $('.view').click(function(event){
       event.preventDefault();
        var url = $(this).attr('href');
        if($('table#pm_messages').attr('name')=='Inbox'){
                        $(this).parents('tr').removeClass('unread-message');}

        $.ajax({
            url: url,
            method: 'GET',

            success: function (data) {
                $('.message-container').html(data).parents('.modal').modal('show');
                var title = $('.postman').find('h1').text();
                $('.modal-header').find('h2').text(title);
                $('.postman').find('h1').text('');
                $('textarea').addClass('form-control');
            }
        })
    });
});