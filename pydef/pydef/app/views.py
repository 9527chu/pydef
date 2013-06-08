#!-*-coding:utf8-*-
# Create your views here.
from django import forms
from django.contrib.sessions.models import Session
from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse 
from app.models import *
from app.pydeforms import QusForm,SeForm
from weibo import APIClient
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


APP_KEY = '858209012'
APP_SECRET = '9dae456aff47263586f4cb0a5d56bb4e'
CALLBACK_URL = 'http://www.pydef.com/index2'
client = APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK_URL)
def index1(req):
    url=client.get_authorize_url()
    return render(req,'index1.html',locals())


def index2(req):
    code = req.GET.get('code')
    r = client.request_access_token(code)
    access_token = r.access_token
    req.session['a']=access_token
    espires_in = r.expires_in
    req.session['e']=espires_in
    client.set_access_token(access_token,espires_in)
    uid = client.account.get_uid.get()
    id = uid['uid']
    j = Uid.objects.filter(uid = id)
    if j:
        pass
    else:
        Uid.objects.create(uid = id)
    return redirect('/index/')

def index(req):
    client.set_access_token(req.session['a'],req.session['e'])
    uid = client.account.get_uid.get()
    id = uid['uid']
    req.session['id']=id
    id_list = Uid.objects.all().order_by('-time')
    imgs = []
    for i in id_list:
        ue = client.users.show.get(uid = i.uid)
        imgs.append(ue['profile_image_url']) 
    ur =  client.users.show.get(uid = id )
    name = ur['name']
   # email = client.account.profile.email.get()
    eml = str(id)+"@qq.com"
    headimg = ur['avatar_large']
    req.session['headimg']=headimg
    user = authenticate(username=name,password=id)
    if user is None:
        user = User.objects.create_user(name,eml,id)
    login(req,user)
    return render(req,'index.html',locals())





def ascans(req):
    if req.user.is_authenticated():
        client.set_access_token(req.session['a'],req.session['e'])
        ur =  client.users.show.get(uid = req.session.get('id') )
        headimg = ur['avatar_large']
        name = ur['name']
        qus = QusOfUsr.objects.order_by('-id')
        paginator = Paginator(qus, 5) # Show 25 contacts per page
        q_list    = range(1,paginator.num_pages+1)
        page = req.GET.get('page')
        try:
            qus = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            qus = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            qus = paginator.page(paginator.num_pages)


        if req.method == 'POST':
            qf = QusForm(req.POST)
            sf = SeForm()
            if qf.is_valid():
                content = qf.cleaned_data['content']
                user = req.user
                QusOfUsr.objects.create(user=user,content=content)
                return redirect('/addfunct/show_funcall/')
        else:
            qf = QusForm()
            sf = SeForm()
        p = req.GET.get('p','')
        

 
        return render(req,'ascans.html',locals())
    else:
        return render(req,'index1.html',{})

def sarqus(req):
    if req.user.is_authenticated():
        qf = QusForm()
        if req.method=="post":
            sf = SeForm(req.POST)
            if sf.is_valid():
                content = sf.cleaned_data['content']
                qus = QusOfUsr.objects.filter(content__iexact=content)   
        else:
            p = req.GET.get('')
            sf = SeForm()           
        return render(req,'ascans.html',locals())



          

def search(req):
    if req.user.is_authenticated():
        client.set_access_token(req.session['a'],req.session['e'])
        ur =  client.users.show.get(uid = req.session.get('id') )
        headimg = ur['avatar_large']
        modules = Module.objects.all()
        fun_list = Funct.objects.all().order_by('-time')
        paginator = Paginator(fun_list, 7) # Show 25 contacts per page
        f_list = range(1,paginator.num_pages+1)
        
        page = req.GET.get('page')
        try:
            functs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            functs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            functs = paginator.page(paginator.num_pages)

        return render(req,'search.html',locals())
    else:
        return render(req,'index1.html',{})

