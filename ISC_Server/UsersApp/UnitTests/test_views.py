"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
django.setup()
try:
    from django.test.utils import setup_test_environment# VS goes here
    setup_test_environment()
except :
    pass# Shell goes here

from django.test import TestCase
from django.urls import reverse
from django.test import Client


import ISC_Server.UsersApp.views

from ISC_Server.UsersApp.ErrorCodes import ErrorCodes
from ISC_Server.UsersApp.UsersManager import UsersManager
from ISC_Server.UsersApp.forms import RegisterForm,LoginForm,ForgotForm,ResetForm
from ISC_Server.UsersApp.models import UsersDB

################################################
from colorama import Fore, Back, Style,init
init()
def printf(text,color):
     print(color + text)
     print(Style.RESET_ALL)
################################################

# TODO: Configure your database in settings.py and sync before running tests.

class LoginAndRegisterTest(TestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(LoginAndRegisterTest, cls).setUpClass()
        django.setup()

    def setUp(cls):
        pass

    test_email= "test@gmail.com"
    test_name = "TestName"
    test_password = "pass_test/test_123456"
    test_userAgent = "TestUserAgent//Firefox."

    def test_LoginURLExists(cls):
        response = cls.client.get("/login")
        cls.assertEqual(response.status_code,200)

    def test_LoginURLNameExists(cls):
        response = cls.client.get(reverse("login-page"))
        cls.assertEqual(response.status_code,200)

    def test_RegisterURLExists(cls):
        response = cls.client.get("/register")
        cls.assertEqual(response.status_code,200)

    def test_RegisterURLNameExists(cls):
        response = cls.client.get(reverse("register-page"))
        cls.assertEqual(response.status_code,200)
    
    def test_RegisterAndSucessLogin(cls):
        registrationResponse = cls.addUser(cls.test_email,cls.test_password)
        cls.assertRedirects(registrationResponse,reverse("login-page"),status_code=302,target_status_code=200)
        loginResponse = cls.userLogin(cls.test_email, cls.test_password, cls.test_userAgent,cls.test_userAgent)
        cls.assertRedirects(loginResponse,reverse("home-page"),status_code=302,target_status_code=200)
        homeResponse = cls.getHome(cls.test_userAgent,loginResponse.cookies)
        cls.assertEqual(homeResponse.context['login'],1)
        cls.assertEqual(homeResponse.context['userName'],cls.test_name)

    def test_RegisterInvalidRequests(cls):
        form_data = {'firstName':cls.test_name,'familyName':"TestLastName",'email':cls.test_email,
                'pass1':cls.test_password,'pass2':cls.test_password,'number':"100",'year':"2020"}
        temp_form_data = form_data.copy()
        temp_form_data['firstName'] = "NotValidUser123"
        response = cls.client.post("/register",data=temp_form_data)
        cls.assertEqual(response.status_code,400)

        temp_form_data = form_data.copy()
        temp_form_data['familyName'] = "NotValidUser123"
        response = cls.client.post("/register",data=temp_form_data)
        cls.assertEqual(response.status_code,400)

        temp_form_data = form_data.copy()
        temp_form_data['email'] = "NotValidEmail"
        response = cls.client.post("/register",data=temp_form_data)
        cls.assertEqual(response.status_code,400)

        temp_form_data = form_data.copy()
        temp_form_data['number'] = "NotValidNumber"
        response = cls.client.post("/register",data=temp_form_data)
        cls.assertEqual(response.status_code,400)

        temp_form_data = form_data.copy()
        temp_form_data['year'] = "NotValidYear"
        response = cls.client.post("/register",data=temp_form_data)
        cls.assertEqual(response.status_code,400)

    def test_RegisterPasswordMissmatch(cls):
        form_data = {'firstName':cls.test_name,'familyName':"TestLastName",'email':cls.test_email,
                'pass1':cls.test_password,'pass2':cls.test_password,'number':"100",'year':"2020"}
        temp_form_data = form_data.copy()
        temp_form_data['pass1'] = "First----Pass123"
        temp_form_data['pass2'] = "DifferentPass123"
        response = cls.client.post("/register",data=temp_form_data)
        cls.assertEqual(response.context['error'],ErrorCodes.REGISTER_INPUTS.PASSMISSMATCH) 

    def test_RegisterUserDoesExistBofore(cls):
        cls.addUser2("TestName","myFirstEmail@gmail.com",cls.test_password)#register the user first
        response = cls.addUser2("TestName","mySecondEmail@gmail.com",cls.test_password)#register again
        cls.assertEqual(response.context['error'],ErrorCodes.REGISTER_INPUTS.USEREXISTS)

    def test_RegisterUserDoesExistBofore(cls):
        cls.addUser2("TestNameOne","SameEmail@gmail.com",cls.test_password)#register the user first
        response = cls.addUser2("TestNameTwo","SameEmail@gmail.com",cls.test_password)#register again
        cls.assertEqual(response.context['error'],ErrorCodes.REGISTER_INPUTS.EMAILEXISTS)

    def test_StayLoginWithInvalidSessionToken(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin(cls.test_email, cls.test_password, cls.test_userAgent,cls.test_userAgent)
        cls.assertRedirects(loginResponse,reverse("home-page"),status_code=302,target_status_code=200)
        wrongCookie = loginResponse.cookies
        wrongCookie["session_id"] = "THIS_WRONG_SESSION_ID"
        homeResponse = cls.getHome(cls.test_userAgent,wrongCookie)
        cls.assertEqual(homeResponse.context['login'],0)

    def test_StayLoginWithInvalidUserID(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin(cls.test_email, cls.test_password, cls.test_userAgent,cls.test_userAgent)
        cls.assertRedirects(loginResponse,reverse("home-page"),status_code=302,target_status_code=200)
        wrongCookie = loginResponse.cookies
        wrongCookie["user_id"] = "123456"
        homeResponse = cls.getHome(cls.test_userAgent,wrongCookie)
        cls.assertEqual(homeResponse.context['login'],0)

    def test_StayLoginWithInvalidUserAgent(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin(cls.test_email, cls.test_password, cls.test_userAgent,cls.test_userAgent)
        cls.assertRedirects(loginResponse,reverse("home-page"),status_code=302,target_status_code=200)
        homeResponse = cls.getHome("THIS_WRONG_USERAGENT",loginResponse.cookies)
        cls.assertEqual(homeResponse.context['login'],0)


    def test_RegisterAndFaildLoginPassword(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin(cls.test_email, "WrongPassword123", cls.test_userAgent,"")
        cls.assertEqual(loginResponse.status_code,200)
        cls.assertEqual(loginResponse.context['error'],ErrorCodes.LOGIN_INPUTS.PASS_MISMATCH)

    def test_RegisterAndFaildLoginEmail(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin("WrongEmail@live.com", cls.test_password, cls.test_userAgent,"")
        cls.assertEqual(loginResponse.status_code,200)
        cls.assertEqual(loginResponse.context["error"],ErrorCodes.LOGIN_INPUTS.EMAIL_NOT_FOUND)

    def test_RegisterAndFaildLoginPassEmail(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin("WrongEmail@live.com", "WrongPassword123", cls.test_userAgent,"")
        cls.assertEqual(loginResponse.status_code,200)
        cls.assertEqual(loginResponse.context["error"], ErrorCodes.LOGIN_INPUTS.EMAIL_NOT_FOUND)

    def getHome(cls,userAgent,cookies):
        newClient = Client(HTTP_USER_AGENT=userAgent)
        newClient.cookies = cookies
        response = newClient.get(reverse("home-page"))
        return response

    def addUser2(cls,firstName,email,password):
        form_data = {'firstName':firstName,'familyName':"TestLastName",'email':email,
                'pass1':password,'pass2':password,'number':"100",'year':"2020"}
        return cls.client.post("/register",data=form_data)

    def addUser(cls,email,password):
        form_data = {'firstName':cls.test_name,'familyName':"TestLastName",'email':email,
                'pass1':password,'pass2':password,'number':"100",'year':"2020"}
        return cls.client.post("/register",data=form_data)

    def userLogin(cls,emaill,password,userAgent,cookies):
        form_data = {"email":emaill,"password":password}
        newClient = Client(HTTP_USER_AGENT=userAgent)
        return newClient.post("/login", data=form_data)
