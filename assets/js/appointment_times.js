$(document).ready(function(){
    $('.appointment-date').change(function(){
        var url = $('option:selected', this).data('url');
        if(!url){
            return;
        }
        $.ajax({
            url: url,
            contentType: "text/html",
            success: function(data){
                $('.times').html(data);
            }
        });
    });
    $('.appointment-date').change();
});