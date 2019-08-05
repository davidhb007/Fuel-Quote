from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from .models import *
from .forms import *
from Fuel_Quote.models import *
from Fuel_Quote.forms import *


def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your Account has been created successfully')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userInstance = self.request.user.username

        profiles = Profile.objects.filter(
            username=User.objects.get(username=userInstance))

        profile_made = True
        if len(profiles) == 0:
            profile_made = False
        context['profile_made'] = profile_made
        if profile_made:
            profileInstance = Profile.objects.get(
                username=User.objects.get(username=userInstance))
            context['first_name'] = profileInstance.first_name
            context['last_name'] = profileInstance.last_name
            context['email'] = profileInstance.email
            addr = Address.objects.get(id=profileInstance.address.id)
            context['address1'] = addr.address1
            context['address2'] = addr.address2
            context['city'] = addr.city
            context['state'] = addr.state
            context['zipcode'] = addr.zipcode

            quote_hist = Quote.objects.filter(
                profileId=profileInstance.id)

            quote_set = Quote.objects.filter(
                profileId=profileInstance.id).order_by('-id')[:5]

            has_hist = (len(quote_hist) > 0)

            context['has_quote_history'] = has_hist

            context['quote_set'] = quote_set

        return context


def profile_edit_model(request):

    context = {}

    if len(Profile.objects.filter(username=User.objects.get(username=request.user.username))) != 0:
        profileInstance = Profile.objects.get(
            username=User.objects.get(username=request.user.username))
        if request.method == "POST":
            profile_form = editProfileForm(
                request.POST, instance=profileInstance)
            address_form = updateAddressForm(
                request.POST, instance=profileInstance)
            if profile_form.is_valid() and address_form.is_valid():
                profileInstance.first_name = profile_form.cleaned_data.get(
                    'first_name')
                profileInstance.last_name = profile_form.cleaned_data.get(
                    'last_name')
                profileInstance.email = profile_form.cleaned_data.get(
                    'email')
                addr = Address.objects.get(id=profileInstance.address.id)
                addr.address1 = address_form.cleaned_data.get('address1')
                addr.address2 = address_form.cleaned_data.get('address2')
                addr.city = address_form.cleaned_data.get('city')
                addr.state = address_form.cleaned_data.get('state')
                addr.zipcode = address_form.cleaned_data.get('zipcode')
                addr.save()
                profileInstance.address = addr
                profileInstance.save()
                messages.success(
                    request, f'Your Client Profile has been updated successfully')
                context = {
                    'profile_form': profile_form,
                    'address_form': address_form,
                }
                return redirect("profile")
        else:
            profile_form = editProfileForm(instance=profileInstance)
            address_form = updateAddressForm(instance=profileInstance.address)
            context = {
                'profile_form': profile_form,
                'address_form': address_form,
            }

    else:
        if request.method == "POST":
            profile_form = editProfileForm(request.POST)
            address_form = updateAddressForm(request.POST)
            if profile_form.is_valid() and address_form.is_valid():
                addr = address_form.save()
                newProf = profile_form.save(commit=False)
                newProf.username = User.objects.get(
                    username=request.user.username)
                newProf.address = addr
                newProf.save()
                messages.success(
                    request, f'Your Client Profile has been created successfully')
                context = {
                    'profile_form': profile_form,
                    'address_form': address_form,
                }
                return redirect("profile")
        else:
            profile_form = editProfileForm()
            address_form = updateAddressForm()
            context = {
                'profile_form': profile_form,
                'address_form': address_form,
            }

    return render(request, "users/editprofile.html", context)
