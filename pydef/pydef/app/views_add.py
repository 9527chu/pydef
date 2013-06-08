#coding:utf8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from app.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from weibo import APIClient
APP_KEY = '858209012'
APP_SECRET = '9dae456aff47263586f4cb0a5d56bb4e'
CALLBACK_URL = 'http://www.a.com/index2'
client = APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK_URL)



class AddForm(forms.Form):
     name = forms.CharField(label=u'函数名')
     format = forms.CharField(label=u'语法格式')
     intro  = forms.CharField(label=u'介绍',widget=forms.Textarea)
     input  = forms.CharField(label=u'输入')
     output  = forms.CharField(label=u'输入')
    # module  = forms.CharField(label=u'模块')
def func_add(request):
    if request.user.is_authenticated():
        request.session.get('k')
        ur = client.users.show.get(uid = request.user.username)
        headimg = ur['avatar_large'] 
        name = ur['name']   
        fid = request.GET.get('id','')
        if request.method == "POST":
            af = AddForm(request.POST)
            if af.is_valid():
                name = af.cleaned_data['name']
                format = af.cleaned_data['format']
                intro = af.cleaned_data['intro']
                input = af.cleaned_data['input']
                output = af.cleaned_data['output']
               # module = af.cleaned_data['module']
               # user = af.cleaned_data['user']
                user = User.objects.get(username='root')
                module = request.POST['module']
               # module = Module.objects.create(name=module)
                module = Module.objects.get(name=module)
                funct = Funct.objects.create(name=name,format=format,intro=intro,inputs=input,outputs=output,module=module,user=user,)
                
                #return HttpResponse('ok')
                return HttpResponseRedirect('/app/show_funcall/')
        else:
            af = AddForm()
            modules = Module.objects.all()
        functs = Funct.objects.order_by('-id')[0:5]
        return render_to_response('func_add.html',locals())

def show_func(request,fid):
    fun_list = Funct.objects.order_by('-id')[0:5]    
    func = Funct.objects.get(id=fid)
    fid = int(fid)
    fid_num = len(fun_list)+1
    fid_add=fid+1
    fid_min=fid-1
    return render_to_response('show_func1.html',locals())
    

def show_funcall(request):
    fun_list = Funct.objects.order_by('-id')
    paginator = Paginator(fun_list, 4) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        functs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        functs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        functs = paginator.page(paginator.num_pages)


    return render_to_response('show_funcall.html',locals())
