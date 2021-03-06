from django.shortcuts import render
from .forms import *
from .UsersManager import *
from .EventManager import *
from .PostsManager import *
from .TeamManager import *
from .ErrorCodes import ErrorCodes
from colorama import Fore, Back, Style,init
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
import json

init()
def printf(text,color):
     print(color + text)
     print(Style.RESET_ALL)

def getCurrentUserInfo(request):
    user_id = request.COOKIES['user_id']
    userQuery = UsersManager.getUserFromId(user_id)
    return JsonResponse({'Status':0,
                         'Data':{
                            'id':userQuery.id,
                            'firstName':userQuery.firstName,
                            'familyName':userQuery.familyName,
                            'email':userQuery.email,
                            'number':userQuery.number,
                            'permissions':UsersManager.getPermissions(userQuery.privLevel)}})

def register(request):
    myform = RegisterForm(request.POST)
    if myform.is_valid():
        printf("Registration Request..",Fore.GREEN)
        myform.toLower()
        myform_cleaned = myform.cleaned_data
        newUser = UsersManager.getModelFromRegisterForm(myform_cleaned)
        result = UsersManager.validateInputFrom(newUser,myform_cleaned['pass1'],myform_cleaned['pass2'])
        if result == ErrorCodes.REGISTER_INPUTS.NONE:
            UsersManager.addNewUser(newUser)
            printf("Registration Completed",Fore.GREEN)
        elif result == ErrorCodes.REGISTER_INPUTS.PASSMISSMATCH:
            printf("data not valid : INVALID_INPUTS_PASSMISSMATCH",Fore.RED)
        elif result == ErrorCodes.REGISTER_INPUTS.EMAILEXISTS:
            printf("data not valid : INVALID_INPUTS_EMAILEXISTS",Fore.RED)
        elif result == ErrorCodes.REGISTER_INPUTS.USEREXISTS:
            printf("data not valid : INVALID_INPUTS_USEREXISTS",Fore.RED)
        else:
            printf("This should not happen!!!",Fore.RED)
        return JsonResponse({'Status':result})
    else:
        return HttpResponse(status=400)

def login(request):
    myform = LoginForm(request.POST)
    
    if myform.is_valid():
        myform.toLower()
        myform_cleaned = myform.cleaned_data
        userQuery = UsersManager.getModelFromLoginForm(myform_cleaned['email'])
        result = UsersManager.checkUser(userQuery,myform_cleaned['password'])
        if result == ErrorCodes.LOGIN_INPUTS.NONE:
            printf("Successful Login.",Fore.GREEN)
            newToken = UsersManager.saveSession(userQuery,request.META['HTTP_USER_AGENT'])
            response = JsonResponse({'Status':0})
            response.set_cookie('session_id',newToken)
            response.set_cookie('user_id',userQuery.first().id)
            return response
        else:
            if result == ErrorCodes.LOGIN_INPUTS.EMAIL_NOT_FOUND:
                printf("Email does not exist!",Fore.RED)
            elif result == ErrorCodes.LOGIN_INPUTS.PASS_MISMATCH:
                printf("Wrong password!",Fore.RED)
            return JsonResponse({'Status':result})
    else:
        return HttpResponse(status=400)

def logout(request):
    response = JsonResponse({'Status':0})
    user_id = request.COOKIES['user_id']
    session_id = request.COOKIES['session_id']
    UsersManager.deleteSession(user_id,session_id)
    response.delete_cookie('session_id','')
    response.delete_cookie('user_id','')
    return response

def forgotPassword(request):
    myform = ForgotForm(request.POST)
    if myform.is_valid():
        myform.toLower()
        userQuery = UsersManager.getModelFromLoginForm(myform.cleaned_data['email'])
        result = UsersManager.checkEmail(userQuery)
        if result == ErrorCodes.FORGOT_INPUTS.NONE:
            Token = UsersManager.savePassResetToken(userQuery)
            printf("Password reset token = " + Token,Fore.GREEN)
            #TODO: send token to the email
        elif result == ErrorCodes.FORGOT_INPUTS.EMAIL_NOT_FOUND :
            error = 1
            printf("Email does not exist.",Fore.RED)
        return JsonResponse({'Status':result})
    
    else:
        return HttpResponse(status=400)

