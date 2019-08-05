from django.forms import ModelForm, Select, DateInput, TextInput
from users.models import Address, Profile
from django.db import models
from .models import Quote
from django.core.exceptions import ValidationError


class QuoteForm(ModelForm):
    gallons = models.PositiveIntegerField()
    date = models.DateField()
    price = models.DecimalField(decimal_places=2, max_digits=5)
    total = models.DecimalField(decimal_places=2, max_digits=20)

    class Meta:
        model = Quote
        fields = ['gallons', 'date']
        labels = {
            'gallons': 'Gallons requested',
            'date': 'Date of delivery',
        }
        widgets = {
            'date': DateInput(attrs={'class': 'datepicker'}),
        }

    gal_err = ''
    date_err = ''
    pr_err = ''
    tot_err = ''
    gals = None
    del_date = None
