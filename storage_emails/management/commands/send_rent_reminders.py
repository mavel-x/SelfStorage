from collections import defaultdict
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone

from account.models import User
from storage.models import Booking, Invoice
from storage_emails.utils import send_html_email


REMINDER_PERIODS = (
    timedelta(weeks=4),
    timedelta(weeks=2),
    timedelta(weeks=1),
    timedelta(days=3),
)


def reminder_due(invoice: Invoice):
    return invoice.pays_until - timezone.localdate() in REMINDER_PERIODS


def find_expiring_booking_invoices() -> dict[User, list[Invoice]]:
    active_bookings = Booking.objects.filter(terminated=False)
    invoices = Invoice.objects.filter(booking__in=active_bookings)
    paid_invoices = invoices.filter(paid=True)

    expiring_invoices_by_user = defaultdict(list)
    for invoice in paid_invoices:
        if reminder_due(invoice):
            expiring_invoices_by_user[invoice.booking.user].append(invoice)

    return expiring_invoices_by_user


def send_reminders(invoices_by_user: dict[User, list[Invoice]]):
    for user, invoices in invoices_by_user.items():
        title = 'Напоминание об арендном платеже'
        body = render_to_string('rent_due.html', {
            'title': title,
            'customer_name': user.first_name,
            'invoices': invoices
        })
        send_html_email(title, body, user.email)


def main():
    expiring_booking_invoices_by_user = find_expiring_booking_invoices()
    send_reminders(expiring_booking_invoices_by_user)


class Command(BaseCommand):
    help = "Send reminders to users whose bookings expire soon."

    def handle(self, *args, **options):
        main()
