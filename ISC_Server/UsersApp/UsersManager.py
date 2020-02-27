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
                            privLevel = 0xFFFFFFFF,
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
                                     expiration_date = timezone.now() + timedelta(minutes=5))
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
            return False,0
        if session_id == '':
            return False,0
        SessionQuery = SessionsDB.objects.filter(token=session_id)
        if SessionQuery.count() != 1:
            return False,0
        if SessionQuery.first().uid_id != int(user_id):
            return False,0
        if PasswordManager.chekPassword(userAgent,SessionQuery.first().key) == False:
            return False,0
        if SessionQuery.first().expiration_date < timezone.now():
            return False,0

        return True, SessionQuery.first().uid.privLevel
        
    
    def deleteSession(user_id,session_id):
        Query = SessionsDB.objects.filter(uid_id = user_id, token=session_id)
        if Query.exists() :
            Query.delete()
    
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
           #TODO: should i delete it ?
           #tokenQuery.first().delete() 
           return ErrorCodes.FORGOT_INPUTS.INVALID_TOKEN
        return ErrorCodes.FORGOT_INPUTS.NONE
    
    def changePassword(formToken,password):
        userToken = PassResetDB.objects.filter(token = formToken).first().uid
        userToken.password = password=PasswordManager.hashPassword(password)
        userToken.save()

        sessionQuery = SessionsDB.objects.filter(uid_id = userToken.id).delete()
    
    def deleteToken(formToken):
        tokenQuery = PassResetDB.objects.filter(token = formToken)
        if tokenQuery.exists() :
            tokenQuery.delete()

    def getUsersList():
        members = []
        for x in UsersDB.objects.all():
            memberInfo = {'id':x.id,
                          'firstName':x.firstName,
                          'familyName': x.familyName,
                          'number': x.number,
                          'year': x.year}
            members.append(memberInfo)
        return members

    def getUserDetails(id):
        query = UsersDB.objects.filter(id = id)
        if query.exists():
            x = query.first()
            memberInfo = {  'id':x.id,
                            'firstName':x.firstName,
                            'familyName': x.familyName,
                            #'picture': x.picture,
                            'regDate': str(x.regDate),
                            'email': x.email,
                            'number': x.number,
                            'year': x.year,
                            'permissions':UsersManager.getPermissions(x.privLevel)}
            return ErrorCodes.TEAMUSERS.VALID_USER,memberInfo
        return ErrorCodes.TEAMUSERS.INVALID_USER, {}

    def editUser(id,firstName,familyName,email,number):
        member = UsersDB.objects.filter(id = id).first()
        member.firstName = firstName
        member.familyName = familyName
        member.email = email
        member.number = number
        member.save()
        return ErrorCodes.TEAMUSERS.VALID_USER

    def upgradeUser(id, newLevel):
        member = UsersDB.objects.filter(id = id).first()
        member.privLevel = newLevel
        member.save()
        return ErrorCodes.TEAMUSERS.VALID_USER

    def deleteUser(id):
        member = UsersDB.objects.filter(id = id).first()
        member.delete()
        return ErrorCodes.TEAMUSERS.VALID_USER

    def getPermissions(userPermission):
        permissions ={'CreateEvent': False,
                       'PostponeEvent': False,
                       'ManageEvent': False,
                       'EnrollEvent': False,
                       'ViewEnrollments': False,
                       'Decision': False,
                       'CreateNews': False,
                       'EditNews': False,
                       'DeleteNews': False,
                       'CreateProject': False,
                       'EditProject': False,
                       'DeleteProject': False,
                       'TeamAdd': False,
                       'TeamEdit': False,
                       'TeamDelete': False,
                       'UsersList': False,
                       'ViewUserInfo': False,
                       'EditUserInfo': False,
                       'DeleteUser': False,
                       'ChangeUserPermission': False}

        
        if (userPermission & UserPermission.ChangeUserPermission):
            permissions['ChangeUserPermission'] = True
        if (userPermission & UserPermission.CreateEvent):
            permissions['CreateEvent'] = True
        if (userPermission & UserPermission.CreateNews):
            permissions['CreateNews'] = True
        if (userPermission & UserPermission.CreateProject):
            permissions['CreateProject'] = True
        if (userPermission & UserPermission.Decision):
            permissions['Decision'] = True
        if (userPermission & UserPermission.DeleteNews):
            permissions['DeleteNews'] = True
        if (userPermission & UserPermission.DeleteProject):
            permissions['DeleteProject'] = True
        if (userPermission & UserPermission.DeleteUser):
            permissions['DeleteUser'] = True
        if (userPermission & UserPermission.EditNews):
            permissions['EditNews'] = True
        if (userPermission & UserPermission.EditProject):
            permissions['EditProject'] = True
        if (userPermission & UserPermission.TeamEdit):
            permissions['EditTeam'] = True
        if (userPermission & UserPermission.EditUserInfo):
            permissions['EditUserInfo'] = True
        if (userPermission & UserPermission.EditUserInfo):
            permissions['EditUserInfo'] = True
        if (userPermission & UserPermission.ManageEvent):
            permissions['ManageEvent'] = True
        if (userPermission & UserPermission.PostponeEvent):
            permissions['PostponeEvent'] = True
        if (userPermission & UserPermission.TeamAdd):
            permissions['TeamAdd'] = True
        if (userPermission & UserPermission.TeamDelete):
            permissions['TeamDelete'] = True
        if (userPermission & UserPermission.UsersList):
            permissions['UsersList'] = True
        if (userPermission & UserPermission.ViewEnrollments):
            permissions['ViewEnrollments'] = True
        if (userPermission & UserPermission.ViewUserInfo):
            permissions['ViewUserInfo'] = True
        return permissions

class UserPermission(object):
    VALIDUSER = 0
    CreateEvent = 0x01
    PostponeEvent = 0x02
    ManageEvent = 0x04
    EnrollEvent	= 0x08
    ViewEnrollments = 0x10
    Decision = 0x20

    CreateNews	= 0x40
    EditNews	= 0x80	
    DeleteNews	= 0x100

    CreateProject = 0x200
    EditProject	= 0x400
    DeleteProject = 0x800

    TeamAdd	 = 0x1000
    TeamEdit = 0x2000
    TeamDelete = 0x4000

    UsersList = 0x8000
    ViewUserInfo = 0x10000
    EditUserInfo = 0x20000
    DeleteUser	= 0x40000
    ChangeUserPermission = 0x80000

    

        
    



