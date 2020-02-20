from .models import *
from .PasswordManager import PasswordManager
from .ErrorCodes import ErrorCodes
import random
import string
from datetime import datetime, timedelta  
from django.utils import timezone

class PostManager(object):

    def createPost(userID,postType,title,content,tags):
        post = Posts.objects.create(title = title,
                                     type = postType,
                                     user_id = userID,
                                     tags = tags,
                                     content = content)
        return post.id
    
    def getPostsList(postType):
        posts = []
        for x in Posts.objects.filter(type = postType):
            postInfo = {'id':x.id,
                         'title':x.title,
                         'user':x.user_id,
                         'tags': x.tags,
                         'date': x.posting_date}
            posts.append(postInfo)
        return posts

    def getPostDetails(id):
        query = Posts.objects.filter(id = id)
        if query.exists():
            x = query.first()
            postInfo = {'id':x.id,
                        'title':x.title,
                        'type':x.type,
                        'user':x.user_id,
                        'tags': x.tags,
                        'date': x.posting_date,
                        'content': x.content}
            return ErrorCodes.POSTS.VALID_POST, postInfo
        else:
            return ErrorCodes.POSTS.INVALID_POST, {}

    def editPost(postID,title,content,tags):
        post = Posts.objects.filter(id = postID).first()
        print(postID)
        post.title = title
        post.content = content
        post.tags = tags
        post.save()
        return ErrorCodes.POSTS.VALID_POST

    def deletePost(postID):
        post = Posts.objects.filter(id = postID)
        post.delete()
        return ErrorCodes.POSTS.VALID_POST