function openFBModal(isError){
    //showFBForm();
    $('.FBbox').fadeIn('fast',function(){
        $('.modal-title').html('Обратная связь');

        setTimeout(function(){
            $('#FBModal').modal('show');

            if(isError) {
                $('.form-control').val('');
            }
        }, 230);
    });
}

$('body').on('hidden.bs.modal', '.modal', function (){
   //$('.modal-body').find('textarea,input').val('');
     //$('.FBbox').find('form').reset();
    //$('.FBbox').find('form').trigger("reset");
   $('#alert_fb, #alert2_fb').hide();
   $('.errorlist li').hide();
});

/*function showFBForm(){

    $('.FBbox').fadeIn('fast',function(){

        $('.modal-title').html('Обратная связь');
    });
}*/

$(document).on('submit', '#fb_form', function (e) {

    e.preventDefault();
    var fb_form = $('#fb_form')
    var action = fb_form.attr('action');
    var method = fb_form.attr('method');
    var data_ = fb_form.serialize();

    $.ajax({
        type: method,
        url: action,
        data: data_,
        success: function (data, status) {

            if ($(data).find('.alert-danger').length > 0) {
                $('.modal-custom1').html(data);
                openFBModal(0);
                $('#alert_fb').show();
            } else {
                if ($(data).find('.alert-success').length > 0) {
                    $('.modal-custom1').html(data);
                    $('#fb_form').empty();
                    openFBModal(1);
                    $('#alert2_fb').show();
                    //location.reload();
                    setTimeout(window.location.reload.bind(window.location), 2000);
                } else {
                    alert('Ошибка');
                }
            }
        }
    });
    return false;
});