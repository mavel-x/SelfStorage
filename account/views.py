import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from .models import User
from .forms import LoginForm, SignUpForm


def get_display_name(user: User):
    if user.first_name and user.last_name:
        return ' '.join((user.first_name, user.last_name))
    if name := (user.first_name or user.last_name):
        return name
    if user.username:
        return user.username
    return user.email


class AccountView(TemplateView):
    template_name = 'my-rent.html'

    def get(self, request, *args, **kwargs):
        user: User = self.request.user
        display_name = get_display_name(user)
        return render(request, self.template_name, {
            'display_name': display_name,
        })


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
            return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'error', 'errors': 'Неверный логин или пароль.'})

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'errors': form.errors})


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'index.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Добро пожаловать!')
        return JsonResponse({'status': 'ok'})

    def form_invalid(self, form):
        print()
        print(form.errors)
        return JsonResponse({
            'status': 'error',
            # 'errors':  json.dumps(form.errors, ensure_ascii=False),
            'errors': form.errors,
        })


def logout_view(request):
    logout(request)
    messages.success(request, 'До свидания!')
    return redirect('index')
