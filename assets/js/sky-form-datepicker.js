$(document).ready(function () {
      $('#start').datepicker({
		onSelect: function( selectedDate )
		{
			$('#finish').datepicker('option', 'minDate', selectedDate);
		}
	});
	$('#finish').datepicker({
		onSelect: function( selectedDate )
		{
			$('#start').datepicker('option', 'maxDate', selectedDate);
		}
	});
});


