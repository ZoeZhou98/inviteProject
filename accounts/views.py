# -*- encoding: utf-8 -*-
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core import mail
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.shortcuts import resolve_url
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login,logout as auth_logout, get_user_model, update_session_auth_hash)
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth import get_user_model
from django.contrib.auth import login,logout
from django.template import loader, Context
from django.template.context import RequestContext
from django.utils import timezone
from accounts.models import MyUser,MyUserForm
from resume.models import Resume,import_ID
from resume.views import receive_middle
from manager.models import Department,Power,Roles,Cor_role_user_depart,Cor_user_Power,Cor_User_Rule,Rule,Cor_Rule_Power
from side.models import Interview
from talents.models import Position
from django.contrib import auth
from django.db.models import Q,F
from uuslug import slugify
from talents.views import inspectiontime,get_depart
from django.utils.timezone import now,timedelta
import codecs
import time
import re
import random
from accounts.forms import ChangepwdForm,LoginForm
import os
from talents.views import get_role
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class LoginBackend(object):
    def authenticate(self,username=None, password=None, **kwargs):
        UserModel = get_user_model()
    
        if username:
            #email
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", username) != None:
                try:
                    user = UserModel.objects.get(email=username)
                    if user.check_password(password):
                        return user
                except UserModel.DoesNotExist:
                    return None
            #mobile
            elif len(username)==11 and re.match("^(1[3458]\d{9})$", username) != None:
                try:
                    user = UserModel.objects.get(mobile=username)
                    if user.check_password(password):
                        return user
                except UserModel.DoesNotExist:
                    return None
        else:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
                
def alogin(request):
    errors= []
    account=None
    password=None
    if request.method == 'POST' :
        if not request.POST.get('account'):
            errors.append('账户不能为空')
        else:
            account = request.POST.get('account')
        if not request.POST.get('password'):
            errors.append('请输入密码')
        else:
            password= request.POST.get('password')
        if request.POST.get('autoLogin'):
            request.session.set_expiry(604800)        
        else:
            request.session.set_expiry(0)
        if account is not None and password is not None :
            user = auth.authenticate(username=account,password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request,user)
                    receive_middle()
                    return HttpResponseRedirect('/')
                else:
                    errors.append('账户已禁用')
            else :
                errors.append('无效的用户名或密码')
    return render_to_response('login.html', {'errors': errors})

'''
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  
        if form.is_valid():  
            username = request.POST.get('username', '')  
            password = request.POST.get('password', '')  
            user = auth.authenticate(username=username, password=password)  
            if user is not None and user.is_active:  
                auth.login(request, user)  
                return render_to_response('/', RequestContext(request))  
            else:  
                return render_to_response('login', RequestContext(request, {'form': form,'password_is_wrong':True}))  
        else:  
            return render_to_response('login', RequestContext(request, {'form': form,}))
    else:
        form = LoginForm()  
        return render_to_response('login', RequestContext(request, {'form': form,}))
'''
def register(request):
    errors= []
    account=None
    password=None
    password2=None
    email=None
    CompareFlag=False
    mobile = None
    role = None
    rules =  Rule.objects.all()
    roles_departments = Roles.objects.all()
    if request.method == 'POST':
        if not request.POST.get('account'):
            errors.append('请输入用户名')
        else:
            account = request.POST.get('account')
            temp_user3 = MyUser.objects.filter(username=account)
            if len(temp_user3) != 0:
                errors.append('该用户名已注册')
        if not request.POST.get('password'):
            errors.append('请输入密码')
        else:
            password = request.POST.get('password')
        if not request.POST.get('password2'):
            errors.append('请再次输入密码')
        else:
            password2 = request.POST.get('password2')
        if not request.POST.get('email'):
            errors.append('请输入邮箱')
        else:
            email = request.POST.get('email')
            temp_user1 = MyUser.objects.filter(email=email)
            if len(temp_user1) != 0:
                errors.append('该邮箱已注册')
        if not request.POST.get('mobile'):
            errors.append('请输入手机号')
        else:
            mobile = request.POST.get('mobile')   
            temp_user2 = MyUser.objects.filter(mobile=mobile)
            if len(temp_user2) != 0:
                errors.append('该手机号已注册')
        if not request.POST.get('role'):
            errors.append('请选择职位')
        else:
            role = request.POST.get('role')
            
        if not request.POST.get('rule'):
            errors.append('请选择角色')
        else:
            rule = request.POST.get('rule')  
             
        if password is not None and password2 is not None:
            if password == password2:
                CompareFlag = True
            else :
                errors.append('两次输入的密码不一致')

        if len(errors)>0:
            return render_to_response('register.html', {'errors': errors,'account':account,'email':email,'mobile':mobile,'rules':rules,'roles_departments':roles_departments})
        if account is not None and password is not None and password2 is not None and email is not None and mobile is not None and role is not None and CompareFlag and len(temp_user1) == 0 and len(temp_user2) == 0 and len(temp_user3) == 0:  
            now = timezone.now()            
            user = MyUser(username=account,last_login=now,date_joined=now,email=email)
            user.is_active = True
            user.set_password(password)
            user.mobile = str(mobile)
