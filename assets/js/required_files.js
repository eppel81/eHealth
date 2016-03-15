$(document).ready(function () {

    var fileLabel = $('label[for="id_result_report_or_record"]')[0];
    var fileLabelValue = fileLabel.innerText;

    var type = $('#id_type');
    var typeValue = $(type).find('option:selected')[0].value;

    if (typeValue == 1) {

        $(fileLabel).empty();
        $(fileLabel).append("* " + fileLabelValue);

    }

    $(type).on('change', function () {
        $(fileLabel).empty();

        if (this.value == 1) {

            $(fileLabel).append("* " + fileLabelValue)
        }
        else {
            $(fileLabel).append(fileLabelValue)
        }
    })

});