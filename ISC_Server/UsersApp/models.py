from django.db import models
from django.utils import timezone

# Create your models here.

class UsersDB(models.Model):
    firstName = models.CharField(max_length=30)
    familyName = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=256)
    salt = models.CharField(max_length=256)
    privLevel = models.IntegerField(default = 0)
    number = models.CharField(max_length=20)
    year = models.CharField(max_length=4)
    regDate = models.DateField(default=timezone.now)


    #Error Code
    INVALID_INPUTS_NONE = 0
    INVALID_INPUTS_USEREXISTS = 1
    INVALID_INPUTS_EMAILEXISTS = 2

    def validateInputs(self):
        if UsersDB.objects.filter(firstName=self.firstName,familyName=self.familyName).count():
            return False,self.INVALID_INPUTS_USEREXISTS

        if UsersDB.objects.filter(email = self.email).count():
            return False,self.INVALID_INPUTS_EMAILEXISTS

        return True,self.INVALID_INPUTS_NONE
        
    def __str__(self):
        return self.firstName + " " + self.familyName