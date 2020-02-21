from .models import *
from .PasswordManager import PasswordManager
from .ErrorCodes import ErrorCodes
import random
import string
from datetime import datetime, timedelta  
from django.utils import timezone


class EventManager(object):
    def isValidDate(date):
        try:
            timezone.datetime.strptime(formData['event_date'], "%d-%m-%Y %H:%M")
            return True
        except :
            return False
        

    def validateEvent(formData):
        if Event.objects.filter(eventName = formData['eventName']).exists():
            return ErrorCodes.EVENT_INPUTS.EVENTEXISTS
        if EventManager.isValidDate(formData['deadline_date']+ " 23:59"):
            return ErrorCodes.EVENT_INPUTS.INVALIDDATEFORMAT
        if EventManager.isValidDate(formData['event_date']):
            return ErrorCodes.EVENT_INPUTS.INVALIDDATEFORMAT
        return ErrorCodes.EVENT_INPUTS.NONE

    def createNewEvent(formData):
        event = Event.objects.create(eventName = formData['eventName'],
                             picture = "picturePath",#TODO: save picture in some path and edit this here.
                             description = formData['description'],
                             enrolemntDeadline_date = timezone.datetime.strptime(formData['deadline_date']+ " 23:59", "%d-%m-%Y %H:%M"),
                             event_date = timezone.datetime.strptime(formData['event_date'], "%d-%m-%Y %H:%M"),
                             maxNumberOfEnrolment = formData['maxNumberOfEnrolment'],
                             eventEnrolmentData = formData['enrollmentData'])
        return event.id

    def validateEventEnrolment(eventID,userID):
        if Event.objects.filter(id = eventID).exists() == False:
            return ErrorCodes.EVENTENROLMENT_INPUTS.EVENTDOESNOTEXISTS
        elif EventEnrolment.objects.filter(eventID = eventID,userID = userID).exists():
            return ErrorCodes.EVENTENROLMENT_INPUTS.DUPLICATES
        elif Event.objects.filter(id = eventID).first().enrolemntDeadline_date < timezone.now():
            return ErrorCodes.EVENTENROLMENT_INPUTS.ENROLLMENTPASTDEADLINE
        return ErrorCodes.EVENTENROLMENT_INPUTS.NONE

    def createNewEventEnrolment(eventID,userID,response):
        EventEnrolment.objects.create(eventID_id = eventID,
                             userID_id = userID,
                             enrolmentResponse = response)

    def makeEnrolmentDecision(eventID,userID,decision):
        enrollmentQuery = EventEnrolment.objects.filter(eventID = eventID,userID = userID)
        if enrollmentQuery.exists():
            enrollment = enrollmentQuery.first()
            enrollment.decision = decision
            enrollment.save()
            return ErrorCodes.EVENT_INPUTS.NONE
        else:
            return ErrorCodes.EVENT_INPUTS.EVENTDOESNOTEXISTS        

    def getListOfEvents():
        events = []
        for x in Event.objects.all():
            eventInfo = {'id':x.id,
                         'name':x.eventName,
                         'picture': x.picture,
                         'description': x.description,
                         'deadline_date': str(x.enrolemntDeadline_date),
                         'event_date': str(x.event_date),
                         'eventStatus': x.status}
            events.append(eventInfo)
        return events

    def checkEvent(id):
        eventQuery = Event.objects.filter(id = id)
        if eventQuery.exists():
            return ErrorCodes.EVENTMANAGMENT_INPUTS.NONE
        else:
            return ErrorCodes.EVENTMANAGMENT_INPUTS.EVENTDOESNOTEXISTS

    def getEventInfo(id):
        eventQuery = Event.objects.filter(id = id)
        if eventQuery.exists():
             x = eventQuery.first()
             return ErrorCodes.EVENTMANAGMENT_INPUTS.NONE, {'name':x.eventName,
                     'picture': x.picture,
                     'description': x.description,
                     'maxNumberOfEnrolment': x.maxNumberOfEnrolment,
                     'numberOfEnrolment': x.numberOfEnrolment,
                     'posting_date': str(x.posting_date),
                     'event_date': str(x.event_date),
                     'deadline_date': str(x.enrolemntDeadline_date),
                     'eventEnrolmentData': x.eventEnrolmentData,
                     'eventStatus': x.status}
        else:
            return ErrorCodes.EVENTMANAGMENT_INPUTS.EVENTDOESNOTEXISTS, {}

    def getEnrolmentOfEvent(EventID):
        enrolment = []
        for x in EventEnrolment.objects.filter(eventID_id = EventID):
            userQuery = x.userID
            enrolmentInfo = {'id':userQuery.id,
                         'name':userQuery.firstName + " " + x.userID.familyName,
                         'email': userQuery.email,
                         'year': userQuery.year,
                         'enrolemnt_date': x.enrolemnt_date,
                         'enrolmentResponse': x.enrolmentResponse,
                         'decision': x.decision}
            enrolment.append(enrolmentInfo)
        return enrolment

    def getEnrolmentOfUser(UserID):
        enrolment = []
        for x in EventEnrolment.objects.filter(userID_id = UserID):
            enrolmentInfo = {'name':x.eventID.eventName,
                         'enrolemnt_date': x.enrolemnt_date,
                         'decision': x.decision}
            enrolment.append(enrolmentInfo)
        return enrolment

    def postponeEvent(eventID,newDate):
        if EventManager.isValidDate(newDate):
            return ErrorCodes.EVENT_INPUTS.INVALIDDATEFORMAT
        eventQuery = Event.objects.filter(id = eventID)
        if eventQuery.exists():
            event = eventQuery.first()
            event.event_date = timezone.datetime.strptime(newDate, "%d-%m-%Y %H:%M")
            event.status = EventStatus.POSTPONED
            event.save()
            return ErrorCodes.EVENT_INPUTS.NONE
        else:
            return ErrorCodes.EVENT_INPUTS.EVENTDOESNOTEXISTS

    def postponeDeadline(eventID,newDate):
        if EventManager.isValidDate(newDate):
            return ErrorCodes.EVENT_INPUTS.INVALIDDATEFORMAT
        eventQuery = Event.objects.filter(id = eventID)
        if eventQuery.exists():
            event = eventQuery.first()
            event.enrolemntDeadline_date = timezone.datetime.strptime(newDate+ " 23:59", "%d-%m-%Y %H:%M")
            event.save()
            return ErrorCodes.EVENT_INPUTS.NONE
        else:
            return ErrorCodes.EVENT_INPUTS.EVENTDOESNOTEXISTS

    def cancelEvent(eventID):
        eventQuery = Event.objects.filter(id = eventID)
        if eventQuery.exists():
            event = eventQuery.first()
            event.status = EventStatus.CANCELED
            event.save()
            return ErrorCodes.EVENTMANAGMENT_INPUTS.NONE
        else:
            return ErrorCodes.EVENTMANAGMENT_INPUTS.EVENTDOESNOTEXISTS

    def removeEvent(eventID):
        eventQuery = Event.objects.filter(id = eventID)
        if eventQuery.exists():
            eventQuery.first().delete()
            return ErrorCodes.EVENTMANAGMENT_INPUTS.NONE
        else:
            return ErrorCodes.EVENTMANAGMENT_INPUTS.EVENTDOESNOTEXISTS




class EnrolementDecision(object):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2

class EventStatus(object):
    ONGOING = 0
    POSTPONED = 1
    CANCELED = 2