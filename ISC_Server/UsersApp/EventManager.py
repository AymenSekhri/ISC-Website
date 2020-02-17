from .models import UsersDB, SessionsDB, PassResetDB, Event, EventEnrolment
from .PasswordManager import PasswordManager
from .ErrorCodes import ErrorCodes
import random
import string
from datetime import datetime, timedelta  
from django.utils import timezone


class EventManager(object):

    def validateEvent(formData):
        if Event.objects.filter(eventName = formData['eventName']).exists():
            return ErrorCodes.EVENT_INPUTS.EVENTEXISTS
        return ErrorCodes.EVENT_INPUTS.NONE

    def createNewEvent(formData):
        Event.objects.create(eventName = formData['eventName'],
                             picture = "picturePath",#TODO: save picture in some path and edit this here.
                             description = formData['description'],
                             enrolemntDeadline_date = timezone.datetime.strptime(formData['deadline_date']+ " 23:59", "%d-%m-%Y %H:%M"),
                             event_date = timezone.datetime.strptime(formData['event_date'], "%d-%m-%Y %H:%M"),
                             maxNumberOfEnrolment = formData['maxNumberOfEnrolment'],
                             eventEnrolmentData = formData['enrollmentData'])

    def validateEventEnrolment(formData):
        if EventEnrolment.objects.filter(eventID = formData['eventID'],userID = formData['userID']).exists():
            return ErrorCodes.EVENTENROLMENT_INPUTS.DUPLICATES
        return ErrorCodes.EVENTENROLMENT_INPUTS.NONE

    def createNewEventEnrolment(formData):
        EventEnrolment.objects.create(eventID_id = formData['eventID'],
                             userID_id = formData['userID'],
                             enrolmentResponse = formData['response'])

    def makeEnrolmentDecision(decision):
        enrolmentQuery = EventEnrolment.objects.filter(eventID = formData['eventID'],userID = formData['userID'])
        if enrolmentQuery.exists():
            userQuery = enrolmentQuery.first().eventID
            if userQuery.maxNumberOfEnrolment > userQuery.numberOfEnrolment:
                query.first().decision = decision
                userQuery.numberOfEnrolment =  userQuery.numberOfEnrolment + 1
                return ErrorCodes.EVENTENROLMENT_INPUTS.NONE
            else:
                return ErrorCodes.EVENTENROLMENT_INPUTS.MAXNUMBEROFENROLMENTS
        else:
            return ErrorCodes.EVENTENROLMENT_INPUTS.EVENTDOESNOTEXISTS        

    def getListOfEvents():
        events = []
        for x in Event.objects.all():
            eventInfo = {'name':x.eventName,
                         'picture': x.picture,
                         'description': x.description,
                         'deadline_date': str(x.enrolemntDeadline_date),
                         'event_date': str(x.event_date)}
            events.append(eventInfo)
        return events

    def getEnrolmentOfEvent(EventID):
        enrolment = []
        for x in EventEnrolment.objects.filter(eventID_id = EventID):
            userQuery = x.userID
            enrolmentInfo = {'name':userQuery.firstName + " " + x.userID.familyName,
                         'email': userQuery.email,
                         'year': userQuery.year,
                         'enrolemnt_date': x.enrolemnt_date,
                         'enrolmentResponse': x.enrolmentResponse,
                         'decision': x.decision}
            enrolment.append(enrolmentInfo)
        return enrolment

    def GetEnrolmentOfUser(UserID):
        enrolment = []
        for x in EventEnrolment.objects.filter(userID_id = UserID):
            enrolmentInfo = {'name':x.eventID.eventName,
                         'enrolemnt_date': x.enrolemnt_date,
                         'decision': x.decision}
            enrolment.append(enrolmentInfo)
        return enrolment

class EnrolementDecision(object):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2