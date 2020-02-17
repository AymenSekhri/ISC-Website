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
from django.utils import timezone
import json



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
        response = cls.client.post(reverse("login-api"))
        cls.assertEqual(response.status_code,400)


    def test_RegisterURLNameExists(cls):
        response = cls.client.post(reverse("register-api"))
        cls.assertEqual(response.status_code,400)
        
    def test_RegisterInvalidRequests(cls):
        form_data = {'firstName':cls.test_name,'familyName':"TestLastName",'email':cls.test_email,
                'pass1':cls.test_password,'pass2':cls.test_password,'number':"100",'year':"2020"}
        temp_form_data = form_data.copy()
        temp_form_data['firstName'] = "NotValidUser123"
        response = cls.client.post(reverse("register-api"),data=temp_form_data)
        cls.assertEqual(response.status_code,400)

        temp_form_data = form_data.copy()
        temp_form_data['familyName'] = "NotValidUser123"
        response = cls.client.post(reverse("register-api"),data=temp_form_data)
        cls.assertEqual(response.status_code,400)

        temp_form_data = form_data.copy()
        temp_form_data['email'] = "NotValidEmail"
        response = cls.client.post(reverse("register-api"),data=temp_form_data)
        cls.assertEqual(response.status_code,400)

        temp_form_data = form_data.copy()
        temp_form_data['number'] = "NotValidNumber"
        response = cls.client.post(reverse("register-api"),data=temp_form_data)
        cls.assertEqual(response.status_code,400)

        temp_form_data = form_data.copy()
        temp_form_data['year'] = "NotValidYear"
        response = cls.client.post(reverse("register-api"),data=temp_form_data)
        cls.assertEqual(response.status_code,400)

    def test_RegisterPasswordMissmatch(cls):
        form_data = {'firstName':cls.test_name,'familyName':"TestLastName",'email':cls.test_email,
                'pass1':cls.test_password,'pass2':cls.test_password,'number':"100",'year':"2020"}
        temp_form_data = form_data.copy()
        temp_form_data['pass1'] = "First----Pass123"
        temp_form_data['pass2'] = "DifferentPass123"
        response = cls.client.post(reverse("register-api"),data=temp_form_data)
        cls.assertEqual(response.json()['Status'],ErrorCodes.REGISTER_INPUTS.PASSMISSMATCH) 

    def test_RegisterUserDoesExistBofore(cls):
        cls.addUser2("TestName","myFirstEmail@gmail.com",cls.test_password)#register the user first
        response = cls.addUser2("TestName","mySecondEmail@gmail.com",cls.test_password)#register again
        cls.assertEqual(response.json()['Status'],ErrorCodes.REGISTER_INPUTS.USEREXISTS)

    def test_RegisterEmailDoesExistBofore(cls):
        cls.addUser2("TestNameOne","SameEmail@gmail.com",cls.test_password)#register the user first
        response = cls.addUser2("TestNameTwo","SameEmail@gmail.com",cls.test_password)#register again
        cls.assertEqual(response.json()['Status'],ErrorCodes.REGISTER_INPUTS.EMAILEXISTS)

    def test_RegisterAndSucessLogin(cls):
        registrationResponse = cls.addUser(cls.test_email,cls.test_password)
        cls.assertEqual(registrationResponse.status_code,200)
        cls.assertEqual(registrationResponse.json()['Status'],ErrorCodes.REGISTER_INPUTS.NONE)

        loginResponse = cls.userLogin(cls.test_email, cls.test_password, cls.test_userAgent,cls.test_userAgent)
        cls.assertEqual(loginResponse.status_code,200)
        cls.assertEqual(loginResponse.json()['Status'],ErrorCodes.REGISTER_INPUTS.NONE)

        homeResponse = cls.getLoginInfo(cls.test_userAgent,loginResponse.cookies)
        cls.assertEqual(homeResponse.json()['login'],1)
        cls.assertEqual(homeResponse.json()['firstName'],cls.test_name.lower())

    def test_RegisterAndFaildLoginPassword(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin(cls.test_email, "WrongPassword123", cls.test_userAgent,"")
        cls.assertEqual(loginResponse.status_code,200)
        cls.assertEqual(loginResponse.json()['Status'],ErrorCodes.LOGIN_INPUTS.PASS_MISMATCH)

    def test_RegisterAndFaildLoginEmail(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin("WrongEmail@live.com", cls.test_password, cls.test_userAgent,"")
        cls.assertEqual(loginResponse.status_code,200)
        cls.assertEqual(loginResponse.json()['Status'],ErrorCodes.LOGIN_INPUTS.EMAIL_NOT_FOUND)

    def test_RegisterAndFaildLoginPassEmail(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin("WrongEmail@live.com", "WrongPassword123", cls.test_userAgent,"")
        cls.assertEqual(loginResponse.status_code,200)
        cls.assertEqual(loginResponse.json()['Status'], ErrorCodes.LOGIN_INPUTS.EMAIL_NOT_FOUND)

    def test_LoginAndLogout(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin(cls.test_email, cls.test_password, cls.test_userAgent,cls.test_userAgent)
        newClient = Client(HTTP_USER_AGENT=cls.test_userAgent)
        newClient.cookies = loginResponse.cookies
        newClient.get(reverse("logout-api"))
        homeResponse = cls.getLoginInfo(cls.test_userAgent,loginResponse.cookies)
        cls.assertEqual(homeResponse.json()['login'],0)

    def test_StayLoginWithInvalidSessionToken(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin(cls.test_email, cls.test_password, cls.test_userAgent,cls.test_userAgent)
        cls.assertEqual(loginResponse.status_code,200)
        cls.assertEqual(loginResponse.json()['Status'],ErrorCodes.REGISTER_INPUTS.NONE)

        wrongCookie = loginResponse.cookies
        wrongCookie["session_id"] = "THIS_WRONG_SESSION_ID"
        homeResponse = cls.getLoginInfo(cls.test_userAgent,wrongCookie)
        cls.assertEqual(homeResponse.json()['login'],0)

    def test_StayLoginWithInvalidUserID(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin(cls.test_email, cls.test_password, cls.test_userAgent,cls.test_userAgent)
        cls.assertEqual(loginResponse.status_code,200)
        cls.assertEqual(loginResponse.json()['Status'],ErrorCodes.REGISTER_INPUTS.NONE)

        wrongCookie = loginResponse.cookies
        wrongCookie["user_id"] = "123456"
        homeResponse = cls.getLoginInfo(cls.test_userAgent,wrongCookie)
        cls.assertEqual(homeResponse.json()['login'],0)

    def test_StayLoginWithInvalidUserAgent(cls):
        cls.addUser(cls.test_email,cls.test_password)
        loginResponse = cls.userLogin(cls.test_email, cls.test_password, cls.test_userAgent,cls.test_userAgent)
        cls.assertEqual(loginResponse.status_code,200)
        cls.assertEqual(loginResponse.json()['Status'],ErrorCodes.REGISTER_INPUTS.NONE)
        
        homeResponse = cls.getLoginInfo("THIS_WRONG_USERAGENT",loginResponse.cookies)
        cls.assertEqual(homeResponse.json()['login'],0)

    def getLoginInfo(cls,userAgent,cookies):
        newClient = Client(HTTP_USER_AGENT=userAgent)
        newClient.cookies = cookies
        response = newClient.get(reverse("loginInfo-api"))
        return response
    
    def addUser2(cls,firstName,email,password):
        form_data = {'firstName':firstName,'familyName':"TestLastName",'email':email,
                'pass1':password,'pass2':password,'number':"100",'year':"2020"}
        return cls.client.post(reverse("register-api"),data=form_data)

    def addUser(cls,email,password):
        form_data = {'firstName':cls.test_name,'familyName':"TestLastName",'email':email,
                'pass1':password,'pass2':password,'number':"100",'year':"2020"}
        return cls.client.post(reverse("register-api"),data=form_data)

    def userLogin(cls,emaill,password,userAgent,cookies):
        form_data = {"email":emaill,"password":password}
        newClient = Client(HTTP_USER_AGENT=userAgent)
        return newClient.post(reverse("login-api"), data=form_data)


class EventsTest(TestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(EventsTest, cls).setUpClass()
        django.setup()

    def setUp(cls):
        pass

    def test_createEvent(cls):
        newEventFormData1 = {'eventName': 'Machine Learning Bootcamp',
                            'event_date': '10-04-2020 11:30',
                            'description': 'You will learn genetic algorithm in this bootcamp',
                            'deadline_date': '10-04-2020',
                            'maxNumberOfEnrolment': 50,
                            'enrollmentData': 'hello'}
        newEventFormData2 = {'eventName': 'Malware Analysis Bootcamp',
                            'event_date': '20-04-2020 11:30',
                            'description': 'You will learn how to detect malwares',
                            'deadline_date': '18-04-2020',
                            'maxNumberOfEnrolment': 50,
                            'enrollmentData': 'hello'}
        response = cls.client.post(reverse("create-event-api"),data=newEventFormData1)
        cls.assertEqual(response.status_code,200)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENT_INPUTS.NONE)
        response = cls.client.post(reverse("create-event-api"),data=newEventFormData1)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENT_INPUTS.EVENTEXISTS)

        response = cls.client.post(reverse("create-event-api"),data=newEventFormData2)
        cls.assertEqual(response.status_code,200)

        response = cls.client.post(reverse("manage-event-api"),data={'command':"ls events"})
        eventList = response.json()['Data']
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENT_INPUTS.NONE)        
        cls.assertEqual(eventList[0]['name'],newEventFormData1['eventName'])
        cls.assertEqual(eventList[1]['name'],newEventFormData2['eventName'])

        #print(json.loads())
