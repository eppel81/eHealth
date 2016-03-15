$(document).ready(function () {

    $('#id_recipients').on('change', function () {
        var url = $(this).parent('div').data('url');
        if (url)
        {
        var pk = $(this).val();
        $.ajax({
            url: url,
            data: {'pk': pk},
            method: 'GET',

            success: function (data) {
                $('#id_case').find('option').remove().end();
                $.each(data, function (key, value) {
                    $('#id_case').append('<option value=' + key + '>' + value + '</option>');
                });
            }
        })
        }
    })
});