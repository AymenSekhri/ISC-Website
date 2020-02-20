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
import re



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
    

    def test_createEvent(cls):
        #create user
        loginCookie, userAgent, userID = cls.RegisterAndLogin()

        response = cls.postRequest(reverse("create-event-api"),
                    cls.newEventFormData1,
                    userAgent,loginCookie)
        cls.assertEqual(response.status_code,200)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENT_INPUTS.NONE)
        eventID1 = response.json()['Data']['eventID']
        response = cls.postRequest(reverse("create-event-api"),
                    cls.newEventFormData1,
                    userAgent,loginCookie)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENT_INPUTS.EVENTEXISTS)

        response = cls.postRequest(reverse("create-event-api"),
                    cls.newEventFormData2,
                    userAgent,loginCookie)
        cls.assertEqual(response.status_code,200)
        eventID2 = response.json()['Data']['eventID']

        response = cls.client.get(reverse("lsevents-api"))
        eventList = response.json()['Data']
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENT_INPUTS.NONE)

        event1info = cls.client.get(reverse("event-api",kwargs={'id':eventID1}))
        event2info = cls.client.get(reverse("event-api",kwargs={'id':eventID2}))
        cls.assertEqual(event1info.json()['Data']['name'],cls.newEventFormData1['eventName'])
        cls.assertEqual(event2info.json()['Data']['name'],cls.newEventFormData2['eventName'])

    def test_enrollEvent(cls):
        #create user
        loginCookie, userAgent, userID = cls.RegisterAndLogin()
        #create event
        response = cls.postRequest(reverse("create-event-api"),
                    cls.newEventFormData1,
                    userAgent,loginCookie)
        cls.assertEqual(response.status_code,200)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENT_INPUTS.NONE, "should create event OK")
        eventID = response.json()['Data']['eventID']
        
        #get enrollment list
        response = cls.getRequest(reverse("enrollment-list-api",kwargs={'id':eventID}),
                    userAgent,loginCookie)
        cls.assertEqual(response.json()['Status'], ErrorCodes.EVENTMANAGMENT_INPUTS.NONE, "failed to fetch data to enrollment-list-api")
        EnrollmentCount = len(response.json()['Data'])

        #enroll event
        response = cls.postRequest(reverse("enroll-event-api",kwargs={'id':eventID}),
                    {'response':'This is my response for your form'},
                    userAgent,loginCookie)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENTENROLMENT_INPUTS.NONE , "should enroll OK")
        response = cls.postRequest(reverse("enroll-event-api",kwargs={'id':eventID}),
                    {'response':'This is my response for your form'},
                    userAgent,loginCookie)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENTENROLMENT_INPUTS.DUPLICATES, "should return deplicated enrollment")
        #get enrollment list
        response = cls.getRequest(reverse("enrollment-list-api",kwargs={'id':eventID}),
                    userAgent,loginCookie)
        cls.assertEqual(response.json()['Status'], ErrorCodes.EVENTMANAGMENT_INPUTS.NONE, "failed to post data to enrollment-list-api")
        listOfEnrollments = response.json()['Data']
        cls.assertEqual(len(listOfEnrollments), EnrollmentCount + 1, "No enrollment has been added")

        userEnrollment = list(filter(lambda person: person['id'] == userID, listOfEnrollments))
        cls.assertEqual(len(userEnrollment), 1 , "The added enrollment has not been registered")


    def test_makeDecisionEvent(cls):
        #create user
        loginCookie, userAgent, userID = cls.RegisterAndLogin()
        #create event
        response = cls.postRequest(reverse("create-event-api"),
                    cls.newEventFormData1,
                    userAgent,loginCookie)
        cls.assertEqual(response.status_code,200)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENT_INPUTS.NONE, "should create event OK")
        eventID = response.json()['Data']['eventID']

        #enroll event
        response = cls.postRequest(reverse("enroll-event-api",kwargs={'id':eventID}),
                    {'response':'This is my response for your form'},
                    userAgent,loginCookie)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENTENROLMENT_INPUTS.NONE , "should enroll OK")

        #make decision
        response = cls.postRequest(reverse("make-decision-api",kwargs={'id':eventID}),
                    {'userID':userID,'decision':EnrolementDecision.ACCEPTED},
                    userAgent,loginCookie)
        cls.assertEqual(response.status_code,200)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENTENROLMENT_INPUTS.NONE , "should enroll OK")

        #get enrollment list
        response = cls.getRequest(reverse("enrollment-list-api",kwargs={'id':eventID}),
                    userAgent,loginCookie)
        cls.assertEqual(response.json()['Status'], ErrorCodes.EVENTMANAGMENT_INPUTS.NONE, "failed to post data to enrollment-list-api")
        listOfEnrollments = response.json()['Data']
        userEnrollment = list(filter(lambda person: person['id'] == userID, listOfEnrollments))
        cls.assertEqual(userEnrollment[0]['decision'], EnrolementDecision.ACCEPTED, "make sure he is accpeted")

        #make another decision
        response = cls.postRequest(reverse("make-decision-api",kwargs={'id':eventID}),
                    {'userID':userID,'decision':EnrolementDecision.REJECTED},
                    userAgent,loginCookie)
        cls.assertEqual(response.status_code,200)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENTENROLMENT_INPUTS.NONE , "should enroll OK")

        #get enrollment list
        response = cls.getRequest(reverse("enrollment-list-api",kwargs={'id':eventID}),
                    userAgent,loginCookie)
        cls.assertEqual(response.json()['Status'], ErrorCodes.EVENTMANAGMENT_INPUTS.NONE, "failed to post data to enrollment-list-api")
        listOfEnrollments = response.json()['Data']
        userEnrollment = list(filter(lambda person: person['id'] == userID, listOfEnrollments))
        cls.assertEqual(userEnrollment[0]['decision'], EnrolementDecision.REJECTED, "make sure he is accpeted")




    def test_PostponeEvent(cls):
        #create user
        loginCookie, userAgent, userID = cls.RegisterAndLogin()
        
        #create event
        response = cls.postRequest(reverse("create-event-api"),
                    cls.newEventFormData1,
                    userAgent,loginCookie)
        cls.assertEqual(response.status_code,200)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENT_INPUTS.NONE, "should create event OK")
        eventID = response.json()['Data']['eventID']

        #postpone event
        newEventDate = '10-04-2020 11:30'
        newDeadline = '10-04-2020'
        eventDateObject = timezone.datetime.strptime(newEventDate, "%d-%m-%Y %H:%M")
        deadlineDateObject = timezone.datetime.strptime(newDeadline + " 23:59", "%d-%m-%Y %H:%M")
        response = cls.postRequest(reverse("postpone-event-api",kwargs={'id':eventID}),
                    {'cmd':'pse','newDate':newEventDate},
                    userAgent,loginCookie)
        cls.assertEqual(response.status_code,200)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENTENROLMENT_INPUTS.NONE , "should postpone OK")

        #shift deadline event
        
        response = cls.postRequest(reverse("postpone-event-api",kwargs={'id':eventID}),
                    {'cmd':'pdl','newDate':newDeadline},
                    userAgent,loginCookie)
        cls.assertEqual(response.status_code,200)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENTENROLMENT_INPUTS.NONE , "should shift deadline OK")

        #get events list
        response = cls.client.get(reverse("lsevents-api"))
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENT_INPUTS.NONE)
        eventList = response.json()['Data']
        myevent = list(filter(lambda person: person['id'] == eventID, eventList))
        
        #2020-04-10 11:30:00+00:00
        newEventDate = myevent[0]['event_date'].split('+')[0]
        newDeadlineDate = myevent[0]['deadline_date'].split('+')[0]
        cls.assertEqual(newEventDate, str(eventDateObject), "make sure event date is changed")
        cls.assertEqual(newDeadlineDate, str(deadlineDateObject), "make sure deadline is changed")

    def test_ManageEvent(cls):
        #create user
        loginCookie, userAgent, userID = cls.RegisterAndLogin()
        
        #create event
        response = cls.postRequest(reverse("create-event-api"),
                    cls.newEventFormData1,
                    userAgent,loginCookie)
        cls.assertEqual(response.status_code,200)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENT_INPUTS.NONE, "should create event OK")
        eventID = response.json()['Data']['eventID']

        #get events list
        response = cls.client.get(reverse("lsevents-api"))
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENT_INPUTS.NONE)
        eventList = response.json()['Data']
        myevent = list(filter(lambda person: person['id'] == eventID, eventList))
        cls.assertEqual(myevent[0]['eventStatus'], EventStatus.ONGOING, "make sure event date is changed")

        #cancel event
        response = cls.postRequest(reverse("manage-event-api",kwargs={'id':eventID}),
                    {'cmd':'cnl'},
                    userAgent,loginCookie)
        cls.assertEqual(response.status_code,200)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENTENROLMENT_INPUTS.NONE , "should cancel the event")

        #get events list
        response = cls.client.get(reverse("lsevents-api"))
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENT_INPUTS.NONE)
        eventList = response.json()['Data']
        myevent = list(filter(lambda person: person['id'] == eventID, eventList))
        cls.assertEqual(myevent[0]['eventStatus'], EventStatus.CANCELED, "event should be canceled now")

        #remove event
        response = cls.postRequest(reverse("manage-event-api",kwargs={'id':eventID}),
                    {'cmd':'rm'},
                    userAgent,loginCookie)
        cls.assertEqual(response.status_code,200)
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENTENROLMENT_INPUTS.NONE , "should remove the event")

        #get events list
        response = cls.client.get(reverse("lsevents-api"))
        cls.assertEqual(response.json()['Status'],ErrorCodes.EVENT_INPUTS.NONE)
        eventList = response.json()['Data']
        myevent = list(filter(lambda person: person['id'] == eventID, eventList))
        cls.assertEqual(len(myevent), 0, "no more event anymore")
        

    def RegisterAndLogin(cls):
        test_email= "test@gmail.com"
        test_password = "pass_test/test_123456"
        test_userAgent = "TestUserAgent//Firefox."
        registrationResponse = cls.addUser(test_email,test_password)
        cls.assertEqual(registrationResponse.status_code,200)
        cls.assertEqual(registrationResponse.json()['Status'],ErrorCodes.REGISTER_INPUTS.NONE)

        form_data = {"email":test_email,"password":test_password}
        newClient = Client(HTTP_USER_AGENT=test_userAgent)
        loginResponse = newClient.post(reverse("login-api"), data=form_data)
        cls.assertEqual(loginResponse.status_code,200)
        cls.assertEqual(loginResponse.json()['Status'],ErrorCodes.LOGIN_INPUTS.NONE)

        response = cls.getRequest(reverse("loginInfo-api"), test_userAgent, loginResponse.cookies)
        cls.assertEqual(response.status_code,200)
        return loginResponse.cookies , test_userAgent, response.json()['id']

    
    def addUser(cls,email,passrd):
        form_data = {'firstName':"thisismyfirstName",'familyName':"ThisMyFamName",'email':email,
                'pass1':passrd,'pass2':passrd,'number':"100",'year':"2020"}
        return cls.client.post(reverse("register-api"),data=form_data)

    def postRequest(cls,url,data,userAgent,cookie):
        newClient = Client(HTTP_USER_AGENT=userAgent)
        newClient.cookies = cookie
        response = newClient.post(url,data=data)
        return response

    def getRequest(cls,url,userAgent,cookie):
        newClient = Client(HTTP_USER_AGENT=userAgent)
        newClient.cookies = cookie
        response = newClient.get(url)
        return response

class EnrolementDecision(object):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2

class EventStatus(object):
    ONGOING = 0
    POSTPONED = 1
    CANCELED = 2