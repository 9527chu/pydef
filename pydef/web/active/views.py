# Create your views here.
from active.forms import *
from active.models import *
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import time


def index(req):
    if req.method=="POST":
        lf = LoginForm(req.POST)
        if lf.is_valid():
            username = lf.cleaned_data['username'] 
            password = lf.cleaned_data['password']
            user = authenticate(username = username,password=password)
            if user is None:
                return redirect('/index/')
            else :
                if req.META.has_key('HTTP_X_FORWARDED_FOR'):
                    ip = req.META['HTTP_X_FORWARDED_FOR']
                else:
                    ip = req.META['REMOTE_ADDR']
                login(req,user) 
                up = UserProfile.objects.get(user=user)
		up.ip=ip
                up.save()
	#	return render(req,'index.html',{'user':req.user,'up':up})       
    else:
        lf = LoginForm()
        if req.user.is_authenticated():
            up = UserProfile.objects.get(user=req.user)
        else:
            up = None
    active = Active.objects.all()
    say = Say.objects.all().order_by('time')
    zidian={'lf':lf,'up':up,'active':active,'say':say}
    return render(req,'index.html',zidian)

def huodong(req):
    if req.user.is_authenticated():
        up = UserProfile.objects.get(user=req.user)
    else:
        up = None
    active = Active.objects.all()
    lf = LoginForm()    
    return render(req,'huodong.html',{'lf':lf,'up':up,'active':active})


def disact(req,id):
    act = Active.objects.get(id=id)
    akwds = Ackwd.objects.filter(active = act)
    lf=LoginForm()
    return render(req,'disact.html',{'act':act,'akwds':akwds,'lf':lf})

def haowan(req):
    lf = LoginForm()
    return render(req,'haowan.html',{'lf':lf})



def meiwei(req):
    lf = LoginForm()
    return render(req,'meiwei.html',{'lf':lf})



    
def gggg(req):
    if req.user.is_authenticated():
        up = UserProfile.objects.get(user=req.user)
        fpnum = up.fpnum()
        print up.fllowp,fpnum
    else :
        up = None
        fpnum = None 
    lf = LoginForm()
    say = Say.objects.all().order_by('time')
    active = Active.objects.all()
    return render(req,'gggg.html',{'fpnum':fpnum,'up':up,'say':say,'active':active,'lf':lf})



def search(req):
    sch = req.POST.get('search','')
    if sch:
        pass
    else:
        return redirect('/index/')

def flwp(req):
    if req.user.is_authenticated():
        flwp_id = req.GET.get('id','')
        id = int(flwp_id)
        flwp = User.objects.get(id = id)
        print type(flwp)
        up = UserProfile.objects.get(user = req.user)
        print up
        up.fllowp.add(flwp)
        up.save()
        return redirect('/index/gggg/')
    else:
        return redirect('/index/')

def flwa(req):
    if req.user.is_authenticated():
        flwa_id = req.GET.get('id','')
        flwa = Active.objects.get(id=flwa_id)
        up = UserProfile.objects.get(user = req.user)
        if flwa in up.fllowa.all():
            up.qxgza(flwa)   
        else:
            up.fllowa.add(flwa)
            up.save()
        return redirect('/index/huodong/')
    else :
        return redirect('/index/')
def joia(req):
    if req.user.is_authenticated():
        joia_id = req.GET.get('id','')
        joia = Active.objects.get(id=joia_id)
        up = UserProfile.objects.get(user = req.user)
        if joia in up.joina.all():
            up.qxjoia(joia)
        else:
            up.joina.add(joia)
            up.save()
        return redirect('/index/huodong/')
    else:
        return redirect('/index/')
def saycmm(req):
    if req.user.is_authenticated():
        id =req.POST.get('id')
        i =int(id) 
        cont = req.POST.get('content','')
        say = Say.objects.get(id = i)
        urls = req.POST.get('url','')
        Saycmm.objects.create(content=cont,user=req.user,say=say)
        return redirect(urls)
    else :
        return redirect('/index/')
def uregist(req):
    if req.method=="POST":
        uf = UserForm(req.POST)
        if uf.is_valid():
            un = uf.cleaned_data['username']
            pa = uf.cleaned_data['password']
            email = uf.cleaned_data['email']
            print un,pa,email
            user = User.objects.create_user(un,email,pa)
            u = UserProfile.objects.create(user=user)
            print u
            return redirect('/index/')
    else:
        lf=LoginForm() 
        uf=UserForm()
        zidian={'uf':uf,'lf':lf}
    return render(req,'register.html',zidian)
    