def ResetPassword(request):
    myform = ResetForm(request.POST)
    if myform.is_valid():
        myform_cleaned = myform.cleaned_data
        fromToken = myform_cleaned['token']
        fromPass = myform_cleaned['password']
        result = UsersManager.isValidResetToken(fromToken)
        if  result == ErrorCodes.FORGOT_INPUTS.NONE:
            UsersManager.changePassword(fromToken,fromPass)
            UsersManager.deleteToken(fromToken)
        elif result == ErrorCodes.FORGOT_INPUTS.INVALID_TOKEN:
            printf("Email does not exists.",Fore.RED)
        return JsonResponse({'Status':result})
    else:
        return HttpResponse(status=400)


def createEvent(request):
    myform = CreateEventForm(request.POST)
    if myform.is_valid():
        myform_cleaned = myform.cleaned_data
        result = EventManager.validateEvent(myform_cleaned)
        if result == ErrorCodes.EVENT_INPUTS.NONE:
            id = EventManager.createNewEvent(myform_cleaned)
            return JsonResponse({'Status':result,'Data':{'eventID':id}})
        return JsonResponse({'Status':result,'Data':{}})
    return HttpResponse(status=400)

def enrollEvent(id, request):
    user_id = request.COOKIES['user_id']
    myform = EnrollEventForm(request.POST)
    if myform.is_valid():
        myform_cleaned = myform.cleaned_data
        result = EventManager.validateEventEnrolment(id,user_id)
        if result == ErrorCodes.EVENTENROLMENT_INPUTS.NONE:
            EventManager.createNewEventEnrolment(id,user_id,myform_cleaned['response'])
        return JsonResponse({'Status':result})
    return HttpResponse(status=400)

def getEventsList():
    return JsonResponse(data = {'Status':0,
                                        'Data':EventManager.getListOfEvents()})

def getEventInfo(id):
    result, data = EventManager.getEventInfo(id)
    if result == ErrorCodes.EVENT_INPUTS.NONE:
        return JsonResponse(data = {'Status':0,'Data':data})
    else:
        return HttpResponse(status=404)

def ManageEvent(id, request):
    user_id = request.COOKIES['user_id']
    myform = ManageEventsForm(request.POST)
    if myform.is_valid():
        myform_cleaned = myform.cleaned_data
        if myform_cleaned['cmd'] == 'rm':
            #remove event
            return JsonResponse(data = {'Status':EventManager.removeEvent(id)})
        elif myform_cleaned['cmd'] == 'cnl':
            #cancel event
            return JsonResponse(data = {'Status':EventManager.cancelEvent(id)})
        elif myform_cleaned['cmd'] == 'snd':
            #send email to accepted people
            return JsonResponse({'Status':0})
    return HttpResponse(status=400)

def getEnrollmentList(id, request):
    user_id = request.COOKIES['user_id']
    return JsonResponse(data = {'Status':0,
                                    'Data':EventManager.getEnrolmentOfEvent(id)})


def makeEnrollmentDecision(id, request):
    user_id = request.COOKIES['user_id']
    myform = DecisionForm(request.POST)
    if myform.is_valid():
        myform_cleaned = myform.cleaned_data
        return JsonResponse(data = {'Status':EventManager.makeEnrolmentDecision(id,myform_cleaned['userID'], myform_cleaned['decision'])})
    return HttpResponse(status=400)

def postponeEvent(id, request):
    user_id = request.COOKIES['user_id']
    myform = PostponeEventsForm(request.POST)
    if myform.is_valid():
        myform_cleaned = myform.cleaned_data
        if myform_cleaned['cmd'] == 'pse':
            #postpone event
            return JsonResponse(data = {'Status':EventManager.postponeEvent(id,myform_cleaned['newDate'])})
        elif myform_cleaned['cmd'] == 'pdl':
            #postpone event's deadline
            return JsonResponse(data = {'Status':EventManager.postponeDeadline(id,myform_cleaned['newDate'])})
    return HttpResponse(status=400)