#             user.rule = role
            user.save()
            rule_obj = Rule.objects.get(id= int(rule))
            role_obj = Roles.objects.get(id = int(role))
            rules =  Rule.objects.all()
            roles_departments = Roles.objects.all()
            rule_powers = Cor_Rule_Power.objects.filter(RuleID=rule_obj) 
            Cor_User_Rule.objects.get_or_create( 
                                         RuleID=rule_obj, 
                                         UserID=user,
                                        )
            for power in rule_powers:
                Cor_user_Power.objects.get_or_create(
                    PowerID = power.PowerID,
                    UserID =user,
                                                    )

            Cor_role_user_depart.objects.get_or_create( 
                             UserID=user, 
                             RoleID=role_obj,
                                        )  
            add()
            return HttpResponseRedirect('/accounts/login')
            
    else:
        return render_to_response('register.html', {'errors': errors,'account':account,'email':email,'mobile':mobile,'rules':rules,'roles_departments':roles_departments})

def alogout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required 
def refresh(request):
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    str_req=''
    try:
        str_req = request.GET['a']
    except:
        pass
    finally:
        pass
    if str_req == '1':
        renli=False
        #secondrule=False
        #cookie
        UserModel = get_user_model()
        session_id = request.COOKIES['sessionid']
        user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
        user = UserModel.objects.get(id = user_id)
        #特殊处理
        Powers=[]
        powers=Cor_user_Power.objects.filter(UserID=user_id)
        for power in powers:
            Powers.append(power.PowerID.id)
        #待招聘的岗位(特殊9)
        roles=get_role(user)
        num=0
        pos=[]
        for role in roles:
            if role.name == "招聘专员":
               department=role.DepartmentID
               pos=Position.objects.filter(Q(Depart=department)|Q(SecondDepartment=department)).filter(Filing = 0)
               num=len(pos)
               break
            else:
               pos=Position.objects.filter(UserID=user_id).filter(Filing=0)
               num=len(pos)
               break
        
        #招聘中的职位
        positions=Position.objects.filter(UserID=user_id).filter(Filing=0)
        #待处理的职位(审批、申请权  1or2)
        handlepositions=Position.objects.filter(Approver=user_id,Filing=2)
        amount=len(handlepositions)
        #待发布的职位(特殊7)
        publishing_positions=Position.objects.filter(Filing=4)
        publishing=len(publishing_positions)
        #待处理的面试(面试权6)
        inters1 = Resume.objects.filter(Status=u"未处理")
        inters = inters1.filter(Q(UserID=user_id,Agency=None)|Q(Agency=user_id))
        inters2 = Interview.objects.filter(Q(resume__Status=u"一面",InterviewProcess=u"电话面试",InterStatus=u"通过")|Q(resume__Status=u"一面",InterviewProcess=u"电话面试",InterStatus=u"发邀请函") | Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"通过")| Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"发邀请函")| Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"通过")| Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"发邀请函")|Q(resume__Status=u"填写offer信息",InterviewProcess=u"二面",InterStatus=u"填写offer信息")|Q(resume__Status=u"填写offer信息",InterviewProcess=u"三面",InterStatus=u"填写offer信息")|Q(resume__Status=u"审批offer信息",InterviewProcess=u"二面",InterStatus=u"审批offer信息")|Q(resume__Status=u"审批offer信息",InterviewProcess=u"三面",InterStatus=u"审批offer信息")|Q(resume__Status=u"发邮件",InterviewProcess=u"二面",InterStatus=u"发邮件")|Q(resume__Status=u"发邮件",InterviewProcess=u"三面",InterStatus=u"发邮件")).filter(Q(NextUser=user_id,resume__Agency=None)|Q(resume__Agency=user_id)).filter(lockuser=F('resume__UserID')).filter(Active=1).filter(Turn=F('resume__Turn'))
        length=len(inters)+len(inters2)
        #待抢占的简历(特殊4)
        seizes=[]
        intes=[]
        Seizes = user.Interview_NextUser.filter(Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"发邀请函")|Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"发邀请函")).filter(Active=1).filter(Turn=F('resume__Turn'))
        if Seizes:
            for seize in Seizes: 
                inter2s = seize.NextUser.all() 
                
                if len(inter2s) > 1:
                    intes = Interview.objects.filter(id=seize.id).filter(Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"发邀请函")|Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"发邀请函")).filter(Active=1).filter(Turn=F('resume__Turn'))
                    for inte in intes:
                        pass
                    if inte:
                        seizes.append(inte)
        seizelength=len(seizes)
        #总待办事项
        Task = length
        #Task=0
        
        #待入职人员(特殊5)
        staffs = Resume.objects.filter(Status=u"发offer")
        stalength=len(staffs)
        #待下载的简历(特殊8)
        downresumes = []
        downresumes = import_ID.objects.filter(Status = 0)
        downrelength=len(downresumes)
        power_numb='0'
        if 1 in Powers:
            Task += amount
            power_numb += '1'
        if 2 in Powers and 1 not in Powers:
            Task += amount
            power_numb += '2'
        if 4 in Powers:
            Task += seizelength
            power_numb += '4'
        if 5 in Powers:
            Task += stalength
            power_numb += '5'
        if 7 in Powers:
            Task += publishing
            power_numb += '7'
        if 8 in Powers:
            Task += downrelength
            power_numb += '8'
        if 9 in Powers:
            Task += num
            power_numb += '9'
        {'length':length,'publishing':publishing,'downrelength':downrelength,'seizelength':seizelength,'amount':amount,'Task':Task,'stalength':stalength,'num':num }        
        str_resp = ';'.join([power_numb,str(length),str(publishing),str(downrelength),str(seizelength),str(amount),str(Task),str(stalength),str(num)])    
       
        return HttpResponse(str_resp)

