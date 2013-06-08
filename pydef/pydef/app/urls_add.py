from django.conf.urls import patterns, include, url

urlpatterns = patterns('app.views_add',
    url(r'fun_add/$','func_add'),
    url(r'show_func1/(\d+)/$','show_func'),
    url(r'show_funcall/$','show_funcall'),
)
