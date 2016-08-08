# -*- encoding: utf-8 -*-

import os, sys
from django import forms  
from django.db import models  
from accounts.models import *
from side.models import *
from resume.models import *
from talents.models import *
import string

reload(sys)
sys.setdefaultencoding('utf8')
#offer信息表单数据定义
class Mail_OfferForm(forms.ModelForm):  
    Ename = forms.CharField(required=False,label=u"姓名")
    Ephone = forms.CharField(required=False,label=u"电话")
    Email = forms.CharField(required=False,label=u"邮箱")
    Eentrytime = forms.CharField(required=False,label=u"办理入职时间")
    Epost = forms.CharField(required=False,label=u"入职岗位")
    Epostgrade = forms.CharField(required=False,label=u"岗位级别")
    Ejob = forms.CharField(required=False,label=u"招聘职位")
    Ejobin = forms.CharField(required=False,label=u"招聘渠道")
    Ejobaim = forms.CharField(required=False,label=u"招聘目的")
    Eprimary = forms.CharField(required=False,label=u"一级部门")
    Esecond = forms.CharField(required=False,label=u"二级部门")
    Eproject = forms.CharField(required=False,label=u"三级工作小组")
    Ecompacttime = forms.CharField(required=False,label=u"合同期限")
    Eapplytime = forms.CharField(required=False,label=u"试用期限")
    #models继承
    class Meta:
        model = Mail_Offer
        fields = ('Ename','Ephone','Email','Eentrytime','Epost','Epostgrade','Ejob','Ejobin','Ejobaim','Eprimary','Esecond','Eproject','Ecompacttime','Eapplytime')

