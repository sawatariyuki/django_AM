from django.contrib import admin

# Register your models here.
from .models import *

class UserDefaultInfo(admin.ModelAdmin):
	list_display = ('name', 'pw', 'email', 'isActivated', 'activateCode')
admin.site.register(UserDefault, UserDefaultInfo)