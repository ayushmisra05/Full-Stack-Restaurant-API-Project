from django import forms
from django.utils import timezone


class BookingForm(forms.Form):
    name = forms.CharField(max_length=255, required=True, label='Name')
    no_of_guests = forms.IntegerField(initial=6, required=True, min_value=1, label='Number of Guests')
    booking_date = forms.DateField(initial=timezone.now().date, required=True, label='Booking Date')
