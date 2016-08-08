from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from django.contrib.auth.models import (AbstractUser,AbstractBaseUser,BaseUserManager)

class MyUser(AbstractUser):
    mobile   = models.CharField(max_length=11,unique=True)
    rule = models.CharField(max_length=20,null=True)
    mail_password = models.CharField(('password'), max_length=128,null=True)
    forget_time=models.CharField(max_length=50,blank=True,null=True)
    temp_1 =  models.CharField(max_length=32,null=True,blank=True)
    temp_2 =  models.CharField(max_length=32,null=True,blank=True) 
    temp_3 =  models.CharField(max_length=32,null=True,blank=True)
    temp_4 =  models.CharField(max_length=32,null=True,blank=True) 
    class Meta:
        db_table = 'user'

class MyUserForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ('username','email','mobile')
admin.site.register(MyUser)
