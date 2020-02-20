from django.shortcuts import render
from django.http import HttpResponse
from .API_Functionality import *


# Create your views here.

def APIGetLoginInfo(request):
    if request.method == "GET":
        if checkPrivLevel(request,PRIVILEGE_LEVEL_0):
            return getCurrentUserInfo(request)
    return HttpResponse(status=400)

def APIRegister(request):
    if request.method == "POST":
        return register(request)
    return HttpResponse(status=400)

def APILogin(request):
    if request.method == "POST":
        return login(request)
    return HttpResponse(status=400)

def APILogout(request):
    if checkPrivLevel(request,PRIVILEGE_LEVEL_4):
        return logout(request)
    return HttpResponse(status=400)

def APIForgotPassword(request):
    if request.method == "POST":
        return forgotPassword(request)
    return HttpResponse(status=400)

def APIResetPassword(request):
    if request.method == "POST":
        return ResetPassword(request)
    return HttpResponse(status=400)

def APICreateEvent(request):
    if request.method == "POST":
        if checkPrivLevel(request,PRIVILEGE_LEVEL_0):
            return createEvent(request)
    return HttpResponse(status=400)

def APIEnrollEvent(request,id):#id = the id of the event
   if request.method == "POST":
        if checkPrivLevel(request,PRIVILEGE_LEVEL_0):
            return enrollEvent(id, request)
   return HttpResponse(status=400)

def APIListEvents(request):
    if request.method == "GET":
        return getEventsList()
    return HttpResponse(status=400)

def APIEventInfo(request,id):
    if request.method == "GET":
        return getEventInfo(id)
    return HttpResponse(status=400)

def APIManageEvent(request,id):
   if request.method == "POST":
        if checkPrivLevel(request,PRIVILEGE_LEVEL_0):
            return ManageEvent(id, request)
   return HttpResponse(status=400)

def APIListEnrollmentsOfEvent(request,id):
   if request.method == "GET":
        if checkPrivLevel(request,PRIVILEGE_LEVEL_0):
            return getEnrollmentList(id, request)
   return HttpResponse(status=400)

def APIMakeDecision(request,id):
   if request.method == "POST":
        if checkPrivLevel(request,PRIVILEGE_LEVEL_0):
            return makeEnrollmentDecision(id, request)
   return HttpResponse(status=400)

def APIPostponeEvent(request,id):
   if request.method == "POST":
        if checkPrivLevel(request,PRIVILEGE_LEVEL_0):
            return postponeEvent(id, request)
   return HttpResponse(status=400)

def APICreatePost(request):
   if request.method == "POST":
        if checkPrivLevel(request,PRIVILEGE_LEVEL_0):
            user_id = request.COOKIES['user_id']
            myform = PostsForm(request.POST)
            if myform.is_valid():
                myform_cleaned = myform.cleaned_data
                return JsonResponse(data = {'Status': 0,
                                            'Data': EventManager.createPost(user_id,POST_TYPE.NEWS,
                                                                                 myform_cleaned['title'],
                                                                                 myform_cleaned['content'],
                                                                                 myform_cleaned['tags'])})
            return HttpResponse(status=400)
   return HttpResponse(status=400)

def APIGetPostsList(request):
   if request.method == "GET":
        if myform.is_valid():
            myform_cleaned = myform.cleaned_data
            return JsonResponse(data = {'Status': 0,
                                        'Data': EventManager.getPostsList(POST_TYPE.NEWS)})
        return HttpResponse(status=400)
   return HttpResponse(status=400)

def APIGetPostDetails(request,id):
   if request.method == "GET":
        if myform.is_valid():
            result , data = EventManager.getPostDetails(id)
            if result == ErrorCodes.POSTS.VALID_POST:
                return JsonResponse(data = {'Status': 0,
                                        'Data': data})
            else:
                return HttpResponse(status=404)
        return HttpResponse(status=400)
   return HttpResponse(status=400)

def APIEditPost(request,id):
   if request.method == "POST":
        if checkPrivLevel(request,PRIVILEGE_LEVEL_0):
            user_id = request.COOKIES['user_id']
            myform = PostsForm(request.POST)
            if myform.is_valid():
                myform_cleaned = myform.cleaned_data
                result , data = EventManager.getPostDetails(id)
                if result == ErrorCodes.POSTS.VALID_POST:
                    return JsonResponse(data = {'Status':EventManager.editPost( id,
                                                                                myform_cleaned['title'],
                                                                                myform_cleaned['content'],
                                                                                myform_cleaned['tags'])})
                else:
                    return HttpResponse(status=404)
            return HttpResponse(status=400)
   return HttpResponse(status=400)

def APIDeletePost(request,id):
   if request.method == "POST":
        if checkPrivLevel(request,PRIVILEGE_LEVEL_0):
            user_id = request.COOKIES['user_id']
            myform = PostsForm(request.POST)
            if myform.is_valid():
                myform_cleaned = myform.cleaned_data
                result , data = EventManager.getPostDetails(id)
                if result == ErrorCodes.POSTS.VALID_POST:
                    return JsonResponse(data = {'Status':EventManager.deletePost(id)})
                else:
                    return HttpResponse(status=404)
            return HttpResponse(status=400)
   return HttpResponse(status=400)

