$(function(){

    $('#appointment-request').on('change', '#id_follow_up', function(){
        $('.problem').toggle(1000);
        $('.comments').toggle(1000);
        $('.case').toggle(1000);
        $('.is_second_opinion').toggle(1000);
    });
});

