from .models import UsersDB
from .PasswordManager import PasswordManager
from .ErrorCodes import ErrorCodes
import random
import string

class UsersManager(object):

  
    def getModelFromRegisterForm(cleaned_form):
        return UsersDB(firstName=cleaned_form['firstName'],
                            familyName=cleaned_form['familyName'],
                            email=cleaned_form['email'],
                            password=PasswordManager.hashPassword(cleaned_form['pass1']),
                            privLevel = 0,
                            number = cleaned_form['number'],
                            year = cleaned_form['year'])

    def validateInputFrom(newUser,cleaned_form):
        if cleaned_form['pass1'] != cleaned_form['pass2']:
            return ErrorCodes.REGISTER_INPUTS.PASSMISSMATCH
        if UsersDB.objects.filter(firstName=newUser.firstName,familyName=newUser.familyName).count():
            return ErrorCodes.REGISTER_INPUTS.USEREXISTS
        if UsersDB.objects.filter(email = newUser.email).count():
            return ErrorCodes.REGISTER_INPUTS.EMAILEXISTS
        return ErrorCodes.REGISTER_INPUTS.NONE

    def addNewUser(newUser):
        newUser.save()

    def getModelFromLoginForm(cleaned_form):
        return UsersDB.objects.filter(email = cleaned_form['email'])

    def generateRandomString(stringLength):
        letters = string.printable
        return ''.join(random.choice(letters) for i in range(stringLength))

    def checkUser(items_with_this_email,cleaned_form):
        mystr = generateRandomString(20)
        print(mystr)

        if items_with_this_email.count() == 0:
            return ErrorCodes.LOGIN_INPUTS.EMAIL_NOT_FOUND
        elif items_with_this_email.count() > 1:
            return ErrorCodes.LOGIN_INPUTS.EMAIL_MULTIPLES
        elif PasswordManager.chekPassword(cleaned_form['password'],items_with_this_email.first().password):
            return ErrorCodes.LOGIN_INPUTS.NONE
        else:
            return ErrorCodes.LOGIN_INPUTS.PASS_MISMATCH
    
    
    def saveSession(userQuery):
        userInfo = userQuery.first()
        userSession = userInfo.objects.filter(uid_id = userInfo.id)
        if userSession.count() == 0:
            newUserSession = UsersDB(uid_id = userInfo.id,)
    
    def checkSession(args):
        pass
    
    def changeSession(args):
        pass
        
    



