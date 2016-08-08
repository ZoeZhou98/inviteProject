# -*- encoding: utf-8 -*-
"""
Created on Aug 30 2015

@author: fengyan
last change 11 11 2015
"""
from django.db import models
from django.contrib import admin
from accounts.models import MyUser
from resume.models import Resume
from talents.models import Position
#models定义数据库数据类型    
class Interview(models.Model):
    resume = models.ForeignKey(Resume,blank=True,null=True)
    user = models.ForeignKey(MyUser,blank=True,null=True)
    InterviewResults = models.TextField()
    Level = models.SmallIntegerField(blank=True,null=True)
    Time = models.DateTimeField(blank=True,null=True)
    InterviewProcess = models.CharField(max_length=20,default="未处理",blank=True,null=True)
    NextUser = models.ManyToManyField(MyUser,related_name='Interview_NextUser',blank=True)
    lockuser = models.ForeignKey(MyUser,related_name='Interview_lockuser',blank=True,null=True)
    InterStatus = models.CharField(max_length=20,default="未处理",blank=True,null=True)
    Notes = models.CharField(max_length=100,blank=True,null=True)
    Turn = models.SmallIntegerField(blank=True,null=True)
    Projectname = models.CharField(max_length=64,blank=True,null=True)
    #Offer = models.CharField(max_length=32,blank=True,null=True)
    Agency = models.ForeignKey(MyUser,related_name='Interview_Agency',blank=True,null=True)
    Active = models.SmallIntegerField(blank=True,null=True,default=1)
    temp_1 =  models.CharField(max_length=32,null=True,blank=True)
    temp_2 =  models.CharField(max_length=32,null=True,blank=True)
    temp_3 =  models.CharField(max_length=32,null=True,blank=True)
    temp_4 =  models.CharField(max_length=32,null=True,blank=True)
    handletime = models.DateTimeField(auto_now_add=True,blank=True,null=True)
#注册到admin
admin.site.register(Interview)
#models定义数据库数据类型
class Entry(models.Model):
    resume = models.ForeignKey(Resume,blank=True,null=True)
    position = models.ForeignKey(Position,blank=True,null=True)
    user = models.ForeignKey(MyUser,blank=True,null=True)
    EntryResults = models.TextField()
    Time = models.DateTimeField(blank=True,null=True)
    temp_1 =  models.CharField(max_length=32,null=True,blank=True)
    temp_2 =  models.CharField(max_length=32,null=True,blank=True)
    temp_3 =  models.CharField(max_length=32,null=True,blank=True)
    temp_4 =  models.CharField(max_length=32,null=True,blank=True)
    handletime = models.DateTimeField(auto_now_add=True,blank=True,null=True)
#注册到admin
admin.site.register(Entry)
#models定义数据库数据类型
class Invitation(models.Model):
    interview = models.ForeignKey(Interview,blank=True,null=True)
    Iaddr = models.CharField(max_length=32,null=True,blank=True)
    Itime = models.CharField(max_length=32,null=True,blank=True)
    Iname = models.CharField(max_length=32,null=True,blank=True)
    Iphone = models.CharField(max_length=32,null=True,blank=True)
    Imail = models.CharField(max_length=32,null=True,blank=True)
    Inotes = models.CharField(max_length=64,null=True,blank=True)
    temp_1 =  models.CharField(max_length=32,null=True,blank=True)
    temp_2 =  models.CharField(max_length=32,null=True,blank=True)
    temp_3 =  models.CharField(max_length=32,null=True,blank=True)
    temp_4 =  models.CharField(max_length=32,null=True,blank=True)
    handletime = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    handleuser = models.ForeignKey(MyUser,blank=True,null=True)
#注册到admin
admin.site.register(Invitation)
class ChangeRecord(models.Model):
    interview = models.ForeignKey(Interview,blank=True,null=True)
    Cname = models.CharField(max_length=32,null=True,blank=True)
    Ctype = models.CharField(max_length=32,null=True,blank=True)
    Creason = models.CharField(max_length=32,null=True,blank=True)
    Ctime = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    Cnotes = models.CharField(max_length=64,null=True,blank=True)
    temp_1 =  models.CharField(max_length=32,null=True,blank=True)
    temp_2 =  models.CharField(max_length=32,null=True,blank=True)
    temp_3 =  models.CharField(max_length=32,null=True,blank=True)
    temp_4 =  models.CharField(max_length=32,null=True,blank=True)
#注册到admin
admin.site.register(ChangeRecord)
class EmailRecord(models.Model):
    resume = models.ForeignKey(Resume,blank=True,null=True)
    interview = models.ForeignKey(Interview,blank=True,null=True)
    handleuser = models.ForeignKey(MyUser,blank=True,null=True)
    handletime = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    touser = models.CharField(max_length=32,null=True,blank=True)
    Type = models.CharField(max_length=32,null=True,blank=True)
    notes = models.CharField(max_length=32,null=True,blank=True)
    cc = models.TextField(null=True,blank=True)
    bcc = models.TextField(null=True,blank=True)
#注册到admin
admin.site.register(EmailRecord)

class HandleRecord(models.Model):
    resume = models.ForeignKey(Resume,blank=True,null=True)
    interview = models.ForeignKey(Interview,blank=True,null=True)
    handleuser = models.ForeignKey(MyUser,blank=True,null=True)
    handletime = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    Type = models.CharField(max_length=32,null=True,blank=True)
    active = models.SmallIntegerField(blank=True,null=True,default=1)
    notes = models.CharField(max_length=32,null=True,blank=True)
#注册到admin
admin.site.register(HandleRecord)
    

