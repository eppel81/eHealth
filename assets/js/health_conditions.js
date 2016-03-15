$(document).ready(function () {
    var radio = $('.conditions > label > input');

    $.each(radio, function (index, value) {
        var new_name = '.' + value.name + '_info';
        $(new_name).addClass('hidden');
    });

    radio.on('change', function () {
        var new_name = '.' + this.name + '_info';
        if ($(this).is(':checked') && $(this).val() == 'True') {
            $(new_name).slideDown();
            $(new_name).removeClass('hidden');
            $(new_name).find('textarea').removeAttr('style');
        }
        else {
            $(new_name).slideUp();
        }
    });

    radio.change();
});