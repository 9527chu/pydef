#!-*-coding:utf-8-*-
from django import forms
from django.core.exceptions import ValidationError

class QusForm(forms.Form):
    content = forms.CharField(label='说出你的疑问：', widget=forms.Textarea)

class SeForm(forms.Form):
    content = forms.CharField(label='搜索你的疑问：')
