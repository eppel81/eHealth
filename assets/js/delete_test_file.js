$(function(){
    $('.delete_file').click(function(event){
        event.preventDefault();
        $('#deleteModal').modal('toggle');
        $('.confirm').attr('action', $(this).attr('href'));
    });
});