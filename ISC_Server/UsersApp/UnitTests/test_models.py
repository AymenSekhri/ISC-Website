"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.

Django Unit Testing :
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
"""

import django
django.setup()
from django.test import TestCase
from ISC_Server.UsersApp.models import UsersDB
# TODO: Configure your database in settings.py and sync before running tests.

class UsersDBTest(TestCase):
    
    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(UsersDBTest, cls).setUpClass()
        django.setup()
        

    def setUp(cls):
        UsersDB.objects.create(firstName = "TestFirstName",familyName = "TestFamilyName",email= "MyEmail@gmail.com",password = "123456",
                         privLevel = 0, number = "100",year = "2020")

    
    def test_OneUserPerName(self):
        newUserQuery = UsersDB.objects.filter(firstName = "TestFirstName",familyName = "TestFamilyName")
        self.assertEqual(newUserQuery.count(), 1)

    def test_UserFields(self):
        newUser = UsersDB.objects.filter(firstName = "TestFirstName",familyName = "TestFamilyName").first()
        self.assertEqual(newUser.email, "MyEmail@gmail.com")
        self.assertEqual(newUser.password, "123456")
        self.assertEqual(newUser.privLevel, 0)
        self.assertEqual(newUser.number, "100")
        self.assertEqual(newUser.year, "2020")
