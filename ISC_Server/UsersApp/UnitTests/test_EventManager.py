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
        newEventFormData1 = {'eventName': 'Machine Learning Bootcamp',
                            'picturePath': '0.png',
                            'description': 'You will learn genetic algorithm in this bootcamp',
                            'deadline_date': '10-04-2020',
                            'maxNumberOfEnrolment': 50,
                            'eventEnrolmentData': ''}
        newEventFormData2 = {'eventName': 'Malware Analysis Bootcamp',
                            'picturePath': '1.png',
                            'description': 'You will learn how to detect malwares',
                            'deadline_date': '20-04-2020',
                            'maxNumberOfEnrolment': 50,
                            'eventEnrolmentData': ''}

        cls.assertEqual(EventManager.validateEvent(newEventFormData1),ErrorCodes.EVENT_INPUTS.NONE)
        EventManager.createNewEvent(newEventFormData1)

        cls.assertEqual(EventManager.validateEvent(newEventFormData1),ErrorCodes.EVENT_INPUTS.EVENTEXISTS)

        cls.assertEqual(EventManager.validateEvent(newEventFormData2),ErrorCodes.EVENT_INPUTS.NONE)
        EventManager.createNewEvent(newEventFormData2)

        listOfEvents = EventManager.getListOfEvents()
        cls.assertEqual(len(listOfEvents),2)
        cls.assertEqual(listOfEvents[0]['name'],newEventFormData1['eventName'])
        cls.assertEqual(listOfEvents[1]['name'],newEventFormData2['eventName'])

    def test_EnrollAnEvent(cls):
        event_id = 0
        user_id = cls.addUser("1")
        user_id2 = cls.addUser("2")
        newEventFormData1 = {'eventName': 'Machine Learning Bootcamp',
                            'picturePath': '0.png',
                            'description': 'You will learn genetic algorithm in this bootcamp',
                            'deadline_date': '10-04-2020',
                            'maxNumberOfEnrolment': 50,
                            'eventEnrolmentData': ''}
        EventManager.createNewEvent(newEventFormData1)
        newEnrollment1 = {'eventID': event_id,
                        'userID': user_id,
                        'response': 'MachineLearningLevel:50,PythonLevel:30'}
        newEnrollment2 = {'eventID': event_id,
                        'userID': user_id2,
                        'response': 'MachineLearningLevel:50,PythonLevel:30'}
        cls.assertEqual(EventManager.validateEventEnrolment(newEnrollment1),ErrorCodes.EVENTENROLMENT_INPUTS.NONE)
        EventManager.createNewEventEnrolment(newEnrollment1)
        cls.assertEqual(EventManager.validateEventEnrolment(newEnrollment1),ErrorCodes.EVENTENROLMENT_INPUTS.DUPLICATES)
        cls.assertEqual(EventManager.validateEventEnrolment(newEnrollment2),ErrorCodes.EVENTENROLMENT_INPUTS.NONE)
        EventManager.createNewEventEnrolment(newEnrollment2)

        listOfEnrolments = EventManager.getEnrolmentOfEvent(event_id)
        cls.assertEqual(len(listOfEnrolments),2)
        print(listOfEnrolments)

    def addUser(cls,user):
        
        form_data = {'firstName': 'Aymen'+user,
                     'familyName': "Sekhri"+user,
                     'email': 'a11111@live.com',
                     'pass1': "123456789",
                     'pass2': "123456789",
                     'number': "100",
                     'year': "2020"}
        newUser = UsersManager.getModelFromRegisterForm(form_data)
        UsersManager.addNewUser(newUser)
        return newUser.id




