from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from django.views import View
from .forms import BookingForm
import requests
import json
import environ

# Load environment variables
env = environ.Env()
environ.Env.read_env()

def get_token():
    url = 'http://127.0.0.1:8000/api/token/login/'
    data = {
        'username': env('USERNAME'),
        'password': env('PASSWORD')
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        response_dict = response.json()
        return response_dict.get('access')
    return None

def get_auth_header():
    token = get_token()
    if token:
        return {'Authorization': f'JWT {token}'}
    return {}

def index(request):
    return render(request, 'restaurant/index.html')

def about(request):
    return render(request, 'restaurant/about.html')

def menu(request):
    url = f"http://127.0.0.1:8000{reverse('api:menu')}"
    headers = get_auth_header()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        menu_items = response.json()
    else:
        menu_items = []
    return render(request, 'restaurant/menu.html', context={'menu_items': menu_items})

def menu_item(request, pk):
    url = f"http://127.0.0.1:8000{reverse('api:menu-detail', kwargs={'pk': pk})}"
    headers = get_auth_header()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        menu_item = response.json()
    else:
        menu_item = {}
    return render(request, 'restaurant/menu_item.html', context={'menu_item': menu_item})

class Book(View):
    form_class = BookingForm
    template_name = 'restaurant/book.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = {
                'name': form.cleaned_data['name'],
                'no_of_guests': form.cleaned_data['no_of_guests'],
                'booking_date': form.cleaned_data['booking_date'],
            }
            headers = get_auth_header()
            url = f"http://127.0.0.1:8000{reverse('api:bookings')}"
            response = requests.post(url, data=data, headers=headers)
            if response.status_code == 201:
                return render(request, self.template_name, {'form': BookingForm()})
        return render(request, self.template_name, {'form': form})

def bookings(request):
    date = request.GET.get('date', timezone.now().date())
    url = f"http://127.0.0.1:8000{reverse('api:bookings')}?date={date}"
    headers = get_auth_header()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        bookings = response.json()
    else:
        bookings = []
    return render(request, 'restaurant/bookings.html', context={'bookings': bookings})
