from django.forms import ModelForm, Select, DateInput, TextInput
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from localflavor.us.forms import USStateField


from .models import *


class editProfileForm(ModelForm):
    First_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    Email = models.EmailField()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'firstname': 'Your first name',
            'lastname': 'Your lastname',
            'email': 'Your email address',
        }


class updateAddressForm(ModelForm):

    class Meta:
        model = Address
        fields = ['address1', 'address2', 'city', 'state', 'zipcode']
        labels = {
            'address1': 'Address line 1',
            'address2': 'Address line 2',
            'city': 'City',
            'state': 'State',
            'zipcode': 'ZIP Code',
        }

    def clean_zipcode(self):
        data = self.cleaned_data['zipcode']
        if len(str(data)) not in [5, 9]:
            self.add_error(None, ValidationError(
                "ZIP must either be 5 digits or 9"))
            print("Error" + str(len(str(data))))
        return data
