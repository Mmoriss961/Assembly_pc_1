    $('.test_btn').click(function(){
        if ($('.test_inp').filter(function(){  return $(this).find(':checked').length === 0 }).length > 0 ) {
            alert('Пожалуйста, ответьте на вопросы из каждой категории');
            return false
        }
    });