@login_required    
def index(request):
    renli=False
    #secondrule=False
    #cookie
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    #用户所在部门发布的职位

    departs=get_depart(user)
    departpositions = []
    temp = []
    for depart in departs:
        departposition=Position.objects.filter(Q(Depart=depart.id)|Q(SecondDepartment=depart.id)).filter(Filing=0)
        departpositions=list(set(departposition).union(set(departpositions)))
    #特殊处理
    Powers=[]
    powers=Cor_user_Power.objects.filter(UserID=user_id)
    for power in powers:
        Powers.append(power.PowerID.id)
    #待招聘的岗位(特殊9)
    roles=get_role(user)
    num=0
    pos=[]
    for role in roles:
        if role.name == "招聘专员":
           department=role.DepartmentID
           pos=Position.objects.filter(Q(Depart=department)|Q(SecondDepartment=department)).filter(Filing = 0)
           num=len(pos)
           break
        else:
           pos=Position.objects.filter(UserID=user_id).filter(Filing=0)
           num=len(pos)
           break
    
    #招聘中的职位
    positions=Position.objects.filter(UserID=user_id).filter(Filing=0)
    #待处理的职位(审批、申请权  1or2)
    handlepositions=Position.objects.filter(Approver=user_id,Filing=2)
    amount=len(handlepositions)
    #待发布的职位(特殊7)
    publishing_positions=Position.objects.filter(Filing=4)
    publishing=len(publishing_positions)
    #待处理的面试(面试权6)
    inters1 = Resume.objects.filter(Status=u"未处理")
    inters = inters1.filter(Q(UserID=user_id,Agency=None)|Q(Agency=user_id))
    inters2 = Interview.objects.filter(Q(resume__Status=u"一面",InterviewProcess=u"电话面试",InterStatus=u"通过")|Q(resume__Status=u"一面",InterviewProcess=u"电话面试",InterStatus=u"发邀请函") | Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"通过")| Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"发邀请函")| Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"通过")| Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"发邀请函")|Q(resume__Status=u"填写offer信息",InterviewProcess=u"二面",InterStatus=u"填写offer信息")|Q(resume__Status=u"填写offer信息",InterviewProcess=u"三面",InterStatus=u"填写offer信息")|Q(resume__Status=u"审批offer信息",InterviewProcess=u"二面",InterStatus=u"审批offer信息")|Q(resume__Status=u"审批offer信息",InterviewProcess=u"三面",InterStatus=u"审批offer信息")|Q(resume__Status=u"发邮件",InterviewProcess=u"二面",InterStatus=u"发邮件")|Q(resume__Status=u"发邮件",InterviewProcess=u"三面",InterStatus=u"发邮件")).filter(Q(NextUser=user_id,resume__Agency=None)|Q(resume__Agency=user_id)).filter(lockuser=F('resume__UserID')).filter(Active=1).filter(Turn=F('resume__Turn'))
    length=len(inters)+len(inters2)
    #待抢占的简历(特殊4)
    seizes=[]
    intes=[]
    Seizes = user.Interview_NextUser.filter(Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"发邀请函")|Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"发邀请函")).filter(Active=1).filter(Turn=F('resume__Turn'))
    if Seizes:
        for seize in Seizes: 
            inter2s = seize.NextUser.all() 
            
            if len(inter2s) > 1:
                intes = Interview.objects.filter(id=seize.id).filter(Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"发邀请函")|Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"发邀请函")).filter(Active=1).filter(Turn=F('resume__Turn'))
                for inte in intes:
                    pass
                if inte:
                    seizes.append(inte)
    seizelength=len(seizes)
    #总待办事项
    Task = length
    #Task=0
    
    #待入职人员(特殊5)
    staffs = Resume.objects.filter(Status=u"发offer")
    stalength=len(staffs)
    #待下载的简历(特殊8)
    downresumes = []
    downresumes = import_ID.objects.filter(Status = 0) 
    downrelength=len(downresumes)
    if 1 in Powers:
        Task += amount
    if 2 in Powers and 1 not in Powers:
        Task += amount
    if 4 in Powers:
        Task += seizelength
    if 5 in Powers:
        Task += stalength
    if 7 in Powers:
        Task += publishing
    if 8 in Powers:
        Task += downrelength
    if 9 in Powers:
        Task += num
    #岗位时间到归档
    inspectiontime()
    t = loader.get_template("index.html")
    c = Context({'departpositions':departpositions,'Powers':Powers,'member' : user,'positions':positions,'pos':pos,'publishing':publishing,'downrelength':downrelength,'length':length,'seizelength':seizelength,'amount':amount,'Task':Task,'stalength':stalength,'num':num})
    return HttpResponse(t.render(c))

