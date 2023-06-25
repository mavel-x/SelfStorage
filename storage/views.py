import datetime

from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy

from .models import Storage, Box
from .forms import PaymentForm, LeadForm

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

        return render(request, self.template_name, context)


class PaymentFormViews(FormView):
    form_class = PaymentForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        if self.request.POST.get('change', '') == 'date':
            box_amount = self.change_date(form)

            return JsonResponse({
                'box_amount': box_amount,
            })

        #form.save()

        return JsonResponse({'status': 'ok'})

    def form_invalid(self, form):
        if self.request.POST.get('change', '') == 'date':
            box_amount = self.change_date(form)

            return JsonResponse({
                'box_amount': box_amount,
            })

        return JsonResponse({
            'status': 'error',
            'errors': form.errors,
        })

    def change_date(self, form):
        box = Box.objects.get(pk=self.request.POST['box'])
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        months_difference = relativedelta(end_date, start_date)
        months_count = (months_difference.years * 12) + months_difference.months
        if start_date.day != end_date.day:
            months_count += 1
        box_amount = box.price * months_count

        return box_amount