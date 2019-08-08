from django.shortcuts import render, redirect
import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import date

from .forms import SearchForm, GetContactInforForm
from .models import Booking, Room, Guest


def inputBookingInfo(request, error=''):
    try:
        searchForm = SearchForm()
        return render(request, "bookings/searchroom.html", {'searchForm':searchForm, 'error': error})
    except Exception as e:
        print('Error in inputBookingInfo due to: '+str(e))
        return render(request, "bookings/searchroom.html", {'searchForm':searchForm})

@login_required(redirect_field_name='input_booking_info')
def searchRoom(request):
    try:
        if request.method == 'POST':
            #extracting info from form
            checkIn  = request.POST.get('checkInDate')
            request.session['checkIn'] = checkIn
            checkIn  = datetime.datetime.strptime(checkIn, "%d-%m-%Y").date()
            checkOut = request.POST.get('checkOutDate')
            request.session['checkOut'] = checkOut
            checkOut = datetime.datetime.strptime(checkOut, "%d-%m-%Y").date()
            people=request.POST.get('people')
            request.session['people'] = people

            if checkIn >= checkOut or checkIn < date.today():
                searchForm = SearchForm()
                return render(request, "bookings/searchroom.html", {'searchForm':searchForm, 'error':'Please check dates'})
            
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
        return inputBookingInfo(request, 'Error while searching for available rooms')
    


@login_required(redirect_field_name='input_booking_info')
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


@login_required(redirect_field_name='input_booking_info')
def showAllBookings(request):
    try:
        bookings = Booking.getAllBookings()
        return render(request, "bookings/staffshowbooking.html", {'bookings':bookings,'all':'true'})
    except Exception as e:
        print('Error in showAllBookings due to: '+str(e))


@login_required(redirect_field_name='input_booking_info')
def cancelbooking(request):
    try:
        if request.method == 'POST':
            bookingId = request.POST.get('bookingId')
            booking = Booking.cancelBooking(bookingId)
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'ko'})
    except Exception as e:
        print('Error in cancelBooking due to: '+str(e))
        return inputBookingInfo(request, 'Error while canceling booking')




@login_required(redirect_field_name='input_booking_info')
def doCheckIn(request):
    try:
        if request.method == 'POST':
            Guest.storeGuestsNames(request)

            bookingId = request.POST.get('bookingId')
            booking = Booking.doCheckIn(bookingId)
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'ok'})
    except Exception as e:
        print('Error in doCheckIn due to: '+str(e))
        return inputBookingInfo(request, 'Error while doing checkIn')






@login_required(redirect_field_name='input_booking_info')
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
        return inputBookingInfo(request, 'Error while doing checkout')

@login_required(redirect_field_name='input_booking_info')
def showTodayBookings(request):
    try:
        bookings = Booking.getTodayBookings()
        return render(request, "bookings/staffshowbooking.html", {'bookings':bookings})
    except Exception as e:
        print('Error in showTodaysBookings due to: '+str(e))
        inputBookingInfo()

@login_required(redirect_field_name='input_booking_info')
def showUserBookings(request):
    try:
        bookings = Booking.getUserBookings(request.user)
        return render(request, "bookings/showclientbookings.html", {'bookings':bookings})
    except Exception as e:
        print('Error in showUserBookings due to: '+str(e))
        return inputBookingInfo(request, 'Error showing user bookings')

@login_required(redirect_field_name='input_booking_info')
def getContactInfo(request):
    try:
        if request.method == 'POST':
            request.session['roomId']     = request.POST.get('roomId', None)
            return JsonResponse({'redirectUrl':'/getcontactinfo'})
        else:
            room     = Room.getRoom(request.session['roomId'])
            
            context = {}
            context['checkIn']  = request.session['checkIn']
            context['checkOut'] = request.session['checkOut']
            checkInDate  = datetime.datetime.strptime(context['checkIn'], "%d-%m-%Y").date()
            checkOutDate  = datetime.datetime.strptime(context['checkOut'], "%d-%m-%Y").date()
            
            context['people'] = request.session['people']
            context['roomDescription']    = room.description
            context['getContactInfoForm'] = GetContactInforForm()
            context['price']              = room.price*(checkOutDate-checkInDate).days
            return render(request, "bookings/getcontactinfo.html", context)
    except Exception as e:
        print('Error in getContactInfo due to: '+str(e))
        del request.session['checkIn']
        del request.session['checkOut']
        del request.session['people']
        return inputBookingInfo(request, 'Error while getting contact information')
        


@login_required(redirect_field_name='input_booking_info')
def book(request):
    try:
        context = {}
        booking = Booking.performBook(request)

        context['id']           = booking.id
        context['telephone']    = request.POST.get('telephone')
        context['creditCard']   = request.POST.get('creditCard')
        context['comments']     = request.POST.get('comments')
        context['checkIn']      = request.session['checkIn']
        context['checkOut']     = request.session['checkOut']
        context['people']       = request.session['people']
        context['room']         = booking.room
        context['price']        = booking.price
        return render(request, "bookings/successbook.html", context)

    except Exception as e:
        print(str(e))
        del request.session['checkIn']
        del request.session['checkOut']
        del request.session['people']
        return inputBookingInfo(request,'Error While finalising booking')