def add():
    with codecs.open(r'/home/resume/project/media/TMP/station_name.js', 'r', 'UTF-8') as file:
                            content = file.read()
    with codecs.open(r'/home/resume/project/media/TMP/favorite_name.js', 'r', 'UTF-8') as file:
                            content1 = file.read()
    Pos = content.find("'@")
    Pos1 = content1.find("'@")
    pos = content.find("';")
    pos1 = content1.find("';")
    users = MyUser.objects.all()
    cor1s=Cor_role_user_depart.objects.filter(RoleID__name__contains=u"总裁")
    cor2s=Cor_role_user_depart.objects.filter(RoleID__name__contains=u"总经理")
    cor3s=Cor_role_user_depart.objects.filter(Q(RoleID__name=u"经理")|Q(RoleID__name=u"副经理"))
    cor4s=Cor_role_user_depart.objects.filter(RoleID__name=u"招聘专员")
    cor5s=Cor_role_user_depart.objects.filter(RoleID__name=u"人力助理")
    nams = "'"
    num=0
    for cor1 in cor1s:
        a = "@1"
        r = slugify(cor1.UserID.username)
        strnum=str(num)
        nam = "|".join([a+r,cor1.UserID.username,strnum])
        nams += nam
        num += 1
    for cor2 in cor2s:
        a = "@2"
        r = slugify(cor2.UserID.username)
        strnum=str(num)
        nam = "|".join([a+r,cor2.UserID.username,strnum])
        nams += nam
        num += 1
    for cor3 in cor3s:
        a = "@3"
        r = slugify(cor3.UserID.username)
        strnum=str(num)
        nam = "|".join([a+r,cor3.UserID.username,strnum])
        nams += nam
        num += 1
    for cor4 in cor4s:
        a = "@4"
        r = slugify(cor4.UserID.username)
        strnum=str(num)
        nam = "|".join([a+r,cor4.UserID.username,strnum])
        nams += nam
        num += 1
    for cor5 in cor5s:
        a = "@5"
        r = slugify(cor5.UserID.username)
        strnum=str(num)
        nam = "|".join([a+r,cor5.UserID.username,strnum])
        nams += nam
        num += 1
    content = content[:Pos] + nams + content[pos:]
    nam1s="'"
    num1=0
    a1="@"
    for user in users:
        r1 = slugify(user.username)
        strnum1=str(num1)
        nam1 = "|".join([a1+r1,user.username,strnum1])
        nam1s += nam1
        num1 += 1
    content1 = content1[:Pos1] + nam1s + content1[pos1:]
    with codecs.open(r'/home/resume/project/media/TMP/station_name.js', 'w', 'UTF-8') as f:
                              f.write(content)
    with codecs.open(r'/home/resume/project/media/TMP/favorite_name.js', 'w', 'UTF-8') as f:
                              f.write(content1)

