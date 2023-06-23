from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

from .models import User


class EmailAdminAuthenticationForm(AdminAuthenticationForm):
    username = forms.EmailField(label='Email', max_length=75)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if not user.username:
            user.username = user.email
        user.save()
        return user


class AccountChangeForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = PhoneNumberField(required=False)
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)
    password_old = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        password_old = cleaned_data.get('password_old')
        if (password1 or password2) and password1 != password2:
            self.add_error('password2', 'Пароли не совпадают.')
        if self.user and not check_password(password_old, self.user.password):
            self.add_error('password_old', 'Неправильный пароль.')
        return cleaned_data

    def update_user(self):
        if self.is_valid():
            data = self.cleaned_data
            fields = ['first_name', 'last_name', 'phone']
            for field in fields:
                if data.get(field):
                    setattr(self.user, field, data[field])
            if data.get('password1'):
                self.user.set_password(data['password1'])
            self.user.save()