def home(req):
    if req.user.is_authenticated():
        id = req.GET.get('id','')
        if id:
            user = User.objects.get(id__exact=id)
            says = Say.objects.filter(user = user)
            urls = req.get_full_path()
            print urls
            print req.get_full_path()
        else :
            user = User.objects.get(id = req.user.id)
            up = UserProfile.objects.get(user = user)
            all = up.fllowp.all()
            
            says=[]
            for i in all:
                says.extend(Say.objects.filter(user = i))
            says.extend(Say.objects.filter(user=req.user))
            urls = req.path    
        cmms=[]
        for say in says:
            cmms.extend(Saycmm.objects.filter(say=say))
        usermain = req.user 
        return render(req,'home.html',{'url':urls,'user':user,'says':says,'cmms':cmms,'um':usermain})
    else:
        return redirect('/index/')


def shuoshuo(req):
    if req.user.is_authenticated():
        if req.method == 'POST':
            shuo = req.POST.get('shuo','')
            if shuo:
              #  tm = time.strftime('%Y-%m-%d %X',time.localtime())
                Say.objects.create(content=shuo,user=req.user)
        return redirect('/user/home/')   
                
    else:
        return redirect('/index/')
        
def mysays(req):
    if req.user.is_authenticated():
        user = req.user
        says = Say.objects.filter(user = user)
        cmms=[]
        for say in says:
            cmms.extend(Saycmm.objects.filter(say =say))
        return render(req,'mysays.html',{'user':user,'cmms':cmms,'says':says})   
    else :
        return redirect('/index/')

def myflwp(req):
    return render(req,'myflwp.html',{})




def myact(req):
    
    if req.user.is_authenticated():
        id = req.GET.get('id','')    
        if id:
            user = User.objects.get(id__exact=id)
            acts = Active.objects.filter(user = user)
        else:    
            user = req.user
            acts = Active.objects.filter(user=user)
    else:
        return redirect('/index/')
    um = req.user
        
    return render(req,'myact.html',{'um':um,'user':user,'acts':acts})


def myfriend(req):
    if req.user.is_authenticated():
        user = req.user
        return render(req,'myfriend.html',{'user':user})


    else:
        return redirect('/index/')    





def user_info(req):
    if req.method=='POST':
        pass 
    else:
        if req.user.is_authenticated():
            zidian={'user':req.user,'um':req.user}
            return render(req,'user_info.html',zidian)
        else :
            return redirect('/index/')



def face(req):
    if req.method=="POST":
        hdimg = req.FILES.get('hdimg','')
        print hdimg
        if hdimg:
            user = UserProfile.objects.get(user=req.user)
            user.headimg=hdimg
            user.save()
            pd=2
        else:
            pd=1
        up=UserProfile.objects.get(user__exact=req.user)
        zidian={'pd':pd,'user':req.user,'up':up}
        return render(req,'face.html',zidian)
    else:
        if req.user.is_authenticated():
            pd=0
            up=UserProfile.objects.get(user__exact=req.user)
            zidian={'user':req.user,'pd':pd,'up':up}
            
            return render(req,'face.html',zidian)
        else:
            return redirect('/index/')



def change_passwd(req):
    if req.method=="POST":
        user = User.objects.get(username=req.user.username)
        passwd = req.POST.get('oldpswd','')
        pd1 = req.POST.get('newpswd1','')
        pd2 = req.POST.get('newpswd2','')
        if user.check_password(passwd):
            if pd1 == pd2 and pd1 and pd2:
                user.set_password(pd1)
                user.save()
                pd=3
            else:
                pd=2
        else:
            pd=1
        zidian={'user':user,'pd':pd}
        return render(req,'change_passwd.html',zidian)
    else:
        if req.user.is_authenticated():
            pd=0
            zidian={'user':req.user,'pd':pd}
            return render(req,'change_passwd.html',zidian)
        else:
            return redirect('/index/')

def hold_act(req):
    if req.method=='POST':
        title = req.POST.get('title')
        content = req.POST.get('hdcont')
        picture = req.FILES.get('hdpic')
        print 'picture:',picture
        holdtime = req.POST.get('time')
        city = req.POST.get('ddop')
       # sendtime = time.strftime('%Y-%m-%d %X',time.localtime())
        leibie = req.POST.get('lbop')
        money = req.POST.get('sfop')
        tags = req.POST.get('tag','')
        active = Active.objects.create(title=title,content=content,picture=picture,holdtime = holdtime,city=city,leibie=leibie,money=money,user=req.user)     
        print active
        if tags:
            for i in tags.split('/'):
                Ackwd.objects.create(kword=i,active=active)
        else :
            Ackwd.objects.create(active=active)
        return redirect('/user/home/myact')   
    else:
        if req.user.is_authenticated(): 
               
            zidian={'user':req.user,'um':req.user}
            return render(req,'hold_act.html',zidian)
        else:
            return redirect('/index/')
    
def ulogout(req):
    logout(req)
    return redirect('/index/')
