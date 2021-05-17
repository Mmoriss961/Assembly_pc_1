function showRegisterForm(){
    $('.errorlist  li ').hide();
    $('#alert_log,#alert2_log').hide();
    $('.loginBox').fadeOut('fast',function(){

        $('.registerBox').fadeIn('fast');
        $('.login-footer').fadeOut('fast',function(){
            $('.register-footer').fadeIn('fast');
        });
        $('.modal-title').html('Регистрация');
    });
    $('.error').removeClass('alert alert-danger').html('');

}
function showLoginForm(){

    $('#loginModal .registerBox').fadeOut('fast',function(){
        $('.errorlist  li ').hide();
        $('#alert_reg,#alert2_reg').hide();
        $('.loginBox').fadeIn('fast');

        $('.register-footer').fadeOut('fast',function(){
            $('.login-footer').fadeIn('fast');
        });

        $('.modal-title').html('Авторизация');
    });
    $('.error').removeClass('alert alert-danger').html('');
}

function openLoginModal(){
    showLoginForm();
    setTimeout(function(){
        $('#loginModal').modal('show');
    }, 230);

}
function openRegisterModal(){
    showRegisterForm();
    setTimeout(function(){
        $('#loginModal').modal('show');
    }, 230);

}

$('body').on('hidden.bs.modal', '.modal', function (){
   //$('.modal-body').find('textarea,input').val('');
   $('#alert_reg, #alert2_reg, #alert_log , #alert2_log').hide();
});

$(document).on('submit', '#login_form', function (e) {

    e.preventDefault();
    var login_form = $('#login_form');
    var action = login_form.attr('action');
    var method = login_form.attr('method');
    var data_ = login_form.serialize();

    $.ajax({
        type: method,
        url: action,
        data: data_,
        success: function (data, status) {

            if ($(data).find('.alert-danger').length > 0) {
                $('.modal-custom').html(data);
                openLoginModal();
                $('#alert_log').show();
                $('.errorlist  li ').show();
            }
            else {
                if ($(data).find('.alert-success').length > 0) {

                    $('.modal-custom').html(data);
                    $('#login_form').empty();
                    openLoginModal();
                    $('#alert2_log').show();
                     setTimeout(window.location.reload.bind(window.location), 2000);}

                else
                    alert("Ошибка")

            }
        }
    });
    return false;
});


$(document).on('submit', '#reg_form', function (e) {

    e.preventDefault();
    var reg_form = $('#reg_form');
    var action = reg_form.attr('action');
    var method = reg_form.attr('method');
    var data_ = reg_form.serialize();

    $.ajax({
        type: method,
        url: action,
        data: data_,
        success: function (data, status) {

            if ($(data).find('.alert-danger').length > 0) {
                $('.modal-custom').html(data);
                openRegisterModal();
                $('#alert_reg').show();
                  $('.errorlist  li ').show();
            }
            else {
                if ($(data).find('.alert-success').length > 0) {

                    $('.modal-custom').html(data);
                    $('#reg_form').empty();
                    openRegisterModal();
                    $('#alert2_reg').show();
                    //location.reload();
                    setTimeout(window.location.reload.bind(window.location), 2000);}

                else
                    alert("Ошибка")

            }
        }
    });
    return false;
});
