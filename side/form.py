# -*- encoding: utf-8 -*-
"""
Created on Aug 30 2015

@author: fengyan
last change 11 11 2015
"""
import os, sys
from django import forms  
from django.db import models  
from accounts.models import *
from side.models import *
from resume.models import *
from talents.models import *
from manager.models import *
import string

reload(sys)
sys.setdefaultencoding('utf8')

Level_choice = ( 
    (0, u"无星"),         
    (1, u"一星"),         
    (2, u"二星"), 
    (3, u"三星"), 
)
Status_choice = ( 
    (u'一面', u"一面"),         
    (u'二面', u"二面"),         
    (u'三面', u"三面"), 
    (u'淘汰', u"淘汰"), 
    (u'填写offer信息', u"填写offer信息"), 
    (u'推荐', u"推荐"), 
)
#没用
InterviewProcess_choice = (
    (u'电话面试', u"电话面试"), 
    (u'一面', u"一面"),         
    (u'二面', u"二面"),         
    (u'三面', u"三面"), 
)
Status1_choice = (
    (u'',u''),
    (u'已入职',u'已入职'),
    (u'发offer未入职',u'发offer未入职'),
)
Iaddr_choice = (
    (u'',u''),
    (u'公司',u'公司'),
    (u'光大银行西二旗数据中心',u'光大银行西二旗数据中心'),
    (u'建行洋桥数据中心',u'建行洋桥数据中心'),
    (u'中国银行黑山扈数据中心',u'中国银行黑山扈数据中心'),
)


#新的面试表单数据定义
class InterviewForm(forms.ModelForm): 
    #只做表单形式数据由后台添加 
    resume = forms.ModelChoiceField(queryset=Resume.objects.all().exclude(UserID=None),label=u"*候选人",required=False,initial=1)  
    user = forms.ModelChoiceField(queryset=MyUser.objects.all(),label=u"*面试官",required=False,initial=1)
    InterviewProcess= forms.CharField(label=u"*面试过程",required=False,initial=u"未处理") 
    
    InterviewResults = forms.CharField(label=u"*面试评价",widget=forms.Textarea,required=True,error_messages={'required': u'请填写面试记录'})
    Level = forms.ChoiceField(label=u"*候选人水平",required=True, choices=Level_choice,error_messages={'required': u'请选择候选人水平'})
    Time = forms.DateTimeField(label=u"*面试时间",required=True,error_messages={'required': u'请选择面试时间'})
    Status = forms.ChoiceField(choices=Status_choice,widget=forms.Select(),label=u"*候选人下一步状态",required=False,error_messages={'required': u'请选择候选人下一步状态'})
    #NextUser = forms.ModelMultipleChoiceField(queryset=MyUser.objects.all(),label=u"*下一步处理人", widget=forms.CheckboxSelectMultiple,required=False,error_messages={'required': u'请选择下一步处理人'})

    #models继承
    class Meta:
        model = Interview
        fields = ('resume','user','InterviewResults','InterviewProcess','Level','Time','Status','NextUser','Turn','Projectname')
#新的入职表单数据定义
class EntryForm(forms.ModelForm):  
    resume = forms.ModelChoiceField(queryset=Resume.objects.all().exclude(UserID=None),label=u"*候选人",required=False,initial=1)  
    user = forms.ModelChoiceField(queryset=MyUser.objects.all(),label=u"*操作人",required=False,initial=1)
    position = forms.ModelChoiceField(queryset=Position.objects.all().filter(Filing=0),label=u"*入职职位",required=True,initial=1,error_messages={'required': u'请选择需要或可能入职职位'})
    EntryResults = forms.CharField(label=u"*入职记录",widget=forms.Textarea,required=True,error_messages={'required': u'请填写记录'})
    Time = forms.DateTimeField(label=u"*入职时间",required=True,error_messages={'required': u'请选择面试时间'})
    Status1 = forms.ChoiceField(choices=Status1_choice,widget=forms.Select(),label=u"*候选人下一步状态",required=True,error_messages={'required': u'请选择候选人下一步状态'})
    #models继承
    class Meta:
        model = Entry
        fields = ('resume','position','user','EntryResults','Time')
        
#邀请函表单数据定义
class InvitationForm(forms.ModelForm):  
    Iname = forms.CharField(required=True,label=u"接待人",error_messages={'required': u'请填写接待人姓名'})
    Itime = forms.DateField(required=True,label=u"日期",error_messages={'required': u'请填写日期'})
    time1 = forms.CharField(required=True,label=u"时间",error_messages={'required': u'时间'})
    time2 = forms.CharField(required=True,label=u"时间",error_messages={'required': u'时间'})
    Iphone = forms.CharField(required=True,label=u"电话",error_messages={'required': u'请填写接待人联系方式'})
    Inotes = forms.CharField(required=False,label=u"备注")
    Iaddr = forms.ChoiceField(choices=Iaddr_choice,widget=forms.Select(),label=u"地址",required=True,error_messages={'required': u'请选择一个地址'})
    #models继承
    class Meta:
        model = Invitation
        fields = ('Itime','Iaddr','Iname','Iphone','Inotes')
#异常处理表单数据定义
class ChangeRecordForm(forms.ModelForm):  
    Cname = forms.CharField(required=False,label=u"填写人")
    #Ctime = forms.DateTimeField(required=True,label=u"时间",error_messages={'required': u'请填写时间'})
    Creason = forms.CharField(required=True,label=u"原因",widget=forms.Textarea,error_messages={'required': u'请填写原因'})
    
    Ctype = forms.CharField(required=True,label=u"类型",error_messages={'required': u'选择类型'})
    Cnotes = forms.CharField(required=False,label=u"备注",widget=forms.Textarea)
    #models继承
    class Meta:
        model = ChangeRecord
        fields = ('Ctype','Creason','Cname','Cnotes')

