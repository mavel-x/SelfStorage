from django.contrib import messages, admin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from storage.models import Booking
from .models import User
from .forms import LoginForm, SignUpForm, AccountChangeForm


class AccountView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('index')
    template_name = 'my-rent.html'

    def get(self, request, *args, **kwargs):
        user: User = self.request.user
        bookings = Booking.objects.filter(user=user, terminated=False).prefetch_related('box', 'box__storage')

        return render(request, self.template_name, {
            'bookings': bookings,
        })


class AccountChangeView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('index')

    form_class = AccountChangeForm
    template_name = 'my-rent.html'
    success_url = reverse_lazy('account')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form: AccountChangeForm):
        form.update_user()
        messages.success(self.request, 'Данные сохранены.')
        return JsonResponse({'status': 'ok'})

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'form_errors': form.errors})


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
        return JsonResponse({'status': 'error', 'form_errors': form.errors})


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
            'errors': form.errors,
        })


def logout_view(request):
    logout(request)
    messages.success(request, 'До свидания!')
    return redirect('index')


def index_redirect(request):
    return redirect('index')
