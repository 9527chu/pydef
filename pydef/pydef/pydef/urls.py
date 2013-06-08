from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from app.views import *



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pydef.views.home', name='home'),
    # url(r'^pydef/', include('pydef.foo.urls')),
    url(r'^statics/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index1/$',index1),
    url(r'^index2$',index2),
    url(r'^index/$',index),
    url(r'^addfunct/func_add/$',func_add),
    url(r'^addfunct/show_func/$',show_func),
    url(r'^addfunct/show_funcall/$',show_funcall),

    url(r'^ascans/$',ascans),
    url(r'^ascans/sarqus/$',sarqus),


    url(r'^search/$',search),
    url(r'^search/name/$',sername),
    url(r'^search/suoyin/$',suoyin),
    url(r'^search/category/$',category),
    url(r'^search/disp/$',disp),
    url(r'^search/detail/$',detail),
    url(r'^search/qusoffun/$',qusoffun),
    url(r'^search/qusoffun/ansave/$',ansave),
    url(r'^search/like/$',like),

    url(r'^logout/$',ulogout),

)
