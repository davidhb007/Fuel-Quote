from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from django.contrib import messages
from Fuel_Quote.forms import QuoteForm

from . models import Quote

from users.models import Address, Profile

from datetime import date

app_name = 'Fuel_Quote'


def homePage(request):
    return render(request, 'Fuel_Quote/homePage.html', {'title': 'Home'})


def about(request):
    return render(request, 'Fuel_Quote/about.html', {'title': 'About'})


class QuoteListView(ListView):
    template_name = "Fuel_Quote/quotehistory.html"
    paginate_by = 10
    model = Quote

    def get_queryset(self):
        prof = Profile.objects.get(username=User.objects.get(
            username=self.request.user.username))
        return Quote.objects.filter(profileId=prof)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userprof = Profile.objects.filter(
            username=User.objects.get(username=self.request.user.username))
        profile_made = (len(userprof) != 0)
        context['profile_made'] = profile_made
        addr = Address.objects.get(id=Profile.objects.get(
            username=User.objects.get(username=self.request.user.username)).address.id)
        context['addr'] = addr
        return context


def calculate_price():
    price = 2.0
    return price


def quoteRequestView(request):

    profileInstance = get_object_or_404(
        Profile, username=User.objects.get(username=request.user.username))

    addr = Address.objects.get(id=Profile.objects.get(
        username=User.objects.get(username=request.user.username)).address.id)

    profExist = Profile.objects.filter(
        username=User.objects.get(username=request.user.username))

    profile_made = (len(profExist) != 0)

    pr = calculate_price()

    gal_err = ''
    date_err = ''
    pr_err = ''
    tot_err = ''
    gals = ''
    del_date = ''

    quotes = Quote.objects.filter(profileId=profileInstance)

    if request.method == "POST":
        gals = request.POST.get('gallons')
        del_date = request.POST.get('delivery_date')

        form_valid = True
        if gals in ['', None] or int(gals) <= 0:
            form_valid = False
            gal_err = "Please enter a positive integer."
        date_s = del_date
        if date_s == '':
            form_valid = False
            date_err = "Please enter a valid future date."
        else:
            try:
                dateT = date.fromisoformat(date_s)
                if date.today() > dateT:
                    form_valid = False
                    date_err = "Please enter a valid future date."
            except ValueError:
                form_valid = False
                date_err = "Please enter a valid future date."
        if request.POST.get('pr') == '--':
            form_valid = False
            pr_err = "Please generate price before continuing."
        if request.POST.get('tot') == '--':
            form_valid = False
            tot_err = "Please generate price before continuing."
        if form_valid:
            newQuote = Quote(profileId=profileInstance)
            newQuote.gallons = gals
            newQuote.address = addr
            newQuote.date = del_date
            newQuote.price = request.POST.get('pr')
            newQuote.total = request.POST.get('tot')
            newQuote.save()
            return redirect("quotesuccess")

    return render(request, "Fuel_Quote/quotePage.html", {"addr": addr,
                                                         "pr": pr,
                                                         "profile_made": profile_made,
                                                         "gal_err": gal_err,
                                                         "date_err": date_err,
                                                         "pr_err": pr_err,
                                                         "tot_err": tot_err,
                                                         "gals": gals,
                                                         "del_date": del_date,
                                                         "state": addr.state,
                                                         "hist": (len(quotes) > 0)})


class SuccessView(TemplateView):
    template_name = 'Fuel_Quote/quotesuccess.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userprof = Profile.objects.filter(
            username=User.objects.get(username=self.request.user.username))
        profile_made = (len(userprof) != 0)
        context['profile_made'] = profile_made
        return context
