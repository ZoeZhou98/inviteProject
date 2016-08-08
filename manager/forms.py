#encoding=UTF-8
from django import forms
from django.forms import ModelForm
from manager.models import Third_project,Roles,Rule,Department,Power,Cor_role_user_depart,Cor_user_Power,Email,Cor_User_Rule,Customer
from accounts.models import MyUser
class DepartmentForm(ModelForm): 
    name = forms.CharField(max_length=32,required=True,error_messages={'required': u'部门名称不能为空','unique':'重复'},label=u'* 部门名称 ')
    superior_department = forms.ModelChoiceField(queryset=Department.objects.all(),label=u'上级部门 ',required = False)
    class Meta:
        model = Department
        fields=('name','superior_department') 
        
class RoleForm(ModelForm):
     name = forms.CharField(max_length=32,required=True,error_messages={'required': u'职位名称不能为空'},label=u'* 角色名称 ')
     DepartmentID = forms.ModelChoiceField(queryset=Department.objects.all(),label=u'* 部门名称 ',required = True,error_messages={'required': u'所处部门不能为空'})
     superior_role = forms.ModelChoiceField(queryset=Roles.objects.all(),label=u'上级职位 ',required = False)
     class Meta:
        model = Roles
        fields=('name','superior_role','DepartmentID')
class PowerForm(ModelForm): 
    name = forms.CharField(max_length=32,required=True,error_messages={'required': u'权限名称不能为空'},label=u'* 权限名称 ')
    class Meta:
        model = Power
        fields=('name',)
    
class Cor_role_user_departForm(ModelForm): 
    UserID = forms.ModelChoiceField(queryset=MyUser.objects.all(),label=u'* 用户名 ',required = True,error_messages={'required': u'用户名不能为空'})
    RoleID = forms.ModelChoiceField(queryset=Roles.objects.all(),label=u'* 职位 ',required = True,error_messages={'required': u'职位不能为空'})
    class Meta:
        model = Cor_role_user_depart
        fields=('UserID','RoleID')
class Cor_user_powerForm(ModelForm):
    UserID = forms.ModelChoiceField(queryset=MyUser.objects.all(),label=u'* 用户名 ',required = True,error_messages={'required': u'用户名不能为空'})
    PowerID = forms.ModelChoiceField(queryset=Power.objects.all(),label=u'* 权限名',required = True,error_messages={'required': u'权限名不能为空'})
    class Meta:
        model = Cor_user_Power
        fields=('UserID','PowerID')
class EmailForm(ModelForm):
    mail = forms.EmailField(required=True,label=u'*邮箱',error_messages={'required': u'邮箱不能为空'})
    password=forms.CharField(required=True,label=u'*密码',error_messages={'required': u'密码不能为空'},widget=forms.PasswordInput(attrs={'placeholder':u"密码"}))
    class Meta:
        model = Email
        fields=('mail','password')
class RuleForm(ModelForm):
    name = forms.CharField(max_length=32,required=True,error_messages={'required': u'角色名称不能为空'},label=u'* 角色名称 ')
    PowerID = forms.ModelMultipleChoiceField(queryset=Power.objects.all(),label=u'* 职位',widget=forms.CheckboxSelectMultiple,required = True,error_messages={'required': u'权限不可以为空'})
    class Meta:
        model = Rule
        fields=('name','PowerID')
class Cor_User_RuleForm(ModelForm):
    UserID = forms.ModelChoiceField(queryset=MyUser.objects.all(),label=u'* 用户名 ',required = True,error_messages={'required': u'用户名不能为空'})
    RuleID = forms.ModelChoiceField(queryset=Rule.objects.all(),label=u'* 角色名',required = True,error_messages={'required': u'角色名不能为空'})
    class Meta:
        model = Cor_User_Rule
        fields=('UserID','RuleID')
class Third_projectForm(ModelForm):
    name = forms.CharField(max_length=32,required=True,error_messages={'required': u'名称不能为空'},label=u'* 三级项目小组名称')
    project_manager = forms.ModelChoiceField(queryset=MyUser.objects.all(),label=u'* 项目经理 ',required = True,error_messages={'required': u'项目经理不能为空'})
    recruiter = forms.ModelChoiceField(queryset=MyUser.objects.all(),label=u'* 招聘发起人 ',required = True,error_messages={'required': u'发起人不能为空'})
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(),label=u'* 客户',required = True,error_messages={'required': u'客户不能为空'})
    class Meta:
        model = Third_project
        fields=('name','project_manager','recruiter','customer')
class CustomerForm(ModelForm):
    name = forms.CharField(max_length=32,required=True,error_messages={'required': u'名称为空'},label=u'* 客户名称')
    customer_manager = forms.ModelChoiceField(queryset=MyUser.objects.all(),label=u'* 客户负责人 ',required = True,error_messages={'required': u'客户负责人不能为空'})
    depart = forms.ModelChoiceField(queryset=Department.objects.all(),label=u'* 一级部门 ',required =True,error_messages={'required': u'一级部门不能为空'})
    class Meta:
        model = Customer
        fields=('name','customer_manager','depart')
