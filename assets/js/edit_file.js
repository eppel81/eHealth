$(function(){
    $('select[name=case] > option[value=1]').attr('selected', 'selected');
    $('.file').submit(function(event){
        event.preventDefault();
        var action = $(this).attr('action');
        var add_data = {
            'type': $('#id_type').val(),
            'description': $('#id_description').val(),
            'case': $('#id_case option:selected').val(),
        };
        add_data = $.param(add_data);
        var data_form = $(this).serialize();
        data_form += '&' + add_data;
        $.ajax({
            url: action,
            data: data_form,
            method: 'POST',
            error: function(xhr, status, error){
                        alert(error);
                   },
            success: function(data){
                if(data.success){
                    window.location.href = data.url;
                }else{
                   for(var key in data.errors){
                        $('[name='+key+']').parent().addClass('has-error');
                        if ($('[name='+key+']').parent().hasClass('has-error') == true){
                            $('[name='+key+']').next().text(data.errors[key]);
                        }
                }
                }

            },
        });
    });
});