from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy

from .models import Storage, Box
from .forms import LeadForm

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


class LeadViews(FormView):
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


class OrderView(TemplateView):
    template_name = 'order.html'

    def get(self, request, *args, **kwargs):
        #pk = Box.objects.get(pk=kwargs['pk'])
        print(kwargs['pk'])
        return render(request, self.template_name)