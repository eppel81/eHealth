$(document).ready(function () {

    var enterAppointmentButtons = $('a.enter-appointment');
    for (var i=0; i<enterAppointmentButtons.length; i++){
        var enterAppointmentButton = enterAppointmentButtons[i];
        var availableTime = $(enterAppointmentButton).attr('data-available');
     if (availableTime){
         var availableText = '';
         if (availableTime==0){
            availableText = 'You can enter the Appointment Room'
         }
         else {
             availableText = 'The Appointment Room will be open in ' + availableTime + ' min'

         }
         var cells = $(enterAppointmentButton).parents('tr').children('td').length;
         var messageAvailable = "<tr><td colspan='" + cells + "' class='text-center'><b>" + availableText + "</b></td></tr>";
         $(enterAppointmentButton).parents('tr').before(messageAvailable)
     }
    }

});