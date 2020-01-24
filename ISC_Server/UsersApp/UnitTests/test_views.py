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
    test_password = "pass_test/test_123456"
    test_userAgent = "TestUserAgent//Firefox."

    def test_LoginUrlExists(cls):
        response = cls.client.get("/login")
        cls.assertEqual(response.status_code,200)

    def test_LoginUrlNameExists(cls):
        response = cls.client.get(reverse("login-page"))
        cls.assertEqual(response.status_code,200)

    def test_RegisterUrlExists(cls):
        response = cls.client.get("/register")
        cls.assertEqual(response.status_code,200)

    def test_RegisterUrlNameExists(cls):
        response = cls.client.get(reverse("register-page"))
        cls.assertEqual(response.status_code,200)
    
    def test_RegisterAndSucessLogin(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin(cls.test_email, cls.test_password, cls.test_userAgent,"")
        cls.assertRedirects(loginResponse,reverse("home-page"),status_code=302,target_status_code=200)

    def test_RegisterAndFaildLoginPassword(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin(cls.test_email, "WrongPassword123", cls.test_userAgent,"")
        cls.assertEqual(loginResponse.status_code,200)
        cls.assertEqual(loginResponse.context['error'],ErrorCodes.LOGIN_INPUTS.PASS_MISMATCH)

    def test_RegisterAndFaildLoginPassword(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin("WrongEmail@live.com", cls.test_password, cls.test_userAgent,"")
        cls.assertEqual(loginResponse.status_code,200)
        cls.assertEqual(loginResponse.context["error"],ErrorCodes.LOGIN_INPUTS.EMAIL_NOT_FOUND)

    def test_RegisterAndFaildLoginPassEmail(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin("WrongEmail@live.com", "WrongPassword123", cls.test_userAgent,"")
        cls.assertEqual(loginResponse.status_code,200)
        cls.assertEqual(loginResponse.context["error"], ErrorCodes.LOGIN_INPUTS.EMAIL_NOT_FOUND)

    
    def addUser(cls,email,password):
        form_data = {'firstName':"TestFirstName",'familyName':"TestLastName",'email':email,
                'pass1':password,'pass2':password,'number':"100",'year':"2020"}
        response = cls.client.post("/register",data=form_data)

    def userLogin(cls,emaill,password,userAgent,cookies):
        form_data = {"email":emaill,"password":password}
        newClient = Client(HTTP_USER_AGENT=userAgent)
        return newClient.post("/login", data=form_data)
