
from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from accounts.models import MyUser
# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=32,null=True,unique=True)
    superior_department = models.ForeignKey('self',blank=True,null=True)
    level =  models.CharField(max_length=32,null=True)
    temp_2 =  models.CharField(max_length=32,null=True) 
    temp_3 =  models.CharField(max_length=32,null=True)
    temp_4 =  models.CharField(max_length=32,null=True)
    def __unicode__(self):                                                 
         return u'%s' % (self.name) 
admin.site.register(Department)
class Roles(models.Model):
    name = models.CharField(max_length=32,null=True)
    DepartmentID = models.ForeignKey(Department,blank=True,null=True)
    superior_role = models.ForeignKey('self',blank=True,null=True)
    temp_1 =  models.CharField(max_length=32,null=True)
    temp_2 =  models.CharField(max_length=32,null=True) 
    temp_3 =  models.CharField(max_length=32,null=True)
    temp_4 =  models.CharField(max_length=32,null=True)
    def __unicode__(self):                                                 
         return u'%s %s' % (self.name,self.DepartmentID)  
admin.site.register(Roles)

class Cor_role_user_depart(models.Model):
    UserID = models.ForeignKey(MyUser,max_length=32,null=True)
    RoleID = models.ForeignKey(Roles,blank=True,null=True)
    temp_1 =  models.CharField(max_length=32,null=True)
    temp_2 =  models.CharField(max_length=32,null=True) 
    temp_3 =  models.CharField(max_length=32,null=True)
    temp_4 =  models.CharField(max_length=32,null=True) 
admin.site.register(Cor_role_user_depart)
class Power(models.Model):
    name =  models.CharField(max_length=32,null=True)
    temp_1 =  models.CharField(max_length=32,null=True)
    temp_5 =  models.CharField(max_length=32,null=True)
    temp_2 =  models.CharField(max_length=32,null=True) 
    temp_3 =  models.CharField(max_length=32,null=True)
    temp_4 =  models.CharField(max_length=32,null=True) 
    def __unicode__(self):                                                 
         return u'%s' % (self.name) 
admin.site.register(Power)
class Cor_user_Power(models.Model):
    PowerID = models.ForeignKey(Power,blank=True,null=True)
    UserID = models.ForeignKey(MyUser,related_name='power_user', blank=True,null=True)
    temp_1 =  models.CharField(max_length=32,null=True)
    temp_2 =  models.CharField(max_length=32,null=True) 
    temp_3 =  models.CharField(max_length=32,null=True)
    temp_4 =  models.CharField(max_length=32,null=True) 
admin.site.register(Cor_user_Power)
class Email(models.Model):
    mail=models.EmailField(blank=True,null=True)
    password=models.CharField(max_length=32,null=True) 
class Rule(models.Model):
    name =  models.CharField(max_length=32,null=True)
    temp_1 =  models.CharField(max_length=32,null=True)
    temp_5 =  models.CharField(max_length=32,null=True)
    temp_2 =  models.CharField(max_length=32,null=True) 
    temp_3 =  models.CharField(max_length=32,null=True)
    temp_4 =  models.CharField(max_length=32,null=True) 
    def __unicode__(self):                                                 
         return u'%s' % (self.name) 
admin.site.register(Rule)

class Cor_User_Rule(models.Model):
    RuleID = models.ForeignKey(Rule,blank=True,null=True)
    UserID = models.ForeignKey(MyUser,related_name='rule_user', blank=True,null=True)
    temp_1 =  models.CharField(max_length=32,null=True)
    temp_2 =  models.CharField(max_length=32,null=True) 
    temp_3 =  models.CharField(max_length=32,null=True)
    temp_4 =  models.CharField(max_length=32,null=True) 
admin.site.register(Cor_User_Rule)

class Cor_Rule_Power(models.Model):
    RuleID = models.ForeignKey(Rule,blank=True,null=True)
    PowerID = models.ForeignKey(Power,blank=True,null=True)
    temp_1 =  models.CharField(max_length=32,null=True)
    temp_5 =  models.CharField(max_length=32,null=True)
    temp_2 =  models.CharField(max_length=32,null=True) 
    temp_3 =  models.CharField(max_length=32,null=True)
    temp_4 =  models.CharField(max_length=32,null=True) 
admin.site.register(Cor_Rule_Power)

class Customer(models.Model):
    name = models.CharField(max_length=32,null=True)
    customer_manager = models.ForeignKey(MyUser,max_length=32,null=True)
    depart = models.ForeignKey(Department,max_length=32,null=True)
    def __unicode__(self):                                                 
         return u'%s' % (self.name) 
admin.site.register(Customer)
class Third_project(models.Model):
    name = models.CharField(max_length=32,null=True)
    project_manager = models.ForeignKey(MyUser,max_length=32,null=True)
    recruiter = models.ForeignKey(MyUser,related_name='recruiters',max_length=32,null=True) 
    customer = models.ForeignKey(Customer,max_length=32,null=True)
    def __unicode__(self):                                                 
         return u'%s' % (self.name) 
admin.site.register(Third_project)
