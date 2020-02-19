"""
Definition of urls for ISC_Server.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from .MainApp import views as MainApp_views
from .UsersApp import api_views as API
from .UsersApp import page_views as FrontPages

urlpatterns = [
    #path('', MainApp_views.Home, name='home-page'),
    path('admin', admin.site.urls, name='admin-page'),

    path('api/register', API.APIRegister, name='register-api'),
    path('api/login', API.APILogin, name='login-api'),
    path('api/logout', API.APILogout, name='logout-api'),
    path('api/loginInfo', API.APIGetLoginInfo, name='loginInfo-api'),
    path('api/forgotpassword', API.APIForgotPassword, name='forgot-pass-api'),
    path('api/resetpassword', API.APIResetPassword, name='reset-pass-api'),
    path('api/createevent', API.APICreateEvent, name='create-event-api'),
    path('api/events', API.APIListEvents, name='lsevents-api'),
    path('api/events/<int:id>', API.APIEventInfo, name='event-api'),
    path('api/events/<int:id>/manage', API.APIManageEvent, name='manage-event-api'),
    path('api/events/<int:id>/list', API.APIListEnrollmentsOfEvent, name='enrollment-list-api'),
    path('api/events/<int:id>/postpone', API.APIPostponeEvent, name='postpone-event-api'),
    path('api/events/<int:id>/enroll', API.APIEnrollEvent, name='enroll-event-api'),
    path('api/events/<int:id>/decision', API.APIMakeDecision, name='make-decision-api'),

    path('', FrontPages.Home, name='home-page'),
    path('register', FrontPages.Register, name='register-page'),
    path('login', FrontPages.Login, name='login-page'),
    
    path('forgotpassword', FrontPages.ForgotPassword, name='forgot-pass-page'),
    path('resetpassword', FrontPages.ResetPassword, name='reset-pass-page'),
]