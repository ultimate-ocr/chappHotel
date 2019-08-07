from django.shortcuts import render, redirect
import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import date

from .forms import SearchForm, GetContactInforForm
from .models import Booking, Room
'''
class views(view):
    def home():
        pass
'''

def inputBookingInfo(request):
    try:
        searchForm = SearchForm()
        return render(request, "bookings/searchroom.html", {'searchForm':searchForm})
    except Exception as e:
        print('Error in inputBookingInfo due to: '+str(e))

@login_required(redirect_field_name='input_booking_info')
def searchRoom(request):
    try:
        if request.method == 'POST':
            checkIn  = request.POST.get('checkInDate')
            request.session['checkIn'] = checkIn
            checkIn  = datetime.datetime.strptime(checkIn, "%d-%m-%Y").date()
            checkOut = request.POST.get('checkOutDate')
            request.session['checkOutDate'] = checkOut
            checkOut = datetime.datetime.strptime(checkOut, "%d-%m-%Y").date()
            if checkIn >= checkOut or checkIn < date.today():
                searchForm = SearchForm()
                return render(request, "bookings/searchroom.html", {'searchForm':searchForm, 'error':'Please check dates'})
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
    except Exception as e:
        print('Error in searchRoom due to: '+str(e))
        inputBookingInfo()

def checkLogIn(request):
    try:
        if request.method == 'POST':
            if 'user' in request:
                return JsonResponse({'redirectUrl':'/bookininfo'})
            else:
                return JsonResponse({'redirectUrl':'/accounts/login'})
    except Exception as e:
        print('Error in checkLogin due to: '+str(e))
        inputBookingInfo()


@login_required
def redirectStaff(request):
    try:
        if request.user.is_staff:
            print('STAFF')
            bookings = Booking.getAllBookings()
            return render(request, "bookings/staffshowbooking.html", {'bookings':bookings, 'all':'true'})
        else:
            print('CIVIL')
            searchForm = SearchForm()
            return render(request, "bookings/searchroom.html", {'searchForm':searchForm})
    except Exception as e:
        print('Error in redirectStaff due to: '+str(e))
        inputBookingInfo()


@login_required
def showAllBookings(request):
    try:
        bookings = Booking.getAllBookings()
        return render(request, "bookings/staffshowbooking.html", {'bookings':bookings,'all':'true'})
    except Exception as e:
        print('Error in showAllBookings due to: '+str(e))
        inputBookingInfo()

@login_required
def cancelbooking(request):
    try:
        if request.method == 'POST':
            bookingId = request.POST.get('bookingId')
            booking = Booking.cancelBooking(bookingId)
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'ok'})
    except Exception as e:
        print('Error in cancelBooking due to: '+str(e))
        inputBookingInfo()

@login_required
def doCheckIn(request):
    try:
        if request.method == 'POST':
            bookingId = request.POST.get('bookingId')
            booking = Booking.doCheckIn(bookingId)
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'ok'})
    except Exception as e:
        print('Error in doCheckIn due to: '+str(e))
        inputBookingInfo()

@login_required
def doCheckOut(request):
    try:
        if request.method == 'POST':
            bookingId = request.POST.get('bookingId')
            booking = Booking.doCheckOut(bookingId)
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'ok'})
    except Exception as e:
        print('Error in searchRoom due to: '+str(e))
        inputBookingInfo()

@login_required
def showTodayBookings(request):
    try:
        bookings = Booking.getTodayBookings()
        return render(request, "bookings/staffshowbooking.html", {'bookings':bookings})
    except Exception as e:
        print('Error in showTodaysBookings due to: '+str(e))
        inputBookingInfo()

@login_required
def showUserBookings(request):
    try:
        bookings = Booking.getUserBookings(request.user)
        return render(request, "bookings/showclientbookings.html", {'bookings':bookings})
    except Exception as e:
        print('Error in showUserBookings due to: '+str(e))
        inputBookingInfo()

@login_required
def getContactInfo(request):
    try:
        getContactInfoForm = GetContactInforForm()
        return render(request, "bookings/getcontactinfo.html", {'getContactInfoForm':getContactInfoForm})
    except Exception as e:
        print('Error in getContactInfo due to: '+str(e))
        inputBookingInfo()