def createPost(request,type):
    user_id = request.COOKIES['user_id']
    myform = PostsForm(request.POST)
    if myform.is_valid():
        myform_cleaned = myform.cleaned_data
        return JsonResponse(data = {'Status': 0,
                                    'Data': PostManager.createPost(user_id,type,
                                                                         myform_cleaned['title'],
                                                                         myform_cleaned['content'],
                                                                         myform_cleaned['tags'])})
    return HttpResponse(status=400)

def getPostsList(type):
    return JsonResponse(data = {'Status': 0,
                                    'Data': PostManager.getPostsList(type)})

def getPostDetails(id,type):
    result , data = PostManager.getPostDetails(id,type)
    if result == ErrorCodes.POSTS.VALID_POST:
        return JsonResponse(data = {'Status': 0,
                                'Data': data})
    else:
        return HttpResponse(status=404)

def editPost(id,type, request):
    user_id = request.COOKIES['user_id']
    myform = PostsForm(request.POST)
    if myform.is_valid():
        myform_cleaned = myform.cleaned_data
        result , data = PostManager.getPostDetails(id,type)
        if result == ErrorCodes.POSTS.VALID_POST:
            return JsonResponse(data = {'Status':PostManager.editPost( id,
                                                                        myform_cleaned['title'],
                                                                        myform_cleaned['content'],
                                                                        myform_cleaned['tags'])})
        else:
            return HttpResponse(status=404)
    return HttpResponse(status=400)

def deletePost(id, type, request):
    user_id = request.COOKIES['user_id']
    result , data = PostManager.getPostDetails(id, type)
    if result == ErrorCodes.POSTS.VALID_POST:
        return JsonResponse(data = {'Status':PostManager.deletePost(id)})
    else:
        return HttpResponse(status=404)

#members

def editMember(id, request):
    user_id = request.COOKIES['user_id']
    myform = EditMemberFrom(request.POST)
    if myform.is_valid():
        myform_cleaned = myform.cleaned_data
        if TeamManager.checkTeamMember(id) == ErrorCodes.TEAMUSERS.VALID_USER:
            return JsonResponse(data = {'Status':TeamManager.editMember( id,
                                                                        myform_cleaned['title'],
                                                                        myform_cleaned['bio'],
                                                                        myform_cleaned['contacts'])})
        else:
            return HttpResponse(status=404)
    return HttpResponse(status=400)

def addMember(request):
    user_id = request.COOKIES['user_id']
    myform = AddToTeamFrom(request.POST)
    if myform.is_valid():
        myform_cleaned = myform.cleaned_data
        if TeamManager.checkMemberUserID(myform_cleaned['userID']) == ErrorCodes.TEAMUSERS.INVALID_USER:
            return JsonResponse(data = {'Status': 0,
                                        'Data': TeamManager.AddMember(
                                                                        myform_cleaned['userID'],
                                                                        myform_cleaned['title'],
                                                                        myform_cleaned['bio'],
                                                                        myform_cleaned['contacts'])})
        else:
            return JsonResponse(data = {'Status': ErrorCodes.TEAMUSERS.DUPLICATED_USER, 'Data': {}})
    return HttpResponse(status=400)

def getMembers():
    return JsonResponse(data = {'Status': 0,
                                'Data': TeamManager.getTeamList()})

def deleteMember(id, request):
    user_id = request.COOKIES['user_id']
    if TeamManager.checkTeamMember(id) == ErrorCodes.TEAMUSERS.VALID_USER:
        return JsonResponse(data = {'Status':TeamManager.deleteMember(id)})
    else:
        return HttpResponse(status=404)

#users
def getUsersList(request):
    return JsonResponse(data = {'Status': 0,
                            'Data': UsersManager.getUsersList()})

def getUserDetails(id):
    result ,data = UsersManager.getUserDetails(id)
    if result == ErrorCodes.TEAMUSERS.VALID_USER:
        return JsonResponse(data = {'Status': 0,
                             'Data': data})
    else:
         return HttpResponse(status=404)

