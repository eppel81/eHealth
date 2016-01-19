$(document).ready(function(){
    $('.alert').hide();
    $('#id_photo').on('change', function(event){
        console.log(this.files[0].size);
        if (this.files[0].size > 2*1024*1024){
            $('.alert').clone().appendTo('.photo-error');
            $('#id_photo').val('');
            $('.photo-error .alert').show();
            var timeout = 5000;
            setTimeout(function(){
                $('.photo-error .alert').alert('close');
            }, timeout);
        }
    });
});