@login_required
def changepwd(request):  
    if request.method == 'GET':  
        form = ChangepwdForm()  
        return render_to_response('changepwd.html', RequestContext(request, {'form': form,}))
    else:  
        form = ChangepwdForm(request.POST)  
        if form.is_valid():  
            username = request.user.username  
            oldpassword = request.POST.get('oldpassword', '')  
            user = auth.authenticate(username=username, password=oldpassword)  
            if user is not None and user.is_active:  
                newpassword = request.POST.get('newpassword1', '')  
                user.set_password(newpassword)  
                user.save()  
                return render_to_response('login.html', RequestContext(request,{'changepwd_success':True}))
            else:  
                return render_to_response('changepwd.html', RequestContext(request, {'form': form,'oldpassword_is_wrong':True}))
        else:  
            return render_to_response('changepwd.html', RequestContext(request, {'form': form,}))

def forget_changepwd(request):
    time=request.GET.get('t')
    mail=request.GET.get('mail')
    user = MyUser.objects.get(email=mail) 
    fail="none"
    errors=[]
    if time==user.forget_time:
        pass
    else:
        fail="fail"
        return render_to_response('forget_changepwd.html', RequestContext(request, {'fail':fail}))
      
    if request.method == 'POST':
        newpassword1 = request.POST.get('newpassword1','')
        newpassword2 = request.POST.get('newpassword2','')
        if newpassword1 == '':
            errors.append("密码不能为空！")
            return render_to_response('forget_changepwd.html', RequestContext(request, {'errors':errors}))
        if newpassword1 == newpassword2: 
            user.set_password(newpassword1) 
            user.forget_time=random.randrange(0,1000001)
            user.save()
            return HttpResponseRedirect("/")
        else:
            errors.append("两次密码不一致！请重新输入。")
            return render_to_response('forget_changepwd.html', RequestContext(request, {'errors':errors}))
       
    return render_to_response('forget_changepwd.html', RequestContext(request, {'fail':fail}))
