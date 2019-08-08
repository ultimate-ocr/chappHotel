from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import date

class Room(models.Model):
    id = models.IntegerField(primary_key=True)
    price = models.FloatField(null=False, blank=False, default=50.0)
    peopleMax = models.IntegerField (null=False, blank=False, default=1)
    description = models.CharField(max_length = 200)

    @staticmethod
    def getRoom(roomId):
        return Room.objects.get(id = roomId)


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
    people      = models.IntegerField(null=False, 
                               blank=False, 
                               default=2)
    client      = models.ForeignKey(User, on_delete=models.CASCADE)
    
    telephone   = models.CharField(max_length=20)
    creditCard  = models.CharField(max_length=20)

    comments    = models.CharField(max_length=500, null=True)
    price       = models.IntegerField(default=0)

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

    def getUserBookings(user):
        return Booking.objects.filter(client = user)

    def performBook(request):
        booking = Booking()
        booking.telephone       = request.POST.get('telephone')
        booking.creditCard      = request.POST.get('creditCard')
        booking.comments        = request.POST.get('comments')
        booking.checkInDate     = datetime.datetime.strptime(request.session['checkIn'], "%d-%m-%Y").date()
        booking.checkOutDate    = datetime.datetime.strptime(request.session['checkOut'], "%d-%m-%Y").date()
        booking.people          = request.session['people']
        booking.room_id         = request.session['roomId']
        booking.client_id       = request.user.id
        booking.price           = booking.room.price*(booking.checkOutDate-booking.checkInDate).days
        
        booking.save()

        return booking


class Guest(models.Model):
    FirstName = models.CharField(max_length = 100)
    LastName  = models.CharField(max_length = 100)
    book      = models.ForeignKey(Booking,on_delete=models.CASCADE)