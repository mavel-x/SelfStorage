$('[id^="open-box-"]').click(function() {
    let csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    let box_id = this.id.split('-')[2];
    let button = this;
    $.ajax({
        url: '/email/unlock-box/',
        type: 'POST',
        data: {
            box_id: box_id,
            csrfmiddlewaretoken: csrfToken
        },
        success: function(response) {
            alert('Одноразовый QR-код для открытия бокса отправлен на ваш e-mail адрес');
            $(button).prop('disabled', true);
        },
        error: function(response) {
            if (response.status === 404) {
                alert('Похоже, мы не можем открыть этот бокс для Вас. Если этот бокс арендован Вами и оплачен, ' +
                    'пожалуйста, свяжитесь с нами по телефону или напишите нам на e-mail.');
            }
        }
    });
});
