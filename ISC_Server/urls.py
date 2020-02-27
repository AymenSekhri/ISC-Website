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

    path('api/events', API.APIListEvents, name='lsevents-api'),
    path('api/events/create', API.APICreateEvent, name='create-event-api'),
    path('api/events/<int:id>', API.APIEventInfo, name='event-api'),
    path('api/events/<int:id>/manage', API.APIManageEvent, name='manage-event-api'),
    path('api/events/<int:id>/list', API.APIListEnrollmentsOfEvent, name='enrollment-list-api'),
    path('api/events/<int:id>/postpone', API.APIPostponeEvent, name='postpone-event-api'),
    path('api/events/<int:id>/enroll', API.APIEnrollEvent, name='enroll-event-api'),
    path('api/events/<int:id>/decision', API.APIMakeDecision, name='make-decision-api'),
    
    path('api/news/', API.APIGetNewsPostsList, name='get-posts-list-api'),
    path('api/news/create', API.APICreateNewsPost, name='create-post-api'),
    path('api/news/<int:id>', API.APIGetNewsPostDetails, name='get-post-api'),
    path('api/news/<int:id>/edit', API.APIEditNewsPost, name='edit-post-api'),

    path('api/projects', API.APIGetNewsPostsList, name='get-project-list-api'),
    path('api/projects/create', API.APICreateNewsPost, name='create-project-api'),
    path('api/projects/<int:id>', API.APIGetNewsPostDetails, name='get-project-api'),
    path('api/projects/<int:id>/edit', API.APIEditNewsPost, name='edit-project-api'),
    
    path('api/team/', API.APIGetTeamList, name='get-team-api'),
    path('api/team/add', API.APIAddToTheTeam, name='add-member-api'),
    path('api/team/<int:id>', API.APIDeleteMember, name='get-member-api'),
    path('api/team/<int:id>/edit', API.APIEditTeamMember, name='edit-member-api'),

    path('api/users', API.APIGetUsersList, name='get-users-api'),
    path('api/users/<int:id>', API.APIGetUserDetails, name='get-user-api'),
    path('api/users/<int:id>/edit', API.APIEditUserProfile, name='edit-user-api'),
    path('api/users/<int:id>/upgrade', API.APIUpgradeUser, name='upgrade-user-api'),

    path('api/contact', API.APIMakeDecision, name=''),

    ###   Pages
    path('', FrontPages.Home, name='home-page'),
    path('register', FrontPages.Register, name='register-page'),
    path('login', FrontPages.Login, name='login-page'),
    path('forgotpassword', FrontPages.ForgotPassword, name='forgot-pass-page'),
    path('resetpassword', FrontPages.ResetPassword, name='reset-pass-page'),
]