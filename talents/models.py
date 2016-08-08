#encoding=UTF-8
from django.db import models
from django.contrib import admin
from accounts.models import MyUser 
#from  resume.models import Resume
from manager.models import Department
# Create your models here.

class Position(models.Model):
    PositionName = models.CharField(max_length=100)
    UserID = models.ForeignKey(MyUser,null=True)
    Phone1 = models.CharField(max_length=11,blank=True,null=True)
    Depart = models.ForeignKey(Department,null=True)
    SecondDepartment = models.ForeignKey(Department,related_name='Position_SecondDepartment',null=True)
    ExistingPersonNum = models.IntegerField(blank=True,null=True)
    NeedPersonNum = models.IntegerField(blank=True,null=True)
    recruitednum = models.IntegerField(blank=True,default=0,null=True)
    Workplace = models.CharField(max_length=32,blank=True,null=True)
    ProjectName = models.CharField(max_length=32,blank=True,null=True)
    LoWSalary = models.IntegerField(blank=True,null=True)
    HighSalary = models.IntegerField(blank=True,null=True)  
    #Salary = models.CharField(max_length=32,blank=True,null=True)
    RecruitTime = models.DateTimeField(null=True)
    Headline = models.DateTimeField(null=True)
    RecruitReason = models.SmallIntegerField(blank=True,null=True)
    RecruitTime = models.CharField(blank=True,null=True,max_length=100)
    WorkContent = models.TextField(blank=True,null=True)
    CandidateRequirement = models.TextField(null=True)
    RecruitWay = models.SmallIntegerField(blank=True,null=True)
    Approver=models.ForeignKey(MyUser,related_name='Position_Approver',null=True)
    States=models.CharField(max_length=12,default="未处理",blank=True,null=True)
    Accept=models.SmallIntegerField(blank=True,null=True)    
    Awarding=models.IntegerField(blank=True,null=True)
    Email=models.EmailField(default='si_zhaopin@nantian.com.cn',blank=True)
    Filing=models.SmallIntegerField(blank=True,default=2)
    Salary =  models.CharField(max_length=32,null=True,blank=True)
    add_reason =  models.TextField(blank=True,null=True)
    pub_time =  models.DateTimeField(null=True) 
    temp_3 =  models.CharField(max_length=32,null=True)
    temp_4 =  models.CharField(max_length=32,null=True) 
    def __unicode__(self):
        return u'%s %s' % (self.PositionName,self.UserID.username)
admin.site.register(Position) 

class Examine(models.Model):
    PositionID = models.ForeignKey(Position)
    UserID=models.ForeignKey(MyUser)
    Result=models.CharField(max_length=12,blank=True)
    Time=models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True,null=True)
    next_approver=models.ForeignKey(MyUser,related_name='Examine_next_user',null=True)
    last_user=models.ForeignKey(MyUser,related_name='Examine_last_user',null=True)
    Is_resultful = models.SmallIntegerField(blank=True,null=True)
    Count = models.SmallIntegerField(blank=True,null=True)
    temp_1 =  models.CharField(max_length=32,null=True)
    temp_5 =  models.CharField(max_length=32,null=True)
    temp_2 =  models.CharField(max_length=32,null=True) 
    temp_3 =  models.CharField(max_length=32,null=True)
    temp_4 =  models.CharField(max_length=32,null=True) 

   
