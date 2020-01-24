"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
django.setup()
from django.test import TestCase

from ISC_Server.UsersApp.forms import RegisterForm,LoginForm,ForgotForm,ResetForm
# TODO: Configure your database in settings.py and sync before running tests.

class RegisterFormTest(TestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(RegisterFormTest, cls).setUpClass()
        django.setup()

    def setUp(cls):
        pass

    form_data = {'firstName':"TestFirstName",'familyName':"TestLastName",'email':"MyEmail@gmail.com",
                'pass1':"pass_123456",'pass2':"pass_123456",'number':"100",'year':"2020"}

    def checkUserName(cls,fistName,lastName):
        temp_data = cls.form_data.copy()
        temp_data['firstName'] = fistName
        temp_data['familyName'] = lastName
        form = RegisterForm(data=temp_data)
        return form.is_valid()

    def test_NonCharachterNames(cls):
        cls.assertTrue(cls.checkUserName("TestFirstName","TestLastName"))
        cls.assertFalse(cls.checkUserName("TestFirst1Name","TestLastName"))
        cls.assertFalse(cls.checkUserName("TestFirstName","TestLast1Name"))
        cls.assertFalse(cls.checkUserName("TestFirst@Name","TestLast@Name"))
        cls.assertFalse(cls.checkUserName("TestFirst.Name","TestLast.Name"))

    def test_validEmail(cls):
        temp_data = cls.form_data.copy()

        temp_data['email'] = "blabla@gmail.com"
        cls.assertTrue(RegisterForm(data=temp_data).is_valid())
        
        temp_data['email'] = "blablagmail.com"
        cls.assertFalse(RegisterForm(data=temp_data).is_valid())

        temp_data['email'] = "blabla@gmailcom"
        cls.assertFalse(RegisterForm(data=temp_data).is_valid())

        temp_data['email'] = "@."
        cls.assertFalse(RegisterForm(data=temp_data).is_valid())

class LoginFormTest(TestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(LoginFormTest, cls).setUpClass()
        django.setup()

    def setUp(cls):
        pass

    form_data = {'email':"blabla@gmail.com",'password':"password123456"}

    def test_validEmail(cls):
        temp_data = cls.form_data.copy()

        temp_data['email'] = "blabla@gmail.com"
        cls.assertTrue(LoginForm(data=temp_data).is_valid())

        temp_data['email'] = "blablagmail.com"
        cls.assertFalse(LoginForm(data=temp_data).is_valid())

        temp_data['email'] = "blabla@gmailcom"
        cls.assertFalse(LoginForm(data=temp_data).is_valid())

        temp_data['email'] = "@."
        cls.assertFalse(LoginForm(data=temp_data).is_valid())

   

        

