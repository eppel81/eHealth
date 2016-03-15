$(document).ready(function () {

    $('#continuePaymentButton').on('click', function () {
        event.preventDefault();
        $('form#checkout').find('input').click();
        $('#cancelPayment').attr('disabled', 'disabled');
        $(this).attr('disabled', 'disabled');

    });
    $('.enter-appointment').on('click', function (event) {
        event.preventDefault();
        $('#id_consult_payment_confirmation').modal('show');
        var url = $(this).attr('data-token');
        var enterRoomUrl = $(this).attr('href');
        $('#continuePayment').attr('action', enterRoomUrl);

        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'JSON',
            data: {'case': $(this).attr('data-case')},
            success: function (data) {
                $('#deposit').text(data.deposit);
                $('#consult-rate').text(data.consult_rate);
                $('#net-amount').text(data.net_amount);
                $('.appointment-price').removeClass('hidden');
                var clientTokenFromServer = data.client_token;
                $('#dropin-container').html('');

                braintree.setup(clientTokenFromServer, "dropin", {
                    container: "dropin-container",
                    form: "checkout",
                    onPaymentMethodReceived: function (obj) {
                        $('#continuePayment').append("<input type='hidden' name='payment_method_nonce' value='" + obj.nonce + "'></input>");
                        $('#continuePayment').submit();
                    },
                    onReady: function () {
                        $('#cancelPayment').removeAttr('disabled');
                        $('#continuePaymentButton').removeAttr('disabled');

                    }
                });


            }


        });


    });
    $('#cancelPayment').click(function () {
        window.location.reload();
    });


});