from ISC_Server.UsersApp.ErrorCodes import ErrorCodes
from ISC_Server.UsersApp.EventManager import EventManager

class EventsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(LoginAndRegisterTest, cls).setUpClass()
        django.setup()

    def setUp(cls):
        pass


    def test_CreatAnEvent(cls):
        newEventFormData = {'eventName': 'Machine Learning Bootcamp',
                            'picturePath': '0.png',
                            'description': 'You will learn genetic algorithm in this bootcamp',
                            'deadline_date': '10-04-2020',
                            'maxNumberOfEnrolment': 50,
                            'eventEnrolmentData': ''}
        EventManager.createNewEvent(newEventFormData)
        printf(EventManager.getListOfEvents)