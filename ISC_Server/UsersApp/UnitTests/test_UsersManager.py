"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""


import django
from django.test import TestCase
django.setup()

from ISC_Server.UsersApp.UsersManager import UsersManager


# TODO: Configure your database in settings.py and sync before running tests.


class UsersManagerTest(TestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(UsersManagerTest, cls).setUpClass()
        django.setup()


    def test_basic_addition2(self):
        self.assertEqual(1 + 1, 2)