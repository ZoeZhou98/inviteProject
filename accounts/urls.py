from django.conf.urls import patterns, include, url
from accounts.views import alogout,alogin,register,changepwd,change_account,forget_password,mail_password,forget_changepwd,test

urlpatterns = [
    url(r'^login/$', alogin, name='alogin'),
    url(r'^register/$', register, name='register'),
    url(r'^logout/$', alogout, name='alogout'),
    url(r'^changepwd/$',changepwd,name='changepwd'),
	url(r'^change_account/$',change_account,name='change_account'),
	url(r'^forget_password/$',forget_password,name='forget_password'),
	url(r'^forget_changepwd',forget_changepwd,name='forget_changepwd'),
	url(r'^mail_password/$',mail_password,name='mail_password'),
    url(r'^test/$',test,name='test'),
]                                                                                                                                                                                
