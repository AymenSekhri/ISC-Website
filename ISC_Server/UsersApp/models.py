from django.db import models
from django.utils import timezone
from .ErrorCodes import ErrorCodes
# Create your models here.

class UsersDB(models.Model):
    firstName = models.CharField(max_length=30)
    familyName = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=256)
    privLevel = models.SmallIntegerField(default = 4)
    number = models.CharField(max_length=20)
    year = models.CharField(max_length=4)
    regDate = models.DateField(default=timezone.now)

    def __str__(self):
        return self.firstName + " " + self.familyName

class SessionsDB(models.Model):
    uid = models.ForeignKey(UsersDB, on_delete=models.CASCADE)
    token = models.CharField(max_length=128)
    key = models.CharField(max_length=128)
    expiration_date = models.DateTimeField()
    
    def __str__(self):
        return self.token
    def is_expired(self):
        if slef.expiration_date > timezone.now:
            return False
        else:
            return True

class PassResetDB(models.Model):
    uid = models.ForeignKey(UsersDB, on_delete=models.CASCADE)
    token = models.CharField(max_length=128)
    expiration_date = models.DateTimeField()

class Event(models.Model):
    eventName = models.CharField(max_length=512)
    picture = models.CharField(max_length=128)#path to the picture.
    description = models.TextField()
    posting_date = models.DateTimeField(default=timezone.now)
    enrolemntDeadline_date = models.DateTimeField()
    event_date = models.DateTimeField()
    maxNumberOfEnrolment = models.IntegerField(default = 200)
    numberOfEnrolment = models.IntegerField(default = 0)
    eventEnrolmentData = models.TextField()
    status = models.SmallIntegerField(default = 0)#0: ongoing/ 1:postponded/ 3:canceled

class EventEnrolment(models.Model):#Joint Many-To-Many Table.
    eventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    userID = models.ForeignKey(UsersDB, on_delete=models.CASCADE)
    enrolemnt_date = models.DateTimeField(default=timezone.now)
    enrolmentResponse = models.TextField()
    decision = models.SmallIntegerField(default = 0)# 0:pending/1:accepted/2:rejected.