def editUserProfile(id, request):
    myform = EditUserFrom(request.POST)
    if myform.is_valid():
        myform_cleaned = myform.cleaned_data
        result ,data = UsersManager.getUserDetails(id)
        if result == ErrorCodes.TEAMUSERS.VALID_USER:
            return JsonResponse(data = {'Status':UsersManager.editUser( id,
                                                                        myform_cleaned['firstName'],
                                                                        myform_cleaned['familyName'],
                                                                        myform_cleaned['email'],
                                                                        myform_cleaned['number'])})
        else:
            return HttpResponse(status=404)
    return HttpResponse(status=400)

def deleteUser(id):
    result ,data = UsersManager.getUserDetails(id)
    if result == ErrorCodes.TEAMUSERS.VALID_USER:
        return JsonResponse(data = {'Status':UsersManager.deleteUser(id)})
    else:
        return HttpResponse(status=404)

def upgradeUser(id, request):
    myform = UpgradeUserForm(request.POST)
    if myform.is_valid():
        myform_cleaned = myform.cleaned_data
        result ,data = UsersManager.getUserDetails(id)
        if result == ErrorCodes.TEAMUSERS.VALID_USER:
            return JsonResponse(data = {'Status':UsersManager.upgradeUser(id, myform_cleaned['newLevel'])})
        else:
            return HttpResponse(status=404)
    return HttpResponse(status=400)


def checkPrivLevel(request,level):
    if ('user_id' in request.COOKIES) and ('session_id' in request.COOKIES) and ('HTTP_USER_AGENT' in request.META):
        user_id = request.COOKIES['user_id']
        session_id = request.COOKIES['session_id']
        userAgent = request.META['HTTP_USER_AGENT']
        isValidUser, userPermission = UsersManager.checkSession(user_id,session_id,userAgent)
        if isValidUser == False:
            return False
        elif (level == UserPermission.VALIDUSER) and (isValidUser == True):
            return True
        elif (level == UserPermission.ChangeUserPermission) and (userPermission & UserPermission.ChangeUserPermission):
            return True
        elif (level == UserPermission.CreateEvent) and (userPermission & UserPermission.CreateEvent):
            return True
        elif (level == UserPermission.CreateNews) and (userPermission & UserPermission.CreateNews):
            return True
        elif (level == UserPermission.CreateProject) and (userPermission & UserPermission.CreateProject):
            return True
        elif (level == UserPermission.Decision) and (userPermission & UserPermission.Decision):
            return True
        elif (level == UserPermission.DeleteNews) and (userPermission & UserPermission.DeleteNews):
            return True
        elif (level == UserPermission.DeleteProject) and (userPermission & UserPermission.DeleteProject):
            return True
        elif (level == UserPermission.DeleteUser) and (userPermission & UserPermission.DeleteUser):
            return True
        elif (level == UserPermission.EditNews) and (userPermission & UserPermission.EditNews):
            return True
        elif (level == UserPermission.EditProject) and (userPermission & UserPermission.EditProject):
            return True
        elif (level == UserPermission.TeamEdit) and (userPermission & UserPermission.TeamEdit):
            return True
        elif (level == UserPermission.EditUserInfo) and (userPermission & UserPermission.EditUserInfo):
            return True
        elif (level == UserPermission.EnrollEvent) and (userPermission & UserPermission.EnrollEvent):
            return True
        elif (level == UserPermission.ManageEvent) and (userPermission & UserPermission.ManageEvent):
            return True
        elif (level == UserPermission.PostponeEvent) and (userPermission & UserPermission.PostponeEvent):
            return True
        elif (level == UserPermission.TeamAdd) and (userPermission & UserPermission.TeamAdd):
            return True
        elif (level == UserPermission.TeamDelete) and (userPermission & UserPermission.TeamDelete):
            return True
        elif (level == UserPermission.UsersList) and (userPermission & UserPermission.UsersList):
            return True
        elif (level == UserPermission.ViewEnrollments) and (userPermission & UserPermission.ViewEnrollments):
            return True
        elif (level == UserPermission.ViewUserInfo) and (userPermission & UserPermission.ViewUserInfo):
            return True
        return False


class POST_TYPE(object):
        PROJECT = 0
        NEWS = 1
#TODO: Do logs for all operations specially the ones with 400 error 'cause it's probably hacking attempts
