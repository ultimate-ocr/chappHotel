from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import date

class Room(models.Model):
    id = models.IntegerField(primary_key=True)
    price = models.FloatField(null=False, blank=False, default=50.0)
    peopleMax = models.IntegerField (null=False, blank=False, default=1)
    description = models.CharField(max_length = 200)


class Booking(models.Model):
    CONFIRMADA = 'conf'
    CHECKIN = 'cIn'
    CHECKOUT = 'cOut'
    CANCELED = 'canc'
    STATUS = [
        (CONFIRMADA, 'confirmada'),
        (CHECKIN, 'checkin'),
        (CHECKOUT, 'checkout'),
        (CANCELED, 'canceled'),
    ]

    days = models.IntegerField(null=False, 
                               blank=False, 
                               default=1)
    checkInDate  = models.DateField(auto_now=False)
    checkOutDate = models.DateField(auto_now=False)
    creationDate = models.DateField(auto_now=True)
    status = models.CharField(max_length=4,
                              choices=STATUS,
                              default=CONFIRMADA)
    room = models.ForeignKey(
        'Room',
        on_delete=models.CASCADE,
    )
    people = models.IntegerField(null=False, 
                               blank=False, 
                               default=2)
    models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def getAvailableRooms():
        pass
    @staticmethod
    def getAllBookings():
        return Booking.objects.all()

    @staticmethod
    def cancelBooking(bookingId):
        booking = Booking.objects.get(id = bookingId)
        booking.status = Booking.CANCELED
        booking.save()


    @staticmethod
    def doCheckIn(bookingId):
        booking = Booking.objects.get(id = bookingId)
        booking.status = Booking.CHECKIN
        booking.save()


    @staticmethod
    def doCheckOut(bookingId):
        booking = Booking.objects.get(id = bookingId)
        booking.status = Booking.CHECKOUT
        booking.save()

    @staticmethod
    def getTodayBookings():
        bookings = Booking.objects.filter(Q(checkInDate = (date.today())) |\
                                 Q(checkOutDate = (date.today())))
        return bookings

        