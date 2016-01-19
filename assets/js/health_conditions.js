$(document).ready(function(){
    var radio = $('.conditions > label > input');
    radio.change(function(){
      var new_name = '.' + this.name + '_info';
      if ($(this).is(':checked') && $(this).val() == 'True') {
          // $(new_name).removeClass('hidden').addClass('show');
          $(new_name).fadeIn('slow');
        }
      else{
          // $(new_name).removeClass('show').addClass('hidden');
          $(new_name).fadeOut('slow');
        }
    });

    radio.change();
});