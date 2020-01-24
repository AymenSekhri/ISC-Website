"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace cls with more appropriate tests for your application.

Django Unit Testing :
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
"""

import django
django.setup()
from django.test import TestCase
from django.utils import timezone
from ISC_Server.UsersApp.models import UsersDB
from ISC_Server.UsersApp.models import SessionsDB
from datetime import datetime, timedelta  

# TODO: Configure your database in settings.py and sync before running tests.

class UsersDBTest(TestCase):
    #Test User  
    test_firstName= "TestFirstName"
    test_familyName = "TestFamilyName"
    test_email = "MyEmail@gmail.com"
    test_password = "pass_123456"
    test_privLevel = 0
    test_number = "100"
    test_year = "2020"

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(UsersDBTest, cls).setUpClass()
        django.setup()
        

    def setUp(cls):
        UsersDB.objects.create(firstName = cls.test_firstName,familyName = cls.test_familyName,email= cls.test_email,password = cls.test_password,
                         privLevel = cls.test_privLevel, number = cls.test_number,year = cls.test_year)

    
    def test_OneUserPerName(cls):
        newUserQuery = UsersDB.objects.filter(firstName = cls.test_firstName,familyName = cls.test_familyName)
        cls.assertEqual(newUserQuery.count(), 1)

    def test_UserFieldsAreOkay(cls):
        newUser = UsersDB.objects.filter(firstName = cls.test_firstName,familyName = cls.test_familyName).first()
        cls.assertEqual(newUser.email, cls.test_email)
        cls.assertEqual(newUser.password, cls.test_password)
        cls.assertEqual(newUser.privLevel, cls.test_privLevel)
        cls.assertEqual(newUser.number, cls.test_number)
        cls.assertEqual(newUser.year, cls.test_year)
        cls.assertEqual(newUser.regDate, timezone.now().date())

class SessionsDBTest(TestCase):
    
    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(SessionsDBTest, cls).setUpClass()
        django.setup()

    #Test User  
    test_firstName= "TestFirstName"
    test_familyName = "TestFamilyName"
    test_email = "MyEmail@gmail.com"
    test_password = "pass_123456"
    test_privLevel = 0
    test_number = "100"
    test_year = "2020"

    #Test Session
    test_token = "this_session_token_123456"
    test_token = "this_session_key_123456"
    test_expiration = timezone.now() + timedelta(minutes=5)

    def setUp(cls):
        NewUser = UsersDB.objects.create(firstName = cls.test_firstName,familyName = cls.test_familyName,email= cls.test_email,password = cls.test_password,
                         privLevel = cls.test_privLevel, number = cls.test_number,year = cls.test_year)
        SessionsDB.objects.create(uid_id = NewUser.id,token = cls.test_token,key = cls.test_token,
                                  expiration_date = cls.test_expiration)

    
    def test_OneSessionPerUser(cls):
        newUserQuery = SessionsDB.objects.filter(token = cls.test_token)
        cls.assertEqual(newUserQuery.count(), 1)

    def test_SessionFields(cls):
        Session = SessionsDB.objects.filter(token = cls.test_token).first()
        cls.assertEqual(Session.key, cls.test_token)
    
    def test_session_expired(cls):
        cls.assertEqual(1, 1) ## TODO: Unit test time dependent functions
        

        
