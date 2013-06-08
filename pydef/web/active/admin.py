from django.contrib import admin
from active.models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(UserProfile,UserProfileAdmin)

class ActiveAdmin(admin.ModelAdmin):
    list_display = ('title',)
admin.site.register(Active,ActiveAdmin)

class SayAdmin(admin.ModelAdmin):
    list_display = ('user',)
admin.site.register(Say,SayAdmin)



