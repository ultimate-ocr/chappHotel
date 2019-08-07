from django.shortcuts import render, redirect
import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .forms import SearchForm, UserInfoForm
from .models import Booking, Room
'''
class views(view):
    def home():
        pass
'''

def inputBookingInfo(request):
    searchForm = SearchForm()
    return render(request, "bookings/searchroom.html", {'searchForm':searchForm})

@login_required(redirect_field_name='input_booking_info')
def searchRoom(request):
    if request.method == 'POST':
        checkIn  = request.POST.get('checkInDate')
        request.session['checkIn'] = checkIn
        checkIn  = datetime.datetime.strptime(checkIn, "%d-%m-%Y").date()
        checkOut = request.POST.get('checkOutDate')
        request.session['checkOutDate'] = checkOut
        checkOut = datetime.datetime.strptime(checkOut, "%d-%m-%Y").date()

        people=request.POST.get('people')
        days = (checkOut - checkIn).days

        rooms = Room.objects.filter(peopleMax__gte = people).\
                            exclude(Q(booking__checkInDate__range = (checkIn, checkOut)) |\
                                 Q(booking__checkOutDate__range = (checkIn, checkOut)))
        if len(rooms) > 0:
            request.session['days']             = days
            return render(request, "bookings/showResults.html", {'rooms':rooms, 'days': days})
        else:
            searchForm = SearchForm()
            errorMessage = 'Not available rooms for those dates/n. of people'
            return render(request, "bookings/searchroom.html",\
                 {'searchForm':searchForm, 'errorMessage':errorMessage})

def checkLogIn(request):
    if request.method == 'POST':
        if 'user' in request:
            return JsonResponse({'redirectUrl':'/bookininfo'})
        else:
            return JsonResponse({'redirectUrl':'/accounts/login'})

def bookininfo(request):
    print('aaaa')


@login_required
def redirectStaff(request):
    if request.user.is_staff:
        print('STAFF')
        bookings = Booking.getAllBookings()
        return render(request, "bookings/staffshowbooking.html", {'bookings':bookings, 'all':'true'})
    else:
        print('CIVIL')
        searchForm = SearchForm()
        return render(request, "bookings/searchroom.html", {'searchForm':searchForm})


@login_required
def showAllBookings(request):
    bookings = Booking.getAllBookings()
    return render(request, "bookings/staffshowbooking.html", {'bookings':bookings,'all':'true'})

@login_required
def cancelbooking(request):
    if request.method == 'POST':
        bookingId = request.POST.get('bookingId')
        booking = Booking.cancelBooking(bookingId)
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'ok'})

@login_required
def doCheckIn(request):
    if request.method == 'POST':
        bookingId = request.POST.get('bookingId')
        booking = Booking.doCheckIn(bookingId)
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'ok'})

@login_required
def doCheckOut(request):
    if request.method == 'POST':
        bookingId = request.POST.get('bookingId')
        booking = Booking.doCheckOut(bookingId)
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'ok'})

@login_required
def showTodayBookings(request):
    bookings = Booking.getTodayBookings()
    return render(request, "bookings/staffshowbooking.html", {'bookings':bookings})