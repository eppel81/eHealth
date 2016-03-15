var accountDetailsPage = {};

$(document).ready(function () {
    var photoError = $('.photo-error');

    $('#id_photo').on('change', function () {
        $(photoError).addClass('hidden');
        if (this.files[0].size > 2 * 1024 * 1024) {
            clearTimeout(accountDetailsPage.alertTimeout);
            $('#id_photo').val('');
            $(photoError).removeClass('hidden');
            var timeout = 5000;
            accountDetailsPage.alertTimeout = setTimeout(function () {
                $(photoError).addClass('hidden');
            }, timeout);
        }
    });

    $('#close_alert_button').on('click', function () {
        $(photoError).addClass('hidden');
        clearTimeout(accountDetailsPage.alertTimeout);
    })
});