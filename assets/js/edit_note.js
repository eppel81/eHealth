$(function () {
    $('.note-link').click(function (e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr('href'),
            method: 'get',
            success: function (data) {
                $('.note-placeholder').html(data).parents('.modal').modal("show");
                    if(
                        tinymce.editors.length > 0){
                        tinymce.remove();
                    }
                        tinymce.init({selector:'textarea.tinymce',
                        plugins: [
                            "advlist autolink lists charmap hr pagebreak",
                            "searchreplace wordcount visualblocks visualchars fullscreen",
                            "insertdatetime nonbreaking save table contextmenu directionality",
                            "paste textcolor colorpicker textpattern"
                        ],
                        statusbar: false
                    });

            }
        });
    });

    $('.note-placeholder').on('submit', '#id_note_edit', function (e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            method: 'post',
            data: $(this).serialize(),
            success: function (data) {
                if (!data) {
                    $('#id_edit_case_modal').modal('hide');
                    tinymce.remove();
                }
                else {
                    for (var key in data.errors) {
                        $('[name=' + key + ']').parent().addClass('has-error');
                        if ($('[name=' + key + ']').parent().hasClass('has-error') == true) {
                            $('[name=' + key + ']').next().text(data.errors[key]);
                        }
                    }
                }


            }


        });

    });



});