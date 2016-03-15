$(function () {
    var all_notes_url = $('#id_show_all_notes').attr('href');
     $('#id_show_all_notes').click(function (e) {
        e.preventDefault();
        $.ajax({
            url: all_notes_url,
            method: 'get',
            success: function (data) {
                $('.all-notes-placeholder').html(data).parents('.modal').modal();
                $('.all-notes-placeholder').find('i').hide();
            }
        });
    });

    var get_all_notes = function (url, action, order, column){
        $.ajax({
            url: url,
            method: 'get',
            success: function (data) {
                $('.all-notes-placeholder').html(data);
                $('i', column).removeClass('hidea');
                $('.all-notes-placeholder').find('i.hidea').hide();
                $(".all-notes-placeholder").on('mouseenter', 'th', function(){
                    if ($('i', this).hasClass('hidea')){
                        $('i', this).show('1000');
                    }
                });

                $(".all-notes-placeholder").on('mouseleave', 'th', function(){
                    if ($('i', this).hasClass('hidea')){
                        $('i', this).hide('1000');
                    }
                });
                if (action == 'add'){
                    $(column).addClass(order);
                    $(column).find('i').removeClass('fa-sort-desc').addClass('fa-sort-asc');
                }
                if (action == 'remove'){
                    $(column).removeClass(order);
                    $(column).find('i').removeClass('fa-sort-asc').addClass('fa-sort-desc');
                }
            }
        });
    }


    $(".all-notes-placeholder").on('mouseenter', 'th', function(){
        if ($('i', this).hasClass('hidea')){
            $('i', this).show('1000');
        }
    });

    $(".all-notes-placeholder").on('mouseleave', 'th', function(){
        if ($('i', this).hasClass('hidea')){
            $('i', this).hide('1000');
        }
    });

    $(".all-notes-placeholder").on('click', 'th', function(){
        var column_name = $(this).attr('id');
        if ($(this).hasClass('desc')){
            var url = all_notes_url + '?key=' + column_name + '&order=desc';
            get_all_notes(url, 'remove', 'desc', 'th#' + column_name);
        }else{
            var url = all_notes_url + '?key=' + column_name;
            get_all_notes(url, 'add', 'desc', 'th#' + column_name);
        }
    });
});