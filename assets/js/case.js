
$(document).ready(function(){

 $.ajax({
        type: "GET",
        success: function (data) {
            $('#tests').html(data);
        }
    });



    //$('#info_modal').on('show.bs.modal', function (e) {
    //    var button = $(e.relatedTarget);
    //    var appointment = button.data('appointment');
    //
    //    var modal = $(this)
    //    $.get(info_url+appointment+'/', function(data){
    //        modal.find('.modal-body').html(data);
    //        $('#info_modal').modal('handleUpdate');
    //    });
    //});
});

var delTest = function (id) {

  $.ajax({
      type: "GET",
      data:{"id_test": id},
      success: function (data) {
          $('#tests').html(data);
        }
  })


};

var addTest = function () {

  $.ajax({
      type: "GET",
      data:{"add_test": 1},
      success: function (data) {
          $('#tests').html(data);
        }
  })


};