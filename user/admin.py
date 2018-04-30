from django.contrib import admin

# Register your models here.
from .models import *

class UserDefaultInfo(admin.ModelAdmin):
	list_display = ('name', 'pw', 'email', 'isActivated', 'activateCode', 'date_joined', 'last_joined', 'isDeleted')
admin.site.register(UserDefault, UserDefaultInfo)

class UserDetailInfo(admin.ModelAdmin):
	list_display = ('userDefault', 'gender', 'weight', 'birthday', 'age', 'birthplace', 'liveplace')
admin.site.register(UserDetail, UserDetailInfo)

class EventTypeInfo(admin.ModelAdmin):
	list_display = ('userDefault', 'name', 'description', 'useTimes', 'emergencyLevel', 'ctime', 'last_used')
admin.site.register(EventType, EventTypeInfo)

class EventInfo(admin.ModelAdmin):
	list_display = ('userDefault', 'title', 'description', 'eventType', 'ctime', 'userLevel', 'userStartTime', 'userEndTime', 'length', 'sysStartTime', 'sysEndTime', 'sysLevel', 'state')
admin.site.register(Event, EventInfo)

class OperationLogInfo(admin.ModelAdmin):
	list_display = ('userDefault', 'content', 'ip', 'ctime', 'location')
admin.site.register(OperationLog, OperationLogInfo)


