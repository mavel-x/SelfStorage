from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from account.models import User
from storage.models import Box, UnlockQR, Booking, Invoice
from storage_emails.utils import send_html_email


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


def send_invoice(user: User, invoice: Invoice):
    title = 'Счет за аренду складского бокса'
    body = render_to_string('invoice.html', {
        'title': title,
        'user': user,
        'invoice': invoice,
    })
    send_html_email(title, body, user.email)
