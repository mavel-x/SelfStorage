import datetime

from pathlib import Path

from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy


from .models import (
    Booking,
    Box,
    Discount,
    Invoice,
    Storage,
)
from .forms import PaymentForm, LeadForm
from account.models import User
from storage_emails.views import send_invoice

class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    

class FAQView(TemplateView):
    template_name = 'faq.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class BoxesViews(TemplateView):
    template_name = 'boxes.html'

    def get(self, request):
        context = {
            'storages': Storage.objects.all(),
            'boxes': Box.objects.filter(is_busy=False),
        }
        return render(request, self.template_name, context)


class LeadFormViews(FormView):
    form_class = LeadForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()

        return JsonResponse({'status': 'ok'})

    def form_invalid(self, form):
        return JsonResponse({
            'status': 'error',
            'errors': form.errors,
        })


class BookingView(TemplateView):
    template_name = 'booking.html'

    def get(self, request, *args, **kwargs):
        default_months_count = 3
        min_months_count = 1

        box = Box.objects.get(pk=kwargs['pk'])
        box_amount = box.price * default_months_count
        start_date = datetime.datetime.today()
        end_date = start_date + relativedelta(months=default_months_count)
        max_start_date = start_date + relativedelta(months=min_months_count)
        data_format ='%Y-%m-%d'

        context = {
            'box': box,
            'box_amount': box_amount,
            'start_date': start_date.strftime(data_format),
            'end_date': end_date.strftime(data_format),
            'max_start_date': max_start_date.strftime(data_format),
        }

        if self.request.user.id:
            context['email'] = self.request.user.email
        else:
            context['email'] = ''

        return render(request, self.template_name, context)


class PaymentFormViews(FormView):
    form_class = PaymentForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        box = Box.objects.get(pk=self.request.POST['box'])
        promocode = form.cleaned_data['promocode']
        box_amount = self.calculate_amount(form, box.price)
        user_password = ''

        if self.request.POST.get('change', ''):
            return JsonResponse({
                'box_amount': box_amount,
            })

        if Discount.objects.filter(
            promocode__iexact=promocode,
            start_date__lte=datetime.datetime.today(),
            end_date__gte=datetime.datetime.today(),
        ).exists():
            discount = Discount.objects.get(promocode__iexact=promocode)
        else:
            discount = None

        user, created = User.objects.get_or_create(email=form.cleaned_data['email'])

        if created:
            user_password = User.objects.make_random_password()
            user.set_password(user_password)
            user.username = f'{user.email.split("@")[0]}_id{user.id}'
            user.save()



        booking = Booking.objects.create(
            user=user,
            box=box,
            start_date=form.cleaned_data['start_date'],
            end_date=form.cleaned_data['end_date'],
        )

        invoice = Invoice.objects.create(
            booking=booking,
            pays_until=datetime.datetime.today() + datetime.timedelta(days=3),
            amount=box_amount,
            discount=discount,
            paid=True,
        )

        box.is_busy = True
        box.save()

        domain = Path(self.request.build_absolute_uri())

        send_invoice(user, invoice, user_password, domain.parent)

        return JsonResponse({'status': 'ok'})

    def form_invalid(self, form):
        if self.request.POST.get('change', ''):
            box = Box.objects.get(pk=self.request.POST['box'])
            box_amount = self.calculate_amount(form, box.price)

            return JsonResponse({
                'box_amount': box_amount,
            })

        return JsonResponse({
            'status': 'error',
            'errors': form.errors,
        })

    def calculate_amount(self, form, price: int) -> int:
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        promocode = form.cleaned_data['promocode']
        discount = 0
        months_difference = relativedelta(end_date, start_date)
        months_count = (months_difference.years * 12) + months_difference.months

        if Discount.objects.filter(
                promocode__iexact=promocode,
                start_date__lte=datetime.datetime.today(),
                end_date__gte=datetime.datetime.today(),
        ).exists():
            discount = Discount.objects.get(promocode__iexact=promocode).percent

        if start_date.day != end_date.day:
            months_count += 1

        box_amount = round((price - (price / 100 * discount)) * months_count)

        return box_amount

