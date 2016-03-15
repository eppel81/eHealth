var uploadFilesPage = {};

$(document).ready(function () {

    var checkSize = function () {

        if ($(this)[0].files.length > 0) {

            var file_size = $(this)[0].files[0].size;

            if (file_size > 100 * 1024 * 1024) {
                clearTimeout(uploadFilesPage.alertTimeout);
                $(this).val('');
                $('.file-error').removeClass('hidden');

                var timeout = 5000;
                uploadFilesPage.alertTimeout = setTimeout(function () {
                    $('.file-error').addClass('hidden');
                }, timeout);
            }
            else {
                $('.file-error').addClass('hidden');
            }
        }

    };


    var form = $(this).find('form.form-horizontal');
    form.on("change", "input:file", checkSize);

    form.submit(function(){
        $('[type=submit]', this).prop('disabled', 'true');
    });

});

var closeAlert = function () {
    $('.file-error').addClass('hidden');
    clearTimeout(uploadFilesPage.alertTimeout);
};

