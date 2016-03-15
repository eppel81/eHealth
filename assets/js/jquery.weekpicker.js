$(document).ready(function() {
    var startDate;
    var endDate;

    var selectCurrentWeek = function() {
        window.setTimeout(function () {
            $('.week-picker').find('.ui-datepicker-current-day a').addClass('ui-state-active');
        }, 1);
    };

    $('.week-picker').datepicker( {
        showOtherMonths: true,
        selectOtherMonths: true,
        firstDay: 1,
        onSelect: function(dateText, inst) {
            var date = $(this).datepicker('getDate');
            var week_day = date.getDay();
            if (week_day > 0){
                startDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + 1);
                endDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + 7);
            }else{
                startDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() - 6);
                endDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());
            }
            var dateFormat = inst.settings.dateFormat || $.datepicker._defaults.dateFormat;
            var action = $('#calendar-form').attr('action');
            var first_day = $.datepicker.formatDate(dateFormat, startDate, inst.settings);
            var last_day = $.datepicker.formatDate( dateFormat, endDate, inst.settings );

            $.ajax({
                method: 'get',
                url: action,
                data: {
                    "first_day": first_day,
                    "last_day": last_day
                },
                success: function (data) {
                    $(".week-form").html(data);
                    $("#calendar-form > input[name='first_day']").val(first_day);
                    $("#calendar-form > input[name='last_day']").val(last_day);
                }
            });
            var url = $('.res').data('url');
            $('.res').removeClass('hidden');

            $.ajax({
                method: 'get',
                url: url,
                data: {
                     "first_day": first_day,
                     "last_day": last_day
                },
                success: function(data){

                    var get_next = function(td){
                        var columnIndex = td.parent().children().index(td);
                        var rowIndex = td.parent().parent().children().index(td.parent());
                        return $('.appointment>tbody>tr').eq(rowIndex + 1).find('td').eq(columnIndex);
                    };

                    var table = $('.res table>tbody');
                    table.find('td[class]').empty();
                    table.find('td.patient').removeClass('patient');
                    table.find('td.free').removeClass('free');
                    table.find('td.bordered').removeClass('bordered');
                    for(var i=0; i<data.length; i++) {
                        var cur_td = table.children('tr.' + data[i].time.replace(':', '\\:')).children('td.' + data[i].day);


                        if (data[i].patient){
                            template = "<a href='" + data[i].case_url + "'><div>Time: " + data[i].time;
                            template += " Patient: " + data[i].patient;
                            template += '</div></a>';
                        }else{
                            template = "<div>Time: " + data[i].time;
                            template += '</div>';
                        }



                        cur_td.html(template);
                        if (data[i].free){
                            cur_td.addClass('patient free');
                        }
                        else{
                            cur_td.addClass('patient');
                        }
                        var count_period = data[i].duration / 15;
                        if(count_period==1){
                            cur_td.addClass('bordered');
                        }
                        for(var j=1; j<count_period; j++){
                            var next_td = get_next(cur_td);
                            cur_td = next_td;
                            if (data[i].free){
                                cur_td.addClass('patient free');
                            }
                            else{
                                cur_td.addClass('patient');
                            }
                            if (j==count_period-1){
                                cur_td.addClass('bordered');
                            }
                        }
                    }
                }
            });
            selectCurrentWeek();
        },
        beforeShowDay: function(date) {
            var cssClass = '';
            if(date >= startDate && date <= endDate)
                cssClass = 'ui-datepicker-current-day';
            return [true, cssClass];
        },
        onChangeMonthYear: function(year, month, inst) {
            selectCurrentWeek();
        }
    });
    $('.week-picker .ui-datepicker-calendar tr').live('mousemove', function() { $(this).find('td a').addClass('ui-state-hover'); });
    $('.week-picker .ui-datepicker-calendar tr').live('mouseleave', function() { $(this).find('td a').removeClass('ui-state-hover'); });

});
 
(function($){
	var $calroot;

    function selectCurrentWeek() {
        window.setTimeout(function () {
            var t = $calroot.find('.ui-datepicker-current-day a');//.addClass('ui-state-active');
			t= t.closest('tr');
			t.find('td>a').addClass('ui-state-active');//.parent().addClass('ui-state-active');
        }, 1);
		
    }
	function onSelect(dateText, inst) { 
        var date = $(this).datepicker('getDate');
        startDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay());
        endDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + 6);
        var dateFormat = inst.settings.dateFormat || $.datepicker._defaults.dateFormat;
		$calroot.trigger('weekselected',{
			start:startDate,
			end:endDate,
			weekOf:startDate
		});
        selectCurrentWeek();
    }
	var reqOpt = {
		onSelect:onSelect,
		showOtherMonths: true,
        selectOtherMonths: true
	};
    $.fn.weekpicker = function(options){
		var $this = this;
		$calroot = $this;
		
		$this.datepicker(reqOpt);
		//events
		$dprow = $this.find('.ui-datepicker');
		
		$dprow.on('mousemove','tr', function() { 
			$(this).find('td a').addClass('ui-state-hover'); 
		});
		$dprow.on('mouseleave','tr', function() { 
			$(this).find('td a').removeClass('ui-state-hover'); 
		});
	};
})(jQuery);