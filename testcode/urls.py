# Shawn Jain
# 1/19/2013
# Testcode project
# urls.py

# Define URL schema, map URLs to functions in views.py

# imports
from django.conf.urls import patterns, include, url
from testcode import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testcode.views.home', name='home'),
    # url(r'^testcode/', include('testcode.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    # Login page
    url(r'^$', views.home),

    # Student Homepage 
    url(r'^student/$', views.student),
    # Teacher Homepage
    url(r'^teacher/$', views.teacher),

    # API urls to interact with backend
    url(r'^api/login/$', views.login),
    url(r'^api/logout/$', views.logout),
    url(r'^api/signup/$', views.signup),
    url(r'^api/submit/$', views.submit),
)
