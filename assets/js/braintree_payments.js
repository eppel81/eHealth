$(document).ready(function () {

    //var url = $('#checkout').attr('action');

    $.ajax({
        //url: url,
        method: 'GET',
        dataType: 'JSON',

        success: function (data) {
            var clientTokenFromServer = data.client_token;
            braintree.setup(clientTokenFromServer, "dropin", {
                container: "payment-form",
                enableCORS: true,
                onReady: function(){
                    $('#checkout').children('input').removeClass('disabled');

                }

            });
        }
    });
});
