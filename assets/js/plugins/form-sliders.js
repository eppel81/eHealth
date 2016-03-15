var FormSliders = function () {

    return {
        
        //Form Sliders
        initFormSliders: function () {
	        // Regular slider
	        $('#slider1').slider({
		      min: 0,
		      max: 500,
		      slide: function(event, ui)
		      {
		        $('#slider1-value').text(ui.value);
		      }
	        });
	        
	        // Range slider
	        $('#slider2').slider({
		      min: 0,
		      max: 500,
		      range: true,
		      values: [75, 300],
		      slide: function(event, ui)
		      {
		        $('#slider2-value1').text(ui.values[0]);
		        $('#slider2-value2').text(ui.values[1]);
		      }
	        });
	        
	        // Step slider
	        $('#slider3').slider({
		      min: 0,
		      max: 500,
		      step: 100,
		      slide: function(event, ui)
		      {
		        $('#slider3-value').text(ui.value);
		      }
	        });

	         // Rounded Regular slider
	        $('#slider1-rounded').slider({
		      min: 0,
		      max: 500,
		      slide: function(event, ui)
		      {
		        $('#slider1-value-rounded').text(ui.value);
		      }
	        });
	        
	        // Rounded Range slider
	        $('#slider2-rounded').slider({
		      min: 0,
		      max: 500,
		      range: true,
		      values: [75, 300],
		      slide: function(event, ui)
		      {
		        $('#slider2-value1-rounded').text(ui.values[0]);
		        $('#slider2-value2-rounded').text(ui.values[1]);
		      }
	        });
	        
	        // Rounded Step slider
	        $('#slider3-rounded').slider({
		      min: 0,
		      max: 500,
		      step: 100,
		      slide: function(event, ui)
		      {
		        $('#slider3-value-rounded').text(ui.value);
		      }
	        });

				var value1 = $('#slider-rate-value1').val();
			if (!(value1)) {
				value1 = 0;
			}
				var value2 = $('#slider-rate-value2').val();

			if (!(value2)) {
				value2 = 300;
			}
			$('#slider_rate').slider({

		      min: 0,
		      max: 300,
		      range: true,
		      values: [value1, value2],
		      slide: function(event, ui)
		      {
		        $('#slider-rate-value1').val(ui.values[0]);
		        $('#slider-rate-value2').val(ui.values[1]);
		      }
	        });
        }

    };
    
}();