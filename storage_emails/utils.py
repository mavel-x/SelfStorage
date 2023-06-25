from django.conf import settings
from django.core import mail


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
