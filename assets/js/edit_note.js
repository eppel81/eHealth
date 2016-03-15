$(function () {
    $('.note-link').click(function (e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr('href'),
            method: 'get',
            success: function (data) {
                $('.note-placeholder').html(data).parents('.modal').modal("show");

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