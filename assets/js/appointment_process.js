var appProcess = {};

$(document).ready(function () {
 $('.menu_proccess').find('a').first().addClass('active_num font-bold');

    appProcess.changeMenuItem = function () {
        var currentMenuItem = $('.active_num');
        $(currentMenuItem).parents('li').next().find('a').addClass('active_num font-bold');
        $(currentMenuItem).removeClass('active_num font-bold');
    }
});