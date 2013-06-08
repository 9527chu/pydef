from django.contrib import admin
from app.models import *


class ModuleAdmin(admin.ModelAdmin):
    list_display=('name',)


admin.site.register(Module,ModuleAdmin)



class FunctAdmin(admin.ModelAdmin):
    list_display=('name',)



admin.site.register(Funct,FunctAdmin)

class QusOfFunAdmin(admin.ModelAdmin):
    list_display=('content','funct','user')


admin.site.register(QusOfFun,QusOfFunAdmin)


class AnsOfFunAdmin(admin.ModelAdmin):
    list_display=('content','user')


admin.site.register(AnsOfFun,AnsOfFunAdmin)



class QusOfUsrAdmin(admin.ModelAdmin):
    list_display=('content','user')

admin.site.register(QusOfUsr,QusOfUsrAdmin)




class AnsOfUsrAdmin(admin.ModelAdmin):
    list_display=('content','user')


admin.site.register(AnsOfUsr,AnsOfUsrAdmin)

