"""aya URL Configuration

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
from manager.views import add_customer,customer_manage,add_pro,project_manage, update_pro,add_department,add_rule,rule_power_manage,department_manage,add_role,role_manage,add_power,power_manage,user_role_manage,add_user_role,user_power_manage,add_user_power,add_email,user_manage,update,update_user_role,update_user_power,delete_user_role,delete_user_power,change_mail_pwd,delete_user,delete_role,delete_rule,delete_depart,update_depart,update_rule,update_role,add_user_rule,user_rule_manage,delete_user_rule,update_user_rule
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^add_department/',add_department,name = "add_department"),
    url(r'^department_manage/', department_manage, name = "department_manage"),
    url(r'^add_role/', add_role, name = "add_role"),
    url(r'^role_manage/', role_manage, name = "role_manage"),
    url(r'^project_manage/', project_manage, name = "project_manage"),
    url(r'^customer_manage/', customer_manage, name = "customer_manage"),
    url(r'^add_power/', add_power, name = "add_power"),
    url(r'^add_pro/', add_pro, name = "add_pro"),
    url(r'^add_customer/', add_customer, name = "add_customer"),
    url(r'^add_user_rule/', add_user_rule, name = "add_user_rule"),
    url(r'^power_manage/',power_manage , name = "power_manage"),
    url(r'^user_role_manage/(?P<user_id>[^/]+)/$', user_role_manage, name = "user_role_manage"),
    url(r'^user_rule_manage/(?P<user_id>[^/]+)/$', user_rule_manage, name = "user_rule_manage"),
    url(r'^add_user_role/', add_user_role, name = "add_user_role"),
    url(r'^add_user_power/', add_user_power, name = "add_user_power"),
    url(r'^user_power_manage/(?P<user_id>[^/]+)/$', user_power_manage, name = "user_power_manage"),
    url(r'^add_email/', add_email, name = "add_email"),
    url(r'^user_manage/',user_manage, name="user_manage"),
    url(r'^updates/(?P<user_id>[^/]+)/$',update,name="updates"),
    url(r'^update_user_role/(?P<corrole_id>[^/]+)/$',update_user_role,name="update_user_role"),
    url(r'^update_pro/(?P<pro_id>[^/]+)/$',update_pro,name="update_pro"),
    url(r'^update_user_power/(?P<corpower_id>[^/]+)/$',update_user_power,name="update_user_power"),
    url(r'^delete_user_role/(?P<corrole_id>[^/]+)/$',delete_user_role,name="delete_user_role"),
    url(r'^delete_user_rule/(?P<user_rule_id>[^/]+)/$',delete_user_rule,name="delete_user_rule"),
    url(r'^update_user_rule/(?P<user_rule_id>[^/]+)/$',update_user_rule,name="update_user_rule"),
    url(r'^delete_user_power/(?P<corpower_id>[^/]+)/$',delete_user_power,name="delete_user_power"),
    url(r'^change_mail_pwd/',change_mail_pwd,name="change_mail_pwd"),
    url(r'^add_rule/',add_rule,name="add_rule"),
    url(r'^rule_power_manage/',rule_power_manage,name="rule_power_manage"),
    url(r'^delete_user/(?P<user_id>[^/]+)/$',delete_user,name="delete_user"),
    url(r'^delete_rule/(?P<rule_id>[^/]+)/$',delete_rule,name="delete_rule"),
    url(r'^delete_depart/(?P<depart_id>[^/]+)/$',delete_depart,name="delete_depart"),
    url(r'^delete_role/(?P<role_id>[^/]+)/$',delete_role,name="delete_role"),
    url(r'^update_role/(?P<role_id>[^/]+)/$',update_role,name="update_role"),
    url(r'^update_rule/(?P<rule_id>[^/]+)/$',update_rule,name="update_rule"),
    url(r'^update_depart/(?P<depart_id>[^/]+)/$',update_depart,name="update_depart"),
    #url(r'^delete_/(?P<user_id>[^/]+)/$',delete_user,name="delete_user"),
]
