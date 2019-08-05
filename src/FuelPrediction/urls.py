"""FuelPrediction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Fuel_Quote import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from users import views as user_views

from Fuel_Quote.views import (
    homePage,
    about,
    quoteRequestView,
    SuccessView,
    QuoteListView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', homePage, name='Home'),
    path('home/', homePage, name='Home'),
    path('about/', about, name='About'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', user_views.profile_edit_model, name='edit'),
    path('quotes/request/', quoteRequestView, name='quoteRequest'),
    path('quotes/success/', SuccessView.as_view(), name='quotesuccess'),
    path('quotes/history/', QuoteListView.as_view(), name='quotehistory')
]
