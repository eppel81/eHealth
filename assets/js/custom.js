$(function(){
    /* dismiss bootstrap alerts after N seconds */
    (function(){
        var timeout = 5000;
        setTimeout(function(){
            $('.alert-dismissible').alert('close');
        }, timeout);
    })();

    /* i18n - language selector */
    (function(){
        var lang_list = $('ul.anyclass');
        var form = $('form', lang_list);
        $('li > a', lang_list).click(function(e){
            var selector = 'select[name="language"]>option[value="' + $(this).data('lang') + '"]';
            e.preventDefault();
            form.find(selector).prop('selected', true);
            form.submit();
        });
    })();
});