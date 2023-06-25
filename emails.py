from django.conf import settings
from django.core import mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from account.models import User
from storage.models import Box, UnlockQR


def send_html_email(subject: str, body: str, email_to: str):
    with mail.get_connection() as connection:
        email = mail.EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.EMAIL_SEND_FROM,
            to=[email_to],
            connection=connection,
        )
        email.content_subtype = 'html'
        email.send()


def send_opening_qr(user_id: int, box_id: int):
    user = get_object_or_404(User, pk=user_id)
    box = get_object_or_404(Box, pk=box_id)
    code = UnlockQR.create_for_box(box)
    title = 'Одноразовый QR-код для открытия бокса'
    body = render_to_string('qr_open.html', {
        'title': title,
        'customer_name': user.first_name,
        'box': box,
        'box_open_code': code.code,
    })
    send_html_email(title, body, user.email)