def sername(req):
    if req.user.is_authenticated():
        client.set_access_token(req.session['a'],req.session['e'])
        ur =  client.users.show.get(uid = req.session.get('id') )
        headimg = ur['avatar_large']
        if req.method == "POST":
            modules = Module.objects.all()
            name = req.POST.get('funname','')
            if name:
               juge = 0
               functs = Funct.objects.filter(name__startswith=name)

            else:
               juge = 1 
            return render(req,'result.html',locals())
        else :     
            return redirect('/search/')
    else:
        return render(req,'index1.html',{})

def suoyin(req):
    if req.user.is_authenticated():
        client.set_access_token(req.session['a'],req.session['e'])
        ur =  client.users.show.get(uid = req.session.get('id') )
        headimg = ur['avatar_large']
        abc = ['_','a','b','c','d','e','f','g','h','i','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        idx = req.GET.get('index','')
        modules = Module.objects.all()
        if idx:
            if idx == 'all':
                functs = Funct.objects.all().order_by('name')
                paginator = Paginator(functs, 5) # Show 25 contacts per page
                f_list = range(1,paginator.num_pages+1)
                page = req.GET.get('page')
                try:
                    functs = paginator.page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    functs = paginator.page(1)
                except EmptyPage:
                     # If page is out of range (e.g. 9999), deliver last page of results.
                    functs = paginator.page(paginator.num_pages)

  
            elif idx in abc:
               functs = Funct.objects.filter(name__startswith=idx).order_by('name')
               paginator = Paginator(functs, 5) # Show 25 contacts per pag
               f_list = range(1,paginator.num_pages+1)
               page = req.GET.get('page')
               try:
                   functs = paginator.page(page)
               except PageNotAnInteger:
                   # If page is not an integer, deliver first page.
                   functs = paginator.page(1)
               except EmptyPage:
                   # If page is out of range (e.g. 9999), deliver last page of results.
                   functs = paginator.page(paginator.num_pages)
 

 
            else:
                return redirect('/search/')
             
                    
        juge = 2
        rp = req.path
        return render(req,'result.html',locals())


def category(req):
    if req.user.is_authenticated():
            client.set_access_token(req.session['a'],req.session['e'])
            ur =  client.users.show.get(uid = req.session.get('id') )
            headimg = ur['avatar_large']

            idx = req.GET.get(u'index','')
            modules = Module.objects.all()
	    module = Module.objects.get(name = idx)
            functs = Funct.objects.filter(module = module).order_by('name')
            print 'fun:',functs
            paginator = Paginator(functs, 5) # Show 25 contacts per page
            f_list = range(1,paginator.num_pages+1)
            rp = req.path  
            page = req.GET.get('page',1)
            try:
                functs = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                functs = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                functs = paginator.page(paginator.num_pages)

            juge = 3
            return render(req,'result.html',locals())
    else:        
        return redirect('/index1/')

def disp(req):
    if req.user.is_authenticated():
        client.set_access_token(req.session['a'],req.session['e'])
        ur =  client.users.show.get(uid = req.session.get('id') )
        headimg = ur['avatar_large']
        print 1,headimg
        modules = Module.objects.all()
        id = req.GET.get('id','')
        funct = Funct.objects.get(id = id)
        juge = 4
        rp = req.path
        quses = QusOfFun.objects.filter(funct = funct).order_by('-time')[0:3]
        print quses
        return render(req,'result.html',locals())

def detail(req):
    if req.user.is_authenticated():
        client.set_access_token(req.session['a'],req.session['e'])
        headimg = req.session.get('headimg')
        print headimg
        id = req.GET.get('id') 
        funct = Funct.objects.get(id = id)
        if req.method=='POST':
            cont = req.POST.get('cont','')
            name = req.POST.get('name','')
            if cont:
                user = req.user
                q = QusOfFun.objects.create(content = cont,user=user,funct = funct)    
                weibo = cont +name+" "+"http://www.pydef.com/search/qusoffun/?q_id=%s"%q.id 
                client.statuses.update.post(status=weibo)
            else:
                return redirect('/search/detail/?id=%s'%id)
        quses = QusOfFun.objects.filter(funct = funct)
        paginator = Paginator(quses,3) # Show 25 contacts per page
        q_list = range(1,paginator.num_pages+1)
        page = req.GET.get('page')
        try:
            qs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            qs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            qs = paginator.page(paginator.num_pages)   
    rp=req.path
    return render(req,'detail.html',locals())

def qusoffun(req):
    if req.user.is_authenticated():
        client.set_access_token(req.session['a'],req.session['e'])
        headimg = req.session.get('headimg')
        id = req.GET.get('q_id','')
        if id: 
            quse = QusOfFun.objects.get(id = id)
            ans = AnsOfFun.objects.filter(quset = quse)
            paginator = Paginator(ans, 5) # Show 25 contacts per page
            a_list = range(1,paginator.num_pages+1)
            page = req.GET.get('page')
            try:
                ans = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                ans = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                ans = paginator.page(paginator.num_pages)
        rp = req.path
        return render(req,'qusoffun.html',locals())

def ansave(req):
    if req.user.is_authenticated():
        headimg = req.session.get('headimg')
        id = req.GET.get('q_id','')
        if id:
            quse = QusOfFun.objects.get(id=id)
            if req.method == 'POST':
                comm = req.POST.get('comm','')
                if comm:
                    usr = req.user
                    AnsOfFun.objects.create(user=usr,content=comm,quset=quse)
        print usr
        return redirect('/search/qusoffun/?q_id=%s'%id)
             
def like(req):
    if req.user.is_authenticated():
        user = req.user
        if req.method == 'POST':
           id  =  req.POST.get('lk') 
           rp = req.POST.get('rp')
           func = Funct.objects.get(id=id)
           if user not in func.like.all():
               func.like.add(user)
               func.save()
               ts=''
           else:
               ts =1
               print ts
        return redirect('%s'%rp)
    else:
        return redirect('/index1/')






class AddForm(forms.Form):
    name = forms.CharField(label=u'函数名')
    format = forms.CharField(label=u'语法格式')
    intro  = forms.CharField(label=u'介绍',widget=forms.Textarea)
    input  = forms.CharField(label=u'输入')
    output  = forms.CharField(label=u'输出')
     # module  = forms.CharField(label=u'模块')
def func_add(request):
    if request.user.is_authenticated():
        headimg = request.session.get('headimg')
        request.session.get('k')
        ur = client.users.show.get(uid = request.session.get('id'))
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
                module = request.POST['module']
                 # module = Module.objects.create(name=module)
                module = Module.objects.get(name=module)
                funct = Funct.objects.create(name=name,format=format,intro=intro,inputs=input,outputs=output,module=module,user=request.user,)
  
                  #return HttpResponse('ok')
                return redirect('/addfunct/show_funcall/')
            else:
                return redirect('/addfunct/func_add/')    
        else:
            af = AddForm()
            modules = Module.objects.all()
            functs = Funct.objects.order_by('-id')
            paginator = Paginator(functs, 5) # Show 25 contacts per page
            f_list    = range(1,paginator.num_pages+1)
            page = request.GET.get('page')
            try:
                functs = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                functs = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                functs = paginator.page(paginator.num_pages)


        return render_to_response('func_add.html',locals())
  
def show_func(request,fid):
    if request.user.is_authenticated():
        reqest.session.get('k')
        headimg = request.session.get('headimg')        
        fun_list = Funct.objects.order_by('-id')[0:2]
        func = Funct.objects.get(id=fid)
        fid = int(fid)
        fid_num = len(fun_list)+1
        fid_add=fid+1
        fid_min=fid-1
        return render_to_response('show_func1.html',locals())


def show_funcall(request):
    if request.user.is_authenticated():
        headimg = request.session.get('headimg')
        fun_list = Funct.objects.filter(user=request.user).order_by('-id')
        paginator = Paginator(fun_list, 2) # Show 25 contacts per page
        f_list = range(1,paginator.num_pages+1)
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




def addfriend(req):
    req.session.get('k')
    client.friendships.create.post()
    pass



def ulogout(req):
    if req.user.is_authenticated():
        req.session.get('k')
        client.account.end_session.get()
        logout(req)
    return redirect('/index1/')


 
