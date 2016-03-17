$(document).ready(function(){
    $('#info_modal').on('show.bs.modal', function (e) {
        var button = $(e.relatedTarget);
        var appointment = button.data('appointment');

        var modal = $(this);
        $.get(info_url+appointment+'/', function(data){
            modal.find('.modal-body > .row').html(data);
            $('#info_modal').modal('handleUpdate');
        });
    });


    /* required logic for the doctor calendar view form */
    (function(){
        var form = $('#calendar-form'),
            day_css = 'tr > td input.weekday',
            day_shift_css = 'td input.shift-day',
            day_time_css = 'td input.time.day',
            night_shift_css = 'td input.shift-night',
            night_time_css = 'td input.time.night';

        form.on('change', day_css, function(){
            $(this).parents('tr').find(day_shift_css + ',' + night_shift_css).prop('disabled', !this.checked);
            var day_shift_dis = $(this).parents('tr').find(day_shift_css);
            var night_shift_dis = $(this).parents('tr').find(night_shift_css);
            if (day_shift_dis.prop('disabled')){
                $(day_shift_dis).attr('checked', false);
                $(this).parents('tr').find(day_time_css).prop('disabled', 'disabled');
                $(this).parents('tr').find(day_time_css).val('');

            }
            if (night_shift_dis.prop('disabled')){
                $(night_shift_dis).attr('checked', false);
                $(this).parents('tr').find(night_time_css).prop('disabled', 'disabled');
                $(this).parents('tr').find(night_time_css).val('');
            }

        });
        form.on('change', 'tr >' + day_shift_css, function(){
            $(this).parents('tr').find(day_time_css).prop('disabled', !this.checked);
            if ($(this).prop('checked')){
                var timeInputs = $(this).parents('tr').find(day_time_css);
                for (var i=0; i<timeInputs.length; i++){
                    var currentInput = timeInputs[i];
                    var value = $(currentInput).data('value');
                    $(currentInput).val(value);
            }
            }
            else
            {
                $(this).parents('tr').find(day_time_css).val('');
            }

        });
        form.on('change', 'tr >' + night_shift_css, function(){
            $(this).parents('tr').find(night_time_css).prop('disabled', !this.checked);
            if ($(this).prop('checked')){
                var timeInputs = $(this).parents('tr').find(night_time_css);
                for (var i=0; i<timeInputs.length; i++){
                    var currentInput = timeInputs[i];
                    var value = $(currentInput).data('value');
                    $(currentInput).val(value);
            }
            }
            else
            {
                $(this).parents('tr').find(night_time_css).val('');
            }
        });

        form.on('change', 'select.duration:last', function(){
            var duration = $('option:selected', this).val();
            $('select.duration option:selected').val(duration);
        });

    })();


    $('#calendar-form').on('submit', function(event){
        event.preventDefault();
        var self = $(this);
        self.find('button[type=submit]').prop('disabled', true).addClass('disabled');
        var url = self.attr('action');
        var all_input_disabled = $('input[disabled]');
        all_input_disabled.attr('data-disabled', true);
        all_input_disabled.prop('disabled', false);
        var data = $(this).serialize();
        $.ajax({
            url: url,
            data: data,
            method: 'post',
            success: function(data){
                /* if response is not empty, then this should be invalid form, containing error messages */
                if(data){
                    $(".week-form").html(data);
                } else {
                    all_input_disabled.prop('disabled', true);
                    $('.ui-datepicker-current-day').first().click();
                }
            }
        });
    });



    var get_next_2 = function(td){
        var cls = '.' + td.attr('class');
        return td.parent().next().children(cls);
    };
});