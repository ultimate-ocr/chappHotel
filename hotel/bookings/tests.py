from django.test import TestCase, Client
from django.urls import reverse

from .models import *

class BookingTestCase(TestCase):
    def setUp(self):
        for i in range(100,125):
            if i in range(100,110):
                Room.objects.create(id = i, price = 20, peopleMax = 1, description = 'Single')
                continue
            if i in range(110,115):
                Room.objects.create(id = i, price = 30, peopleMax = 2, description = 'Double')
                continue
            if i in range(115,120):
                Room.objects.create(id = i, price = 40, peopleMax = 3, description = 'Triple')
                continue
            if i in range(119,125):
                Room.objects.create(id = i, price = 50, peopleMax = 4, description = 'For 4')
                continue

    def testGetRoom(self):
        room = Room()
        for i in range (100,125):
            self.assertIsInstance(Room.getRoom(123),Room)