from django import forms
from datetime import datetime, timedelta
from django.contrib.admin import widgets
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

from .models import Booking
from django.contrib.auth.models import User

class SearchForm(forms.ModelForm):
    required_css_class = 'required'
    
    class Meta:
        model = Booking
        fields = ('checkInDate', 'checkOutDate','people',)
        widgets = {
            'checkInDate': forms.DateInput(attrs={'class':'datepicker'}),
            'checkOutDate': forms.DateInput(attrs={'class':'datepicker'}),
        }
        labels = {
            'checkInDate': ('Submit check in date'),
            'checkOutDate': ('Submit check out date'),
            'people': ('Number of people'),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        '''
        self.fields['checkInDate'].initial = 'Check In da'
        self.fields['checkInDate'].initial = 'Check Out date'
        
        self.checkInDate    = datetime.today()
        self.checkOutDate   = datetime.now() + timedelta(days=30)
        '''

class UserInfoForm(forms.ModelForm):
    required_css_class = 'required'
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        '''
        self.fields['checkInDate'].initial = 'Check In da'
        self.fields['checkInDate'].initial = 'Check Out date'
        
        self.checkInDate    = datetime.today()
        self.checkOutDate   = datetime.now() + timedelta(days=30)
        '''

class GetContactInforForm(forms.ModelForm):
    required_css_class = 'required'
    
    class Meta:
        model = Booking
        fields = ('telephone','creditCard','comments')


