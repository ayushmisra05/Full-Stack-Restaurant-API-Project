from django.test import Client
from restaurant.models import Booking, Menu
from random import randint


BOOKINGS = {
    1: {'name': 'test1'},
    2: {'name': 'test2', 'no_of_guests': randint(1, 11)},
    3: {'name': 'test3', 'no_of_guests': randint(1, 11)},
    4: {'name': 'test4', 'no_of_guests': randint(1, 11)},
}

MENU_ITEMS = {
    1: {'title': 'ApplePie', 'price': 13.78},
    2: {'title': 'VanillaLatte', 'price': 3.99, 'inventory': randint(0, 11)},
    3: {'title': 'Icecream', 'price': 5.00, 'inventory': randint(0, 11)},
    4: {'title': 'IrishCoffee', 'price': 7.89, 'inventory': randint(0, 11)},
}


class UserMixin:
    @staticmethod
    def create_user(username, password):
        url = 'http://127.0.0.1:8000/auth/users/'
        data = {'username': username, 'password': password}
        return Client().post(url, data=data)

    @staticmethod
    def get_token(username, password):
        url = 'http://127.0.0.1:8000/api/token/login/'
        data = {'username': username, 'password': password}
        response = Client().post(url, data=data)
        return response.data.get('access')

    @staticmethod
    def get_auth_header(token):
        return {'Authorization': f'JWT {token}'}


class BookingMixin:
    bookings = BOOKINGS

    @classmethod
    def create_bookings(cls):
        for idx, booking_data in cls.bookings.items():
            booking = Booking.objects.create(name=booking_data['name'])
            if 'no_of_guests' in booking_data:
                booking.no_of_guests = booking_data['no_of_guests']
            if 'booking_date' in booking_data:
                booking.booking_date = booking_data['booking_date']
            booking.save()


class SingleBookingMixin:
    booking = BOOKINGS.get(1)

    def create_booking(self):
        booking = Booking.objects.create(name=self.booking['name'])
        if 'no_of_guests' in self.booking:
            booking.no_of_guests = self.booking['no_of_guests']
        if 'booking_date' in self.booking:
            booking.booking_date = self.booking['booking_date']
        booking.save()
        self.booking = booking


class MenuItemMixin:
    items = MENU_ITEMS

    @classmethod
    def create_menu_items(cls):
        for idx, item_data in cls.items.items():
            item = Menu.objects.create(title=item_data['title'], price=item_data['price'])
            if 'inventory' in item_data:
                item.inventory = item_data['inventory']
            item.save()


class SingleMenuItemMixin:
    item = MENU_ITEMS.get(1)

    def create_menu_item(self):
        item = Menu.objects.create(title=self.item['title'], price=self.item['price'])
        if 'inventory' in self.item:
            item.inventory = self.item['inventory']
        item.save()
        self.menu_item = item
