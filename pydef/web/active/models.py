#!-*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    headimg = models.FileField(upload_to='./headimg/',blank=True,null=True)
    sex = models.CharField(max_length=1,choices=(('m','man'),('w','woman'),),blank=True)
    user = models.ForeignKey(User,unique=True)
    birthday = models.DateField(blank=True, null=True)
    ip = models.CharField(max_length=20,blank=True)
    fllowp = models.ManyToManyField(User,verbose_name=u'关注',blank=True,related_name='fp')
    fllowa = models.ManyToManyField('Active',blank=True)
    joina = models.ManyToManyField('Active',blank=True,related_name="ja")    
    def fpnum(self):
        return self.fllowp.count()
    def fanum(self):
        return self.fllowa.count()
    def janum(self):
        return self.joina.count()
    def qxgzp(self,user):
        self.fllowp.remove(user)
	return True
    def qxgza(self,active):
        self.fllowa.remove(active)
        return True
    def qxjoia(self,active):
        self.joina.remove(active)
    def fans(self):
        fans = 0
        all = UserProfile.objects.all()
        for i in all:
            if self.user in i.fllowp.all():
                fans+=1
        return fans    

class Active(models.Model):    
    title = models.CharField(max_length=30)
    content = models.TextField()
    picture = models.FileField(upload_to='./picture/')
    leibie = models.CharField(max_length=10,choices=(('a',u'旅游'),('b',u'运动'),('c',u'学习'),('d',u'游戏'),('e',u'聚餐'),('f',u'k歌'),('g',u'棋牌')))
    city = models.CharField(max_length=10)
    holdtime = models.DateField()
    time = models.DateTimeField(auto_now_add=True)
    money = models.CharField(max_length=10)
    user = models.ForeignKey(User)
    

class Ackwd(models.Model):
    kword = models.CharField(max_length=30,blank=True,null=True)
    active = models.ForeignKey(Active)

class Urkwd(models.Model):
    kword = models.CharField(max_length=30,blank=True,null=True)
    user = models.ForeignKey(User)



class Actcmm(models.Model):
    content = models.TextField(u'内容')
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    active = models.ForeignKey(Active)


class Say(models.Model):
    content = models.TextField(u'内容')
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

class Saycmm(models.Model):
    content = models.TextField(u'内容')
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    say =  models.ForeignKey(Say)
   



    


     





