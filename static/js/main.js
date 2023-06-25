$(document).on('submit', '#login-form', function (e){

    e.preventDefault();
    let csrftoken = Cookies.get('csrftoken');
    $.ajax({
        type: 'POST',
        url: '/account/login/',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            email: $('#login-email').val(),
            password: $('#login-password').val(),
        },
        success: function (data) {
            if (data.status === 'error') {
                $('#login-form-errors').html(data.errors);
            }
            else if (data.status === 'ok') {
                let urlParams = new URLSearchParams(window.location.search);
                if (urlParams.has('next')) {
                    window.location.href = urlParams.get('next');
                } else {
                    location.reload();
                }
            }
        }
    })
})

$(document).on('submit', '#signup-form', function (e){
    e.preventDefault();
    let csrftoken = Cookies.get('csrftoken');
    $.ajax({
        type: 'POST',
        url: '/account/signup/',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            first_name: $('#signup-first-name').val(),
            last_name: $('#signup-last-name').val(),
            email: $('#signup-email').val(),
            password1: $('#signup-password1').val(),
            password2: $('#signup-password2').val(),
        },
        success: function (data) {
            if (data.status === 'error') {
                for (let field in data.errors) {
                    let errorList = $('<ul class="errorlist">');
                    for (let error of data.errors[field]) {
                        errorList.append($('<li>').text(error));
                    }
                    $('#error_' + field).html(errorList);
                }
            }
            else if (data.status === 'ok') {
                let urlParams = new URLSearchParams(window.location.search);
                if (urlParams.has('next')) {
                    window.location.href = urlParams.get('next');
                } else {
                    location.reload();
                }
            }
        }
    })
})

$(document).on('submit', '#lead-form', function (e){
    e.preventDefault();
    let csrftoken = Cookies.get('csrftoken');
    let buttonLead = $('#lead-form button ')
    $.ajax({
        type: 'POST',
        url: '/lead/',
        headers: {'X-CSRFToken': csrftoken},
        data: $(this).serialize(),
        beforeSend: function () {
            buttonLead.text('Заявка обрабатывается');
            buttonLead.attr({
                'type': 'button',
                'disabled':'disabled',
            });
        },
        success: function (data) {
            if (data.status === 'ok') {
                $('[id|=lead-error]').text('');

                buttonLead.text('Заявка принята');
                buttonLead.attr({
                    'type': 'button',
                    'disabled':'disabled',
                });
                buttonLead.removeClass('SelfStorage__bg_orange SelfStorage__btn2_orange')
                buttonLead.addClass('SelfStorage__bg_green SelfStorage__btn2_green')
            }
            else if (data.status === 'error') {
                $('#lead-error').text('Форма заполнена не верно!');

                for (let field in data.errors) {
                    let errorList = $('<ul class="errorlist">');
                    for (let error of data.errors[field]) {
                        errorList.append($('<li>').text(error));
                    }

                    $('#lead-error-' + field).html(errorList);

                buttonLead.text('Рассчитать стоимость');
                buttonLead.attr('type','submit');
                buttonLead.removeAttr('disabled')
                }
            }
        }
    })
})

