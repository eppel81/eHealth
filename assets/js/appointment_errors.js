$(document).ready(function () {


    $('.appointment-request').submit(function (event) {
        event.preventDefault();
        var action = $(this).attr('action');
        var add_data = {
            'patient': $('#id_patient').val(),
            'doctor': $('#id_doctor').val(),
            'appointment_time': $('#id_appointment_time').val(),
        };
        add_data = $.param(add_data);
        var data_form = $(this).serialize();
        data_form += '&' + add_data;
        $.ajax({
            url: action,
            data: data_form,
            method: 'POST',
            error: function (xhr, status, error) {
                alert(error);
            },
            success: function (data) {
                if (data.success) {
                    $('.add_file').attr('href', data.next_url);
                    $('.redirect').attr('href', data.case_url);
                    $('.redirecting-text').find('h5').html(data.next_text);
                    $('.modal-header').find('h2').html(data.next_title);
                    $('.modal-footer').find('a').html(data.next_button);
                    if (!(data.next_url)) {
                        $('.add_file').on('click', function () {
                            $('#pop-up').modal('hide');
                        })
                    }
                    if (data.next_url == '#proccessModal') {
                        $('.add_file').addClass('next_to_process');
                    }

                    $('.next_to_process').on('click', function (event) {
                        event.preventDefault();
                        $.ajax({
                            url: $(this).data('url'),
                            method: 'get',
                            success: function (data) {
                                $('#pop-up').modal('hide');
                                $('.form_content').html(data);
                                $('#proccessModal').modal('show');


                            }
                        });
                    });


                    $('#leaveModalForm').submit(function (event) {
                        event.preventDefault();
                        $.ajax({
                            url: data.cancel_url,
                            method: 'GET',
                            success: function (data) {
                                $('#leaveModal').modal('hide');
                            }
                        })

                    });


                    $('.appointment_create').val(data.id);
                    $('#paymentConfirmation').modal('hide');
                    $('#pop-up').modal('toggle');
                } else {
                    for (var key in data.errors) {
                        $('[name=' + key + ']').parent().addClass('has-error');
                        if ($('[name=' + key + ']').parent().hasClass('has-error') == true) {
                            $('[name=' + key + ']').next().text(data.errors[key]);

                        }
                        if (key == '__all__') {
                            var self = $('.non-field-errors');
                            self.addClass('has-error alert alert-danger fade in');
                            var app_link = data.errors[key] + '. Please follow this ' + '<a href="' + data.case_url + '">appointment link</a>';
                            self.find('span').html(app_link);

                        }

                    }
                }

            },
        });
    });

    $('form#checkout').on('submit', function (event) {
        event.preventDefault();
        $(this).find('input').click();
    });

    $('#paymentConfirmationForm').on('submit', function (event) {
        event.preventDefault();
        $('form#checkout').submit();
    });

    $('#cancelPayment').click(function () {

        window.location.reload();
    });

    $('button.appointment-request').on('click', function (event) {
        event.preventDefault();

        var checkUrl = $(this).data('check');
        var add_data = {
            'patient': $('#id_patient').val(),
            'doctor': $('#id_doctor').val(),
            'appointment_time': $('#id_appointment_time').val()
        };
        add_data = $.param(add_data);
        var data_form = $('form.appointment-request').serialize();
        data_form += '&' + add_data;
        $.ajax({
            url: checkUrl,
            data: data_form,
            method: 'POST',
            success: function (data) {
                if (data.success == true) {
                    $('#appointment-request').modal('hide');
                    $('#paymentConfirmation').modal('show');
                    var deposit = $('form.appointment-request').attr('data-deposit');
                    $('.deposit').html(deposit);
                    var url = $('#paymentConfirmationForm').attr('action');
                    $.ajax({
                        url: url,
                        method: 'GET',
                        dataType: 'JSON',
                        success: function (data) {
                            var clientTokenFromServer = data.client_token;
                            $('#dropin-container').html('');

                            braintree.setup(clientTokenFromServer, "dropin", {
                                container: "dropin-container",
                                form: "checkout",
                                onPaymentMethodReceived: function (obj) {
                                    $('form.appointment-request').append("<input type='hidden' name='payment_method_nonce' value='" + obj.nonce + "'></input>");
                                    $('form.appointment-request').submit();
                                    $('#cancelPayment').attr('disabled', 'disabled');
                                    $('#continuePayment').attr('disabled', 'disabled');
                                },
                                onReady: function () {
                                    $('#cancelPayment').removeAttr('disabled');
                                    $('#continuePayment').removeAttr('disabled');
                                }
                            });


                        }
                    });

                }
                else {
                    for (var key in data.errors) {
                        $('[name=' + key + ']').parent().addClass('has-error');
                        if ($('[name=' + key + ']').parent().hasClass('has-error') == true) {
                            $('[name=' + key + ']').next().text(data.errors[key]);

                        }
                        if (key == '__all__') {
                            var self = $('.non-field-errors');
                            self.addClass('has-error alert alert-danger fade in');
                            var app_link = data.errors[key] + '. Please follow this ' + '<a href="' + data.case_url + '">appointment link</a>';
                            self.find('span').html(app_link);

                        }

                    }
                }

            }
        });


    });


});