# -*- encoding: utf-8 -*-
"""
Created on Aug 30 2015

@author: fengyan
last change 10 20 2015
"""
from django.conf.urls import patterns, include, url
from accounts.views import alogout,alogin,register,index
from side.views import *
from talents.views import *
from resume.views import *
from side import views
#网址注册基于整个工程的URL具体网址为http.../side/
#name为重命名
urlpatterns = [
    
    url(r'^stucked/$', 'side.views.stucked', name='stucked'),
    url(r'^myresume/$', 'side.views.myresume', name='myresume'),
    url(r'^mystucked/$', 'side.views.mystucked', name='mystucked'),
    url(r'^worked/$', 'side.views.worked', name='worked'),
    url(r'^worked_search/$', 'side.views.worked_search', name='worked_search'),
    url(r'^seize/$', 'side.views.seize', name='seize'),
    url(r'^exhelp/$', 'side.views.exhelp', name='exhelp'),
    url(r'^processed/$', 'side.views.processed', name='processed'),
    url(r'^interviews/$', 'side.views.interviews', name='interviews'),
    url(r'^newentry/(?P<resume_id>[^/]+)/$', 'side.views.newentry', name='newentry'),
  #  url(r'^recommend/', 'side.views.recommend', name='recommend'),
    url(r'^agency/', 'side.views.agency', name='agency'),
    url(r'^entry/$', 'side.views.entry', name='entry'),
    url(r'^noentryed/$', 'side.views.noentryed', name='noentryed'),
    url(r'^entryed/$', 'side.views.entryed', name='entryed'),
    url(r'^entryrecord/(?P<resume_id>[^/]+)/$', 'side.views.entryrecord', name='entryrecord'),
    url(r'^Interview_resume/(?P<resume_id>[^/]+)/$', 'side.views.Interview_resume', name='Interview_resume'),
    url(r'^newinterview/(?P<resume_id>[^/]+)/$', 'side.views.newinterview', name='newinterview'),
#    url(r'^event/(?P<user_id>[^/]+)/$', 'side.views.event', name='event'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':'/static/'}),
    url(r'^statisticsmon/$', 'side.views.statisticsmon', name='statisticsmon'),
    url(r'^statisticsyea/$', 'side.views.statisticsyea', name='statisticsyea'),
    url(r'^invitation/(?P<interview_id>[^/]+)/$', 'side.views.invitation', name='invitation'),
    url(r'^retreat/(?P<interview_id>[^/]+)/$', 'side.views.retreat', name='retreat'),
    url(r'^recover/(?P<interview_id>[^/]+)/$', 'side.views.recover', name='recover'),
    url(r'^offer/(?P<interview_id>[^/]+)/$', 'side.views.offer', name='offer'),
    url(r'^lookoffer/(?P<interview_id>[^/]+)/$', 'side.views.lookoffer', name='lookoffer'),
    url(r'^exoffer/(?P<interview_id>[^/]+)/$', 'side.views.exoffer', name='exoffer'),
    url(r'^sent_omail/(?P<interview_id>[^/]+)/$', 'side.views.sent_omail', name='sent_omail'),
    url(r'^get_content/', 'side.views.get_content', name='get_content'),
    url(r'^get_emails/', 'side.views.get_emails', name='get_emails'),

]                                                                                                                                                                                
   # url(r'^scheduled/$', 'side.views.scheduled', name='scheduled'),
   # url(r'^delayed/$', 'side.views.delayed', name='delayed'),
