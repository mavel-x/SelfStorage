from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from storage.models import Box, UnlockQR, Booking


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


@require_POST
@login_required
def unlock_box(request):
    user = request.user
    box_id = request.POST.get('box_id')
    box = get_object_or_404(Box, pk=box_id)
    booking = get_object_or_404(Booking, user=user, box=box)
    code = UnlockQR.create_for_box(box)
    title = 'Одноразовый QR-код для открытия бокса'
    body = render_to_string('qr_open.html', {
        'title': title,
        'customer_name': user.first_name,
        'box': box,
        'box_open_code': code.code,
    })
    send_html_email(title, body, user.email)
    return JsonResponse({'status': 'ok'})
