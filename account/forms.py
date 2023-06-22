from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.forms import UserCreationForm

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
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.save()
        return user
