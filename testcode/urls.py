# Shawn Jain
# 1/19/2013
# Testcode project
# urls.py

# Define URL schema, map URLs to functions in views.py

# imports
from django.conf.urls import patterns, include, url
from testcode import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testcode.views.home', name='home'),
    # url(r'^testcode/', include('testcode.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # Login page
    url(r'^$', views.landing),

    # Student Homepage 
    url(r'^student/$', views.student),
    # Teacher Homepage
    url(r'^teacher/$', views.teacher),

    # Editing interface. Grab url
    #url(r'^edit/(\d{1,5})/$', views.edit)

    # API urls to interact with backend
    url(r'^api/login$', views.login),
    url(r'^api/logout$', views.logout),
    url(r'^api/signup$', views.signup),    #url(r'^api/submit$', views.submitsolution),
    url(r'^api/createcourse$', views.createcourse),
    url(r'^api/createlecture$', views.createlecture),
    url(r'^api/addcourse$', views.addcourse),
    url(r'^api/getlectures$', views.getlectures),
    url(r'^api/createproblem$', views.createproblem),
    url(r'^api/createtestcase$', views.createtestcase),
    url(r'^api/getproblemteacher$', views.getproblemteacher),
    url(r'^api/getsubmission$', views.submissionHistory),
    url(r'^api/getproblem$', views.getproblem),
    url(r'^api/userhome$', views.home),
    url(r'^api/viewperformance$', views.viewperformance),
    url(r'^teacher/edit/(\d{1,5})/$', views.teacherlecture),
    url(r'^student/edit/(\d{1,5})/$', views.edit),
    url(r'^teacher/edit/performance/(\d{1,5})/$', views.studentperformance),
    url(r'^api/getsubmissionteacher$', views.getSubmission),
    url(r'^api/submit$', views.saveandrun),
    url(r'^api/account$', views.account),
    url(r'^api/getlecturesstudent$', views.getlecturestudent),
)
