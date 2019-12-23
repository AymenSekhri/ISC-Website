from .models import UsersDB, SessionsDB, PassResetDB
from .PasswordManager import PasswordManager
from .ErrorCodes import ErrorCodes
import random
import string
from datetime import datetime, timedelta  
from django.utils import timezone

class UsersManager(object):

  
    def getModelFromRegisterForm(cleaned_form):
        return UsersDB(firstName=cleaned_form['firstName'],
                            familyName=cleaned_form['familyName'],
                            email=cleaned_form['email'],
                            password=PasswordManager.hashPassword(cleaned_form['pass1']),
                            privLevel = 0,
                            number = cleaned_form['number'],
                            year = cleaned_form['year'])

    def validateInputFrom(newUser,formPass1,formPass2):
        if formPass1 != formPass2:
            return ErrorCodes.REGISTER_INPUTS.PASSMISSMATCH
        if UsersDB.objects.filter(firstName=newUser.firstName,familyName=newUser.familyName).count():
            return ErrorCodes.REGISTER_INPUTS.USEREXISTS
        if UsersDB.objects.filter(email = newUser.email).count():
            return ErrorCodes.REGISTER_INPUTS.EMAILEXISTS
        return ErrorCodes.REGISTER_INPUTS.NONE

    def addNewUser(newUser):
        newUser.save()

    def getModelFromLoginForm(formEmail):
        return UsersDB.objects.filter(email = formEmail)

    def generateRandomString(stringLength):
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(stringLength))

    def checkUser(items_with_this_email,formPassword):
        if items_with_this_email.count() == 0:
            return ErrorCodes.LOGIN_INPUTS.EMAIL_NOT_FOUND
        elif items_with_this_email.count() > 1:
            return ErrorCodes.LOGIN_INPUTS.EMAIL_MULTIPLES
        elif PasswordManager.chekPassword(formPassword,items_with_this_email.first().password):
            return ErrorCodes.LOGIN_INPUTS.NONE
        else:
            return ErrorCodes.LOGIN_INPUTS.PASS_MISMATCH
    def checkEmail(items_with_this_email):
        if items_with_this_email.count() == 0:
            return ErrorCodes.FORGOT_INPUTS.EMAIL_NOT_FOUND
        else:
            return ErrorCodes.LOGIN_INPUTS.NONE
    
    
    def saveSession(userQuery,userAgent):
        # do check for null/valid for all input
        userInfo = userQuery.first()
        userSession = SessionsDB.objects.filter(uid_id = userInfo.id)
        newToken = UsersManager.generateRandomString(128)
        if userSession.count() == 0:
            newUserSession = SessionsDB(uid_id = userInfo.id, token = newToken, key = PasswordManager.hashPassword(userAgent,work=4) ,
                                     expiration_date = datetime.now() + timedelta(minutes=5))
            newUserSession.save()
        else:
            userSessionQuery = userSession.first()
            userSessionQuery.token = newToken
            userSessionQuery.key = PasswordManager.hashPassword(userAgent,work=4)
            userSessionQuery.expiration_date = timezone.now() + timedelta(minutes=5)
            userSessionQuery.save()
        return newToken

    def getUserFromId(UserId):
        return UsersDB.objects.get(id=UserId)

    def checkSession(user_id,session_id,userAgent):
        if str.isdigit(user_id) == False:
            return False
        if session_id == '':
            return False
        SessionQuery = SessionsDB.objects.filter(token=session_id)
        if SessionQuery.count() != 1:
            return False
        if SessionQuery.first().uid_id != int(user_id):
            return False
        if PasswordManager.chekPassword(userAgent,SessionQuery.first().key) == False:
            return False
        if SessionQuery.first().expiration_date < timezone.now():
            return False
        return True 
    
    def savePassResetToken(userQuery):
        newToken = UsersManager.generateRandomString(128)
        previousResetAttempts = PassResetDB.objects.filter(uid_id = userQuery.first().id)
        if previousResetAttempts.count() > 0:
            previousResetAttempts.delete()
        newPassReset =  PassResetDB(uid_id = userQuery.first().id, token = newToken,
                                   expiration_date = timezone.now() + timedelta(minutes=5))
        newPassReset.save()
        return newToken

    def isValidResetToken(formToken):
        tokenQuery = PassResetDB.objects.filter(token = formToken)
        if tokenQuery.count() != 1:
           return ErrorCodes.FORGOT_INPUTS.INVALID_TOKEN
        if tokenQuery.first().expiration_date < timezone.now():
           return ErrorCodes.FORGOT_INPUTS.INVALID_TOKEN
        return ErrorCodes.FORGOT_INPUTS.NONE
    
    def changePassword(formToken,password):
        userToken = PassResetDB.objects.filter(token = formToken).first().uid
        userToken.password = password=PasswordManager.hashPassword(password)
        userToken.save()

        sessionQuery = SessionsDB.objects.filter(uid_id = userToken.id).delete()
    
    def deleteToken(formToken):
        tokenQuery = PassResetDB.objects.filter(token = formToken).delete()


        
    