@login_required
def change_account(request):
    errors= []
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    username = user.username
    email = user.email
    mobile = user.mobile
    rule = None
    if request.method == 'POST':
        username = request.POST.get('account')
        if len(username) == 0:
            errors.append('请输入用户名')
        else:
            temp_user3 = MyUser.objects.filter(username=username)
            if len(temp_user3) != 0 and username != user.username:
                errors.append('该用户名已注册')

        email = request.POST.get('email')
        if len(email) == 0: 
            errors.append('请输入邮箱')
        else:
            temp_user1 = MyUser.objects.filter(email=email)
            if len(temp_user1) != 0 and email != user.email:
                errors.append('该邮箱已注册')

        mobile = request.POST.get('mobile')
        if len(mobile) == 0:
            errors.append('请输入手机号')
        else:
            temp_user2 = MyUser.objects.filter(mobile=mobile)
            if len(temp_user2) != 0 and mobile != user.mobile:
                errors.append('该手机号已注册')

        #if not request.POST.get('rule'):
            #errors.append('请选择职位')
        #else:
            #rule = request.POST.get('rule')
	rule=None
        if len(username) != 0  and len(email) != 0 and len(mobile) != 0:
            user.username = username
            user.email = email
            user.mobile = mobile
            user.rule = rule
            user.save()
            add()
            return render_to_response('change_account_done.html',RequestContext(request,{'change_account_success':True,}))
        else:
            return render_to_response('change_account.html',RequestContext(request,{'errors': errors,'username':username,'email':email,'mobile':mobile}))
    else:
        return render_to_response('change_account.html',RequestContext(request,{'username':username,'email':email,'mobile':mobile}))


def forget_password(request):
    UserModel = get_user_model()
    good="none"
    
    if request.method == 'POST':
        mail = request.POST.get('email','')
        users = MyUser.objects.filter(email=mail)
        for user in users:
            pass
        if len(users):
            user.forget_time=time.time() 
            user.save()
            mail_password(mail,user.username,user.forget_time)
            good="good"
            return render_to_response('forget_password.html',RequestContext(request,{'good':good,'mail':mail}))
        else:
            good="bad"
            return render_to_response('forget_password.html',RequestContext(request,{'good':good}))
    
    
    return render_to_response('forget_password.html',RequestContext(request,{'good':good}))
    
def mail_password(email,username,time):
    subject="找回密码"
    from_email="si_zhaopin@nantian.com.cn"
    recipient_list=[]
    if email=='':
        recipient_list=['fengyan@nantian.com.cn']
    else:
        recipient_list.append(email)
    auth_password='sizhaopin123456'
    text_content = '找回密码'
    t=loader.get_template("mail_password.html")
    c=Context({'username':username,'time':time,'email':email})
    html_content = t.render(c)
    connection =mail.get_connection(username=from_email,password=auth_password,fail_silently=False)
    msg = EmailMultiAlternatives(subject, text_content,from_email, recipient_list,connection=connection)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
         
def test(request):
    return render_to_response('test.html')
