$(function(){
    $('select[name=case] > option[value=1]').attr('selected', 'selected');

    $('input[type=file]').attr('accept', '.txt, .pdf, .doc, .docx, .csx, .xls, .xlsx, .gif, .png, .pjpeg');

    $('.add_files').on('change', 'div.file > div > input', function(event){
        event.preventDefault();
        if (!$(this).parents('.input-group').children('input').val()){
            return;
        }


        var add_file_block = $('.my_form').first().clone();

        var cur_count_form = parseInt($('#id_additionalfile_set-TOTAL_FORMS').val());
        $('#id_additionalfile_set-TOTAL_FORMS').val(cur_count_form+1);

        $.each(add_file_block.find('.file').find('input'), function(index, value){
//            $(this).parent.addClass('hidden');
            var id_number = $(this).attr('id');
            id_number = parseInt(id_number.match('[0-9]+')[0]);
            $(this).attr('id',  $(this).attr('id').replace($(this).attr('id').match('[0-9]+')[0], (id_number+1)));
            $(this).attr('name', $(this).attr('name').replace($(this).attr('name').match('[0-9]+')[0], (id_number+1)));
            $(this).val('');
        });

        $.each($('.test_file_record').find('input'), function(index, value){
            var id_number = $(this).attr('id');
            id_number = parseInt(id_number.match('[0-9]+')[0]);
            $(this).attr('id',  $(this).attr('id').replace($(this).attr('id').match('[0-9]+')[0], (id_number+1)));
            $(this).attr('name', $(this).attr('name').replace($(this).attr('name').match('[0-9]+')[0], (id_number+1)));
        });

        $.each($('.id').find('input'), function(index, value){
            var id_number = $(this).attr('id');
            id_number = parseInt(id_number.match('[0-9]+')[0]);
            $(this).attr('id',  $(this).attr('id').replace($(this).attr('id').match('[0-9]+')[0], (id_number+1)));
            $(this).attr('name', $(this).attr('name').replace($(this).attr('name').match('[0-9]+')[0], (id_number+1)));
        });

         $('.add_files').prepend(add_file_block);

        $.each($('.file').find('input'), function(index, value){
            if ($(this).val()){

//                $(this).prop('disabled', true);
                $(this).parent().find('span a').html('<span class="glyphicon glyphicon-floppy-remove"></span> Remove');
                $(this).parent().find('span a').addClass('for_delete');

            }else{
//                $(this).prop('disabled', false);
                $(this).parent().find('span a').html('<span class="glyphicon glyphicon-floppy-open"></span> Add');
                $(this).parent().find('span a').addClass('add_file');
                $(this).parent().find('span a').removeClass('for_delete');
            }
        });
    });

    $('.add_files').on('click', 'a.for_delete', function(event){
        event.preventDefault();
        var block_for_delete = $(this).parents('.my_form');

        var cur_count_form = parseInt($('#id_additionalfile_set-TOTAL_FORMS').val());
        $('#id_additionalfile_set-TOTAL_FORMS').val(cur_count_form-1);

        block_for_delete.remove();

    });
});