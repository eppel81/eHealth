
$(function(){

    $('form').on('submit', function(event){
        event.preventDefault();
        var action = $(this).attr('action');
        $.ajax({
            url: action,
            data: $(this).serialize(),
            method: 'POST',
            dataType:'JSON',
            error: function(xhr, status, error){
                        alert(error);
                   },
            success: function(data){

                if(data.success){
                    if (data.active_proc_num == 4){
                            $('#proccessModal').modal('hide');
                            var continueButton = $('.add_file');
                            $(continueButton).removeClass('next_to_process');
                            var link = data.url.toString();
                            $(continueButton).attr('data-url', '');
                            $(continueButton).attr('href', link);
                            $(continueButton).click(function(event){
                                event.preventDefault();
                                window.location.href = data.url;
                            });

                            $('.redirecting-text').find('h5').html(data.next_text);
                            $('.modal-header').find('h2').html(data.next_title);
                            $('.modal-footer').find('a').html(data.next_button);
                            $('#pop-up').modal('show');

                    }else{
                        if (data.redirect) {
                            window.location.href = data.url
                        }
                        else {
                            $.ajax({
                                url: data.url,
                                method: 'get',
                                success: function(data1){
                                    $('.form_content').html(data1);
                                    appProcess.changeMenuItem();
                                }
                            });
                        }
                    }
                }else{
                   if (data.errors){
                       for(var key in data.errors){
                            $('[name='+key+']').parent().addClass('has-error');
                            if ($('[name='+key+']').parent().hasClass('has-error') == true){
                                var new_error = '<span class="help-block">' + data.errors[key] + '</span>';
                                if(key=='height_ft'){
                                    $('[name='+key+']').next().next().html(new_error);
                                }else{
                                    $('[name='+key+']').next().html(new_error);
                                }
                            }
                       }
                   }else{
                        $('.alert-danger').addClass('in');
                   }
                }

            },
        });
    });
});