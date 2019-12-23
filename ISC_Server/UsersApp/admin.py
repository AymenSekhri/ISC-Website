from django.contrib import admin
from .models import UsersDB, SessionsDB, PassResetDB
# Register your models here.
admin.site.register(UsersDB)
admin.site.register(SessionsDB)
admin.site.register(PassResetDB)