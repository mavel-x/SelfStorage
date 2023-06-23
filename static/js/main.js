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
                location.reload();
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
                location.reload();
            }
        }
    })
})


document.getElementById('account-edit-button').addEventListener('click', e => {
    e.preventDefault()
    // document.getElementById('account-email').disabled = false
    let phoneField = document.getElementById('account-phone')
    phoneField.disabled = false
    if (phoneField.value === 'не указан') {
        phoneField.value = '';
    }
    document.getElementById('account-password-old').disabled = false
    document.getElementById('account-edit-button').style.display = 'none'
    document.getElementById('account-save-button').style.display = 'inline-block'
    document.getElementById('account-hidden-fields').hidden = false
    document.getElementById('account-new-password-container').hidden = false
    document.getElementById('account-password-old-label').innerText = 'Старый пароль'
    document.getElementById('account-password-old').value = ''
})


function displayErrors(errors, errorElement) {
    if (errors) {
        var errorList = $('<ul class="errorlist long-form-errors"></ul>');
        for (var i = 0; i < errors.length; i++) {
            var errorItem = $('<li></li>').text(errors[i]);
            errorList.append(errorItem);
        }
        errorElement.html(errorList);
    }
}

$(document).on('submit', '#account-change-form', function (e) {
    e.preventDefault();
    $('#account-change-form-errors').html('');
    let errorElements = document.querySelectorAll('[id^="error_"]');
    errorElements.forEach(function(element) {
        element.innerHTML = '';
    });
    let csrftoken = Cookies.get('csrftoken');
    $.ajax({
        type: 'POST',
        url: '/account/change/',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            first_name: $('#account-first-name').val(),
            last_name: $('#account-last-name').val(),
            email: $('#account-email').val(),
            phone: $('#account-phone').val(),
            password1: $('#account-new-password1').val(),
            password2: $('#account-new-password2').val(),
            password_old: $('#account-password-old').val(),
        },
        success: function (data) {
            if (data.status === 'error') {
                $('#account-change-form-errors').html(data.errors);
                if (data.form_errors) {
                    // Display errors for each field
                    for (var field in data.form_errors) {
                        if (data.form_errors.hasOwnProperty(field)) {
                            var errorElement = $('#error_account_' + field);
                            displayErrors(data.form_errors[field], errorElement);
                        }
                    }
                }
            } else if (data.status === 'ok') {
                $('#account-phone').prop('disabled', true);
                $('#account-password-old').prop('disabled', true);
                location.reload();
            }
        }
    })
})
