document.getElementById('account-edit-button').addEventListener('click', e => {
    e.preventDefault()
    let phoneField = document.getElementById('account-phone')
    phoneInitialValue = phoneField.value;
    phoneField.disabled = false
    if (phoneField.value === 'не указан') {
        phoneField.value = '';
    }
    document.getElementById('account-password-old').disabled = false
    document.getElementById('account-edit-button').style.display = 'none'
    document.getElementById('account-save-button').style.display = 'inline-block'
    document.getElementById('account-cancel-edit-button').style.display = 'inline-block'
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

document.getElementById('account-cancel-edit-button').addEventListener('click', e => {
    let phoneField = document.getElementById('account-phone')
    phoneField.value = phoneInitialValue;
    $('#account-phone').prop('disabled', true);
    $('#account-password-old').prop('disabled', true);
    location.reload();
})
