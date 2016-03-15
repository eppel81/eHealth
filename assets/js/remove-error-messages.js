$(document).ready(function () {

    $('form.health-history').on('change', 'input', function(){
        $(this).parents('div').next('div.has-error').children('span').text('');
    });

     $('form.lifestyle').on('change', 'input', function(){
        $(this).parents('div').children('div.has-error').children('span').text('');
        $(this).parents('td').next('td.has-error').children('span').text('');
     });

    $('form.billing').on('change', 'input', function(){
        $(this).parents('div').removeClass('has-error');
        $(this).parents('div').next('div.has-error').children('span').text('');
    });

    $('form.billing').on('change', 'select', function(){
        $(this).parents('div').removeClass('has-error');
        $(this).parents('div').next('div.has-error').children('span').text('');
    });

     $('form.account').on('change', 'select', function(){
        $(this).parents('div.form-group').removeClass('has-error');
        $(this).next('span').text('');
    });

    $('form.account, form.file-upload').on('change', 'input', function(){
        var parentDiv = $(this).parents('div.form-group');
        if ($(parentDiv).hasClass('has-error'))
        {
            $(parentDiv).removeClass('has-error');
            $(this).next('span').text('');
        }
    });

    $('form.appointment-request').on('change', 'input', function(){
        $(this).parent().removeClass('has-error');
        $(this).next('span').text('');
    });

     $('form.payment').on('change', 'input', function(){
        $(this).parent().removeClass('has-error');
        $(this).parent().next().children('span').text('');
    });

    $('form.appointment-request').on('change', 'select', function(){
        $(this).parent().removeClass('has-error');
        $(this).next('span').text('');
    });

    $('form.appointment-request').on('change', 'textarea', function(){
        $(this).parent().removeClass('has-error');
        $(this).next('span').text('');
    });
});