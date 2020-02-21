from .models import *
from .ErrorCodes import ErrorCodes
import random
import string
from datetime import datetime, timedelta  
from django.utils import timezone

class TeamManager(object):


    def checkTeamMember(id):
        if TeamMembers.objects.filter(id = id).exists():
            return ErrorCodes.TEAMUSERS.VALID_USER
        return ErrorCodes.TEAMUSERS.INVALID_USER

    def checkMemberUserID(userID):
        if TeamMembers.objects.filter(user_id = userID).exists():
            return ErrorCodes.TEAMUSERS.VALID_USER
        return ErrorCodes.TEAMUSERS.INVALID_USER

    def AddMember(userID,title,bio,contacts):
        Member = TeamMembers.objects.create(user_id = userID,
                                            title = title,
                                            bio = bio,
                                            contacts = contacts)
        return Member.id
    def getTeamList():
        members = []
        for x in TeamMembers.objects.all():
            memberInfo = {'id':x.id,
                          'userID':x.user_id,
                          'firstName':x.user.firstName,
                          'lastName': x.user.familyName,
                          'title': x.title,
                          'bio': x.bio,
                          'contacts': x.contacts,
                          'date': str(x.date)}
            members.append(memberInfo)
        return members

    def editMember(id,title,bio,contacts):
        member = TeamMembers.objects.filter(id = id).first()
        member.title = title
        member.bio = bio
        member.contacts = contacts
        member.save()
        return ErrorCodes.TEAMUSERS.VALID_USER

    def deleteMember(id):
        member = TeamMembers.objects.filter(id = id).first()
        member.delete()
        return ErrorCodes.TEAMUSERS.VALID_USER