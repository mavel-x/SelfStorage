from django.shortcuts import render
from django.views.generic import TemplateView


class AccountView(TemplateView):
    template_name = 'my-rent.html'

    def get(self, request):
        return render(request, self.template_name)
