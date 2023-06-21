from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from .forms import LoginForm


class AccountView(TemplateView):
    template_name = 'my-rent.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'index.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Добро пожаловать!')
            return super().form_valid(form)
        messages.error(self.request, 'Неверный логин или пароль.')
        return redirect(reverse_lazy('index'), {'login_form': LoginForm()})

    def dispatch(self, request, *args, **kwargs):
        print(self.request.path)
        print(self.request.body)
        print()
        return super().dispatch(request, *args, **kwargs)






