from django import forms
from .models import Booking, Lead


class LeadForm(forms.ModelForm):

    class Meta:
        model = Lead
        fields = ('email', 'name', 'description')


class PaymentForm(forms.ModelForm):
    email = forms.EmailField()
    promocode = forms.CharField(max_length=10, required=False)

    class Meta:
        model = Booking
        fields = ('start_date', 'end_date')

