from django.contrib import admin
from .models import UsersDB, SessionsDB
# Register your models here.
admin.site.register(UsersDB)
admin.site.register(SessionsDB)