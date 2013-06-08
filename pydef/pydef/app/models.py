#!-*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Module(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name


class Funct(models.Model):
    name = models.CharField(max_length=20)
    format = models.CharField(max_length=50)
    intro = models.TextField()
    inputs = models.CharField(max_length=50)
    outputs = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    module = models.ForeignKey(Module)
    like = models.ManyToManyField(User,related_name='like',blank=True,null=True)
    def __unicode__(self):
        return self.name
    def fans(self):
        return self.like.count()

    

class QusOfFun(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    funct = models.ForeignKey(Funct)


class AnsOfFun(models.Model):
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    quset = models.ForeignKey(QusOfFun) 



class QusOfUsr(models.Model):
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    

class AnsOfUsr(models.Model):
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    quest = models.ForeignKey(QusOfUsr)

class Uid(models.Model):
    uid = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)

