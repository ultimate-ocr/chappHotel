from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from django.contrib.auth import views as allauthViews

from . import views
import allauth

urlpatterns = [
    path('', allauth.account.views.LoginView.as_view()),
    path('logedin', views.redirectStaff, name='input_booking_info'),
    path('inputinfo', views.inputBookingInfo, name='input_booking_info'),
    path('search', views.searchRoom, name='search_room'),
    path('checkLogIn', views.checkLogIn, name='checkLogIn'),
    url(r'^accounts/', include('allauth.urls')),
    path('bookininfo', views.bookininfo, name='booking_info'),
    path('cancelbooking', views.cancelbooking, name='cancel_booking'),
    path('docheckin', views.doCheckIn, name='do_checkin'),
    path('docheckout', views.doCheckOut, name='do_checkout'),
    path('showtodaybookings', views.showTodayBookings, name='do_checkout'),
    
]