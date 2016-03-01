"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from mysite.views import *
from fakecube.views import *
from PayAutoTest.views import *
from webpagetest.views import *
from smokeTest.views import *
from django.conf.urls import *
from models import *
from paytools.views import clearwallet,clearrealname,paytools,clearsecstore
from alertStrategy.views import *
from paytools.views import clearwallet,clearrealname,paytools,clearsecstore,diffile
from naccounttools.views import *
#admin.autodiscover()

#urlpatterns = [
#    url(r'^admin/', include(admin.site.urls)),
#]

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	('^hello/$', hello),
	('^time/$', cur_time),
    ('queryReport/$',queryReport),
    (r'queryGraph$',queryGraph),
    ('queryGraphStatus$',queryGraphStatus),
    ('queryReportStatus$',queryReportStatus),
    ('graphDataDiff$',graphDataDiff),
    ('reportPicDiff$',reportPicDiff),
    ('getPicRe$',getPicCom),
    (r'^fakecube', helloworld),
    ('queryFakecube/$',queryFakecube),
    ('queryFakecubeIFStatus$',queryFakecubeIFStatus),
    ('runfJob$',runfJob),
    (r'index$',index),
    (r'tuangou$',tuangou),
    (r'^tuangou_gz$',tuangou_gz),
    ('payautotest$',payautotest),
    ('runpaytest$',runpaytest),
    (r'^payresult/$',payresult), 
    (r'^replaceStand$',replaceStand),
    (r'^showresult/$',showresult),
    (r'^smokeTest$',smokeTest),
    (r'^runSmokeTest$',runSmokeTest),
    (r'^querySmokeStatus$',querySmokeStatus),
    (r'^paytools/',paytools),
    (r'^clearwallet/',clearwallet),
    (r'^clearrealname/',clearrealname),
    (r'^clearsecstore/',clearsecstore),
    (r'^runAllMonitor$',runAllMonitor),
    (r'^getAlertReport$',getAlertReport),
    (r'^diffile/',diffile),
    (r'^groupon_poster_gz$',groupon_poster_gz),
    (r'^loadData$',loadData),
    (r'^sendMailService$',sendMailService),
    (r'^runsame/(.+)/$',runsame),
    (r'^rundiff$',rundiff),
    (r'^updateComments$',updateComments),
    (r'^queryAlert$',queryAlert),
    (r'^naccounttools/$',naccounttools),
    (r'^fenbiao/$',fenbiao),
    (r'^newrunsame/$', newrunsame),
    (r'^getMonitorCurlCmd/$', getMonitorCurlCmd),
    (r'^checkAccount/$',checkAccount),
)
