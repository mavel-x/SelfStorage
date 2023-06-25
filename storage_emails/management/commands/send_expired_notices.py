from collections import defaultdict

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone

from account.models import User
from storage.models import Booking, Invoice
from storage_emails.utils import send_html_email


def find_expired_booking_invoices() -> dict[User, list[Invoice]]:
    active_bookings = Booking.objects.active()
    invoices = Invoice.objects.filter(booking__in=active_bookings)
    paid_invoices = invoices.filter(paid=True)
    expired_booking_invoices = paid_invoices.filter(pays_until__lt=timezone.localdate())
    expired_invoices_by_user = defaultdict(list)
    for invoice in expired_booking_invoices:
        if invoice.pays_until.day == timezone.localdate().day:
            expired_invoices_by_user[invoice.booking.user].append(invoice)
    return expired_invoices_by_user


def send_notices(invoices_by_user: dict[User, list[Invoice]]):
    for user, invoices in invoices_by_user.items():
        title = 'Ваш арендный платеж просрочен!'
        body = render_to_string('rent_expired.html', {
            'title': title,
            'name': user.first_name,
            'invoices': invoices,
        })
        send_html_email(title, body, user.email)


def main():
    expiring_booking_invoices_by_user = find_expired_booking_invoices()
    send_notices(expiring_booking_invoices_by_user)


class Command(BaseCommand):
    help = "Send monthly notices to users whose bookings expired."

    def handle(self, *args, **options):
        main()
