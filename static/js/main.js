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
    document.getElementById('account-phone').disabled = false
    document.getElementById('account-password-old').disabled = false
    document.getElementById('account-edit-button').style.display = 'none'
    document.getElementById('account-save-button').style.display = 'inline-block'
    document.getElementById('account-hidden-fields').hidden = false
    document.getElementById('account-new-password-container').hidden = false
    document.getElementById('account-password-old-label').innerText = 'Старый пароль'
    document.getElementById('account-password-old').value = ''
})

document.getElementById('account-save-button').addEventListener('click', () => {
    setTimeout(() => {
        document.getElementById('account-phone').disabled = true
        document.getElementById('account-password1').disabled = true
        document.getElementById('account-edit-button').style.display = 'inline-block'
        document.getElementById('account-save-button').style.display = 'none'
    }, 0)
})