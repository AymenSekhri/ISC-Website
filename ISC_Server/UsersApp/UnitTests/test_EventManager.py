import django
django.setup()
try:
    from django.test.utils import setup_test_environment# VS goes here
    setup_test_environment()
except :
    pass# Shell goes here

from django.test import TestCase
from ISC_Server.UsersApp.ErrorCodes import ErrorCodes
from ISC_Server.UsersApp.EventManager import EventManager
from ISC_Server.UsersApp.UsersManager import UsersManager

class EventsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(EventsTest, cls).setUpClass()
        django.setup()

    def setUp(cls):
        pass


    def test_CreateAnEvent(cls):
        pass

    def test_EnrollAnEvent(cls):
        pass


