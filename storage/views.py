from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)
    

class FAQView(TemplateView):
    template_name = 'faq.html'

    def get(self, request):
        return render(request, self.template_name)


class BoxesViews(TemplateView):
    template_name = 'boxes.html'

    def get(self, request):
        return render(request, self.template_name)