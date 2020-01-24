from django.db import models
from django.utils import timezone
from .ErrorCodes import ErrorCodes
# Create your models here.

class UsersDB(models.Model):
    firstName = models.CharField(max_length=30)
    familyName = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=256)
    privLevel = models.IntegerField(default = 0)
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