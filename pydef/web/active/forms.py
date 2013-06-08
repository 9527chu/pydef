#-*-coding:utf-8-*-
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label=u'昵称')
    email = forms.CharField(label=u'邮箱')
    password = forms.CharField(label=u'密码',widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField(label='邮箱')
    password = forms.CharField(label='密码',widget=forms.PasswordInput)
 
