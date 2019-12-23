"""
Definition of urls for ISC_Server.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from .MainApp import views as MainApp_views
from .UsersApp import views as UsersApp_views

urlpatterns = [
    path('', MainApp_views.Home, name='home-page'),
    path('admin', admin.site.urls, name='admin-page'),
    path('register', UsersApp_views.Register, name='register-page'),
    path('login', UsersApp_views.Login, name='login-page'),
    path('logout', UsersApp_views.Logout, name='logout-page')
]