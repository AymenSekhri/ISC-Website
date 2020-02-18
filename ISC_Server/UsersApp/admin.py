from django.contrib import admin
from .models import UsersDB, SessionsDB, PassResetDB, EventEnrolment, Event
# Register your models here.
admin.site.register(UsersDB)
admin.site.register(SessionsDB)
admin.site.register(PassResetDB)
admin.site.register(Event)
admin.site.register(EventEnrolment)
