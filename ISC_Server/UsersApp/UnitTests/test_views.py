"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
django.setup()
from django.test import TestCase
import ISC_Server.UsersApp.views
# TODO: Configure your database in settings.py and sync before running tests.

class SimpleTest(TestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(SimpleTest, cls).setUpClass()
        django.setup()

    def setUp(cls):
        pass

    def test_basic_addition3(self):
        self.assertEqual(1 + 1, 2)