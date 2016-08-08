#encoding=UTF-8
from django.db import models
from django.contrib import admin
from accounts.models import MyUser
from talents.models import Position
from manager.models import Cor_role_user_depart,Roles,Department,Power,Cor_user_Power
from datetime import *  
import time
import django.utils.timezone as timezone
# Create your models here.
class Resume(models.Model):
    UserID = models.ForeignKey(MyUser,blank=True,null=True)
    SearchID = models.CharField(max_length=32,null=True)
    PositionName = models.CharField(max_length=128,null=True)
    CandidateName = models.CharField(max_length=32,null=True)
    CandidateSex = models.CharField(null=True,max_length=4)
    CandidateAge = models.CharField(null=True,max_length=11)
    CandidatePhone = models.CharField(max_length=11,null=True)
    CandidateEmail = models.EmailField(max_length=32,null=True)
    CandidateProfile = models.IntegerField(blank=True,null=True)
    Candidate_edu = models.CharField(max_length=20,null=True)
    referrerID = models.ForeignKey(MyUser,related_name='Resume_referrerID',blank=True,null=True)
    Addr = models.CharField(max_length=64)
    Status = models.CharField(max_length=20,default="未处理", editable=False)
    Level = models.SmallIntegerField(blank=True,null=True)
    Time = models.DateTimeField(default=timezone.now())
    NextUser = models.ManyToManyField(MyUser,related_name='Resume_NextUser',blank=True)
    Notes = models.CharField(max_length=128,blank=True,null=True)
    Agency = models.ForeignKey(MyUser,related_name='Resume_Agency',blank=True,null=True)
    lastinter = models.CharField(max_length=32,blank=True,null=True)
    Station = models.ForeignKey(Position,related_name='Resume_Station',blank=True,null=True)
    LockTime = models.DateTimeField(blank=True,null=True)
    Turn = models.SmallIntegerField(blank=True,null=True)
    temp_2 =  models.CharField(max_length=32,null=True,blank=True) 
    temp_3 =  models.CharField(max_length=32,null=True,blank=True)
    temp_4 =  models.CharField(max_length=32,null=True,blank=True) 
    temp_5 =  models.CharField(max_length=32,null=True,blank=True)
    temp_6 =  models.CharField(max_length=32,null=True,blank=True)
    temp_7 =  models.CharField(max_length=32,null=True,blank=True)
    def __unicode__(self):
        return self.CandidateName
admin.site.register(Resume)    
class Repeat_Resume(models.Model):
    user_name = models.CharField(max_length=32,null=True)
    resume_phone = models.CharField(max_length=32,null=True)
    referrerID = models.ForeignKey(MyUser,blank=True,null=True) 
    Time = models.DateTimeField(auto_now_add=True)
    #temp_1 =  models.CharField(max_length=32,null=True)
    temp_2 =  models.CharField(max_length=32,null=True) 
    temp_3 =  models.CharField(max_length=32,null=True)
    temp_4 =  models.CharField(max_length=32,null=True) 
admin.site.register(Repeat_Resume)

class fail_import_id(models.Model):
    user_name = models.CharField(max_length=32,null=True)
    resume_id = models.CharField(max_length=32,null=True)
    source =  models.CharField(max_length=32,null=True)
    referrerID = models.ForeignKey(MyUser,blank=True,null=True) 
    temp_3 =  models.CharField(max_length=32,null=True)
    temp_4 =  models.CharField(max_length=32,null=True) 
admin.site.register(fail_import_id)
from talents.models import Position 
class importid_group(models.Model):
    userID = models.ForeignKey(MyUser,blank=True,null=True) 
    Time = models.DateTimeField(auto_now_add=True)
    remark = models.TextField(blank=True,null=True)
    PositionID = models.ForeignKey(Position,blank=True,null=True) 
    DepartID = models.ForeignKey(Department,blank=True,null=True) 
    referrerID = models.ForeignKey(MyUser,related_name='import_referrerID',blank=True,null=True) 
    Status = models.SmallIntegerField(null=True,default=0)   
admin.site.register(importid_group)
class import_ID(models.Model):
    user_name = models.CharField(max_length=32,null=True)
    resume_id = models.CharField(max_length=32,null=True)
    source =  models.CharField(max_length=32,null=True)
    referrerID = models.ForeignKey(MyUser,blank=True,null=True) 
    UploaderID = models.ForeignKey(MyUser,related_name='import_UploaderID',blank=True,null=True) 
    Time = models.DateTimeField(auto_now=True)
    Status = models.SmallIntegerField(null=True,default=0)   
    remark = models.TextField(blank=True,null=True)
    groupid = models.ForeignKey(importid_group,blank=True,null=True)
admin.site.register(import_ID)

class Mail_Offer(models.Model):
    resume = models.ForeignKey(Resume,blank=True,null=True)
    Ename = models.CharField(max_length=32,blank=True,null=True)
    Ephone = models.CharField(max_length=32,blank=True,null=True)
    Email = models.CharField(max_length=32,blank=True,null=True)
    Eentrytime = models.CharField(max_length=32,blank=True,null=True)
    Epost = models.CharField(max_length=32,blank=True,null=True)
    Epostgrade = models.CharField(max_length=32,blank=True,null=True)
    Ejob = models.CharField(max_length=32,blank=True,null=True)
    Ejobin = models.CharField(max_length=32,blank=True,null=True)
    Ejobaim = models.CharField(max_length=32,blank=True,null=True)
    Eprimary = models.CharField(max_length=32,blank=True,null=True)
    Esecond = models.CharField(max_length=32,blank=True,null=True)
    Eproject = models.CharField(max_length=32,blank=True,null=True)
    Ecompacttime = models.CharField(max_length=32,blank=True,null=True)
    Eapplytime = models.CharField(max_length=32,blank=True,null=True)
    temp_1 =  models.CharField(max_length=32,null=True,blank=True)
    temp_2 =  models.CharField(max_length=32,null=True,blank=True) 
    temp_3 =  models.CharField(max_length=32,null=True,blank=True)
    temp_4 =  models.CharField(max_length=32,null=True,blank=True)
    handletime = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    handleuser = models.ForeignKey(MyUser,blank=True,null=True)
    
admin.site.register(Mail_Offer)  
    
