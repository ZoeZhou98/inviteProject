#-*- encoding: utf-8 -*-
"""
Created on Aug 30 2015

@author: fengyan
last change 02 03 2016
"""
from django.shortcuts import render
from django.template import loader,Context,RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from side.form import InterviewForm,EntryForm,InvitationForm,ChangeRecordForm
from resume.form import Mail_OfferForm
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.shortcuts import render_to_response
from side.models import Interview,Entry,ChangeRecord,Invitation,EmailRecord,HandleRecord
from accounts.models import MyUser
from resume.models import Resume,Mail_Offer
from talents.models import Position
from manager.models import Department,Roles,Cor_role_user_depart,Power,Cor_user_Power,Third_project,Customer
from django.utils.timezone import now, timedelta
from django.utils import timezone
from django.core.mail  import  send_mail
from django.db.models import Q,F
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core import mail
from talents.views import * 
import string
import datetime,time
import sys
import base64
import json
import os
reload(sys)
sys.setdefaultencoding( "utf-8" )
    

#未处理的面试
@login_required	
def stucked(request):
    date = datetime.datetime.now()
    #从cookie得到当前登录用户ID及用户对象
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    #数据
    inters1 = Resume.objects.filter(Status=u"未处理")
    Inters = inters1.filter(Q(UserID=user_id,Agency=None)|Q(Agency=user_id))
    inters=[]
    inte2s=[]
    if Inters:
        for inter in Inters:   
            intes = Interview.objects.filter(resume=inter.id)
            for inte in intes:
                change1s=ChangeRecord.objects.filter(interview=inte.id)
                inte2s.append([inte,change1s]) 
            interss = str(inter.id)+"ss"
            interz = "chkSon"+str(inter.id)
            inters.append([inter,inte2s,interss,interz])
            inte2s=[]
    inters2 = Interview.objects.filter(Q(resume__Status=u"一面",InterviewProcess=u"电话面试",InterStatus=u"通过")|Q(resume__Status=u"一面",InterviewProcess=u"电话面试",InterStatus=u"发邀请函") | Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"通过")| Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"发邀请函")| Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"通过")| Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"发邀请函")|Q(resume__Status=u"填写offer信息",InterviewProcess=u"二面",InterStatus=u"填写offer信息")|Q(resume__Status=u"填写offer信息",InterviewProcess=u"三面",InterStatus=u"填写offer信息")|Q(resume__Status=u"审批offer信息",InterviewProcess=u"二面",InterStatus=u"审批offer信息")|Q(resume__Status=u"审批offer信息",InterviewProcess=u"三面",InterStatus=u"审批offer信息")|Q(resume__Status=u"发邮件",InterviewProcess=u"二面",InterStatus=u"发邮件")|Q(resume__Status=u"发邮件",InterviewProcess=u"三面",InterStatus=u"发邮件")).filter(Q(NextUser=user_id,resume__Agency=None)|Q(resume__Agency=user_id)).filter(lockuser=F('resume__UserID')).filter(Active=1).filter(Turn=F('resume__Turn'))
    sides=[] 
    side2s=[]
    if inters2:
        for inter2 in inters2:   
            inters3 = inter2.NextUser.all() 
            if len(inters3) == 1:
                sidess = Interview.objects.filter(resume=inter2.resume.id)
                for side in sidess:
                    changes=ChangeRecord.objects.filter(interview=side.id)
                    side2s.append([side,changes]) 
                inter2ss = str(inter2.resume.id)+"ss"
                inter2rz = "chkSon"+str(inter2.resume.id)
                sides.append([inter2,side2s,inter2rz,inter2ss])
                side2s=[]
    #加载模版（模版由django自动从文件template里查找）
    t = loader.get_template("stucked.html")
    #Context一组字典用于传递数据
    c = Context({'inters':inters,'member':user,'sides':sides,'date':date})
    #t.render(c)通过context调用Template对象的render()方法来填充模板
    #以字符串的形式传递给页面
    return HttpResponse(t.render(c))
#my未处理
@login_required	
def mystucked(request):
    date = datetime.datetime.now()
    #从cookie得到当前登录用户ID及用户对象
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    #数据
    inters1 = Resume.objects.filter(Status=u"未处理").filter(UserID=user_id)
    Inters = inters1.filter(Q(UserID=user_id,Agency=None)|Q(Agency=user_id))
    inters=[]
    inte2s=[]
    if Inters:
        for inter in Inters:   
            intes = Interview.objects.filter(resume=inter.id)
            for inte in intes:
                change1s=ChangeRecord.objects.filter(interview=inte.id)
                inte2s.append([inte,change1s]) 
            interss = str(inter.id)+"ss"
            interz = "chkSon"+str(inter.id)
            inters.append([inter,inte2s,interss,interz])
            inte2s=[]
    inters2 = Interview.objects.filter(Q(resume__Status=u"一面",InterviewProcess=u"电话面试",InterStatus=u"通过")|Q(resume__Status=u"一面",InterviewProcess=u"电话面试",InterStatus=u"发邀请函") | Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"通过")| Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"发邀请函")| Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"通过")| Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"发邀请函")|Q(resume__Status=u"填写offer信息",InterviewProcess=u"二面",InterStatus=u"填写offer信息")|Q(resume__Status=u"填写offer信息",InterviewProcess=u"三面",InterStatus=u"填写offer信息")|Q(resume__Status=u"审批offer信息",InterviewProcess=u"二面",InterStatus=u"审批offer信息")|Q(resume__Status=u"审批offer信息",InterviewProcess=u"三面",InterStatus=u"审批offer信息")|Q(resume__Status=u"发邮件",InterviewProcess=u"二面",InterStatus=u"发邮件")|Q(resume__Status=u"发邮件",InterviewProcess=u"三面",InterStatus=u"发邮件")).filter(lockuser=user_id).filter(Q(NextUser=user_id,resume__Agency=None)|Q(resume__Agency=user_id)).filter(lockuser=F('resume__UserID')).filter(Active=1).filter(Turn=F('resume__Turn'))
    sides=[] 
    side2s=[]
    if inters2:
        for inter2 in inters2:   
            inters3 = inter2.NextUser.all() 
            if len(inters3) == 1:
                sidess = Interview.objects.filter(resume=inter2.resume.id)
                for side in sidess:
                    changes=ChangeRecord.objects.filter(interview=side.id)
                    side2s.append([side,changes]) 
                inter2ss = str(inter2.resume.id)+"ss"
                inter2rz = "chkSon"+str(inter2.resume.id)
                sides.append([inter2,side2s,inter2rz,inter2ss])
                side2s=[]
    #加载模版（模版由django自动从文件template里查找）
    t = loader.get_template("mystucked.html")
    #Context一组字典用于传递数据
    c = Context({'inters':inters,'member':user,'sides':sides,'date':date})
    #t.render(c)通过context调用Template对象的render()方法来填充模板
    #以字符串的形式传递给页面
    return HttpResponse(t.render(c))
#面试流程说明
def exhelp(request):
    return render(request,'exhelp.html')
#我发起的面试
def myresume(request):
    return render(request,'myresume.html')

#邀请函
@login_required	
def invitation(request,interview_id):
    #cookie
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    #身份验证
    exinvit = Interview.objects.filter(Q(resume__Status=u"一面",InterviewProcess=u"电话面试",InterStatus=u"发邀请函") | Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"发邀请函")| Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"发邀请函")).filter(Q(NextUser=user_id,resume__Agency=None)|Q(resume__Agency=user_id)).filter(lockuser=F('resume__UserID')).filter(Active=1).filter(Turn=F('resume__Turn'))
    if len(exinvit):
        pass
    else:
        return HttpResponse("该事项不属于您！")
    #预处理
    email = user.email
    finish="goback"     
    error=""
    inter=[]
    resume=[]
    inters = Interview.objects.filter(id=interview_id)
    for inter in inters:
        pass
    resumes = Resume.objects.filter(id=inter.resume.id)
    for resume in resumes:
        pass
    Imail = resume.CandidateEmail
    #Imail='fengyan@nantian.com.cn'
    users=inter.NextUser.all()    
    if len(users) > 1:
        inter.NextUser.clear()
        inter.NextUser.add(user)
        resume.NextUser.clear()
        resume.NextUser.add(user)
    invits = Invitation.objects.filter(interview=inter.id)
    for invit in invits:
        pass
    if len(invits):
        Imail = invit.Imail
    #POST方式接受数据
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        Imail=request.POST['Imail']
        judge=request.POST['judge']
        if judge==u"跳过":
            handles=HandleRecord.objects.filter(resume=resume.id,interview=inter.id).filter(Type="跳过邀请函").filter(handleuser=user_id)
            if len(handles):
                pass
            else:
                handletime(resume,inter,user,"跳过邀请函",1,None)
            Interview.objects.filter(id=interview_id).update(InterStatus=u"通过")
            finish="goto"
            return render_to_response("invitationform.html",{'form': form,'finish':finish,'Imail':Imail},context_instance=RequestContext(request))
            #return HttpResponseRedirect("/side/stucked")
        #if judge==u"不跳":
            #return render_to_response("invitationform.html",{'form': form,'finish':finish,'Imail':Imail},context_instance=RequestContext(request))
        
        if Imail:
            pass
        else:
            error="候选人邮箱不能为空"
            return render_to_response("invitationform.html",{'form': form,'finish':finish,'error':error,'Imail':Imail},context_instance=RequestContext(request))
             
        if form.is_valid():
            #cleaned_data读取表单返回的值
            cd = form.cleaned_data
            bcc = request.POST['bcc']
            bccmail=[]
            if len(bcc)>0:
                bccss=bcc.split("\r\n")
                for bccs in bccss:
                    if bccs:
                        bccs=bccs.strip()
                        bccmail.append(bccs)
            else:
                bcc = None
            time1=cd['time1']
            time2=cd['time2']
            Itime1=cd['Itime']
            Itime=str(Itime1) + " " + time1+"--"+time2
            new_invita=form.save(commit=False) 
            new_invita.interview=inter
            new_invita.Imail=Imail
            new_invita.Itime=Itime
            new_invita.handleuser=user
            if len(invits):
                new_invita.id=invit.id
            #保存基本信息
            new_invita.save()
            #保存关联信息
            form.save_m2m()
            mails=EmailRecord.objects.filter(resume=resume.id,interview=inter.id,handleuser=user_id,touser=Imail,Type="邀请函邮件",notes="发送成功")
            if len(mails):
                pass
            else:
                if sent_invitation(interview_id,email,bccmail):
                    mailtime(resume,inter,user,Imail,"邀请函邮件",email,bcc,"发送成功")

                    Interview.objects.filter(id=interview_id).update(InterStatus=u"通过")
                    finish="goto"
                    return render_to_response("invitationform.html",{'form': form,'finish':finish,'bcc':bcc,'error':error,'Imail':Imail},context_instance=RequestContext(request))
                else:
                    error="数据已保存,邮件发送失败！"
                    mailtime(resume,inter,user,Imail,"邀请函邮件",email,bcc,"发送失败")
                    return render_to_response("invitationform.html",{'form': form,'finish':finish,'bcc':bcc,'error':error,'finish':finish,'Imail':Imail},context_instance=RequestContext(request))
                        
            finish="goto"
            return render_to_response("invitationform.html",{'form': form,'finish':finish,'error':error,'Imail':Imail},context_instance=RequestContext(request))
            #return HttpResponseRedirect("/side/stucked")
            
        else:
            pass
    else:
        #获得表单对象
        form = InvitationForm() 

    #context_instance=RequestContext(request)防止crsf错误
    return render_to_response("invitationform.html",{'form': form,'finish':finish,'Imail':Imail},context_instance=RequestContext(request))
    
#新的面试
@login_required	
def newinterview(request,resume_id):
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    User = UserModel.objects.get(id = user_id)
    
    finish="goback"     
    nextuers=myuser_res()
    #django对于一对多错误处理解决         
    shows = Resume.objects.filter(id=resume_id)
    for show in shows:
        dis = show.CandidateName
    inters2 = Interview.objects.filter(resume=resume_id).filter(Q(resume__Status=u"一面",InterviewProcess=u"电话面试",InterStatus=u"通过")| Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"通过")| Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"通过")).filter(Q(NextUser=user_id,resume__Agency=None)|Q(resume__Agency=user_id)).filter(lockuser=F('resume__UserID')).filter(Active=1).filter(Turn=F('resume__Turn'))
    resumes=Resume.objects.filter(Status=u"未处理").filter(Q(UserID=user_id,Agency=None)|Q(Agency=user_id)).filter(id=resume_id)
    if len(inters2) or len(resumes):
        pass
    else:
        return HttpResponse("权限不够,无法处理")
    #判断当前面试状态
    Inp = u"未处理"
    if show.Status == u"未处理":
        Inp = u"电话面试"
    elif show.Status == u"一面":
        Inp = u"一面"
    elif show.Status == u"二面":
        Inp = u"二面"
    elif show.Status == u"三面":
        Inp = u"三面"
    #获取招聘岗位可取列表
    station = show.Station
    positions=Position.objects.filter(Filing=0)

    #POST方式接受数据
    if request.method == 'POST':
        #从POST得到表单
        form = InterviewForm(request.POST)
        #从POST得到部分数据
        Status1 = request.POST['Status']
        
        Time = request.POST['Time']        
        station = request.POST['station']        
        #nextusers = request.POST.getlist('NextUser') 
        nextusers = request.POST['NextUser']
        if station == "None" or station == "":
            if Status1 == u"淘汰":
                pass
            else:
                return render_to_response('newinterview.html', {'form': form,'finish':finish,'error3': '招聘岗位不能为空','member': User,'dis': dis,'nextuers':nextuers,'show':show,'Inp':Inp,'station':station,'positions':positions}, context_instance=RequestContext(request))
            #station = None
        else:
            station = string.atoi(station)
        level = 0 
       # Time1 = request.POST['Time']
       # Time1 = datetime.datetime.strptime(Time1,"%Y-%m-%d %H:%M:%S")
       # date = datetime.datetime.now()
       # diff=date-Time1
        interstatus = u"未处理"
        if Status1 == u"":
            return render_to_response('newinterview.html', {'form': form,'finish':finish,'error1':'请选择下一步候选人状态','member': User,'dis': dis,'nextuers':nextuers,'show':show,'Inp':Inp,'station':station,'positions':positions}, context_instance=RequestContext(request)) 
        if Status1 == u"淘汰":
            interstatus = u"淘汰"
        else:
            interstatus = u"通过"
        if Status1 == u"推荐":
            if len(nextusers)==0:
               return render_to_response('newinterview.html', {'form': form,'finish':finish,'error2':'推荐锁定人不能为空','member': User,'dis': dis,'nextuers':nextuers,'show':show,'Inp':Inp,'station':station,'positions':positions}, context_instance=RequestContext(request)) 
        #对于时间输入处理不能小于今天        
       # if abs(diff.days) < 1:
       #     pass
       # else:
       #     return render_to_response('newinterview.html', {'form': form,'error2': '请选择合适的时间','member': User,'dis': dis,'Inp':Inp}, context_instance=RequestContext(request))
        station_sam=Position.objects.get(id=station)
        project=Third_project.objects.get(name=station_sam.ProjectName)
        #form表单验证
        if form.is_valid():
            #cleaned_data读取表单返回的值
            cd = form.cleaned_data
          
            #print cd['InterviewResults']
            #print cd['Level']
            #print cd['Status']
            #print cd['Time']
            
            #不保存到数据库
            new_inter=form.save(commit=False)
            #外键属性以相应对象赋值
            new_inter.resume=show
            new_inter.user=User
            new_inter.InterviewProcess=Inp
            new_inter.lockuser=show.UserID
            if show.Turn:
                pass
            else:
                Resume.objects.filter(pk=resume_id).update(Turn = 1)
            show = Resume.objects.get(id=resume_id)
            new_inter.Turn = show.Turn
            new_inter.Projectname = station_sam.ProjectName   
            if Status1==u"一面" or Status1==u"二面" or Status1==u"三面":
                new_inter.InterStatus=u"发邀请函"
            elif Status1==u"填写offer信息":
                new_inter.InterStatus=u"填写offer信息"
                new_inter.Notes=u"发offer"
            else:    
                new_inter.InterStatus=interstatus
                
            if show.Agency:
                new_inter.Agency=show.Agency
                
            #保存基本信息
            new_inter.save()
            #保存关联信息
            form.save_m2m()
            #若选择淘汰处理人为锁定人
            #user_1 = UserModel.objects.get(id = 1)
            new_inter.NextUser.clear()
            if Status1==u"一面":
                new_inter.NextUser.add(project.recruiter)
            if Status1==u"二面":
                new_inter.NextUser.add(project.customer.customer_manager)
            if Status1==u"三面":
                boss1=get_boss1(project.customer.depart)
                new_inter.NextUser.add(boss1)
            if Status1==u"填写offer信息":
                new_inter.NextUser.add(project.customer.customer_manager) 
           #if Status1 ==u"二面":
           #     new_inter.NextUser.clear()
           #     new_inter.NextUser.add(user_1)
            inter2s = Interview.objects.filter(resume=resume_id).filter(InterviewProcess=Inp).filter(Active=1).filter(Turn=F('resume__Turn'))
            for inter2 in inter2s:
                pass
            inter2_id = str(inter2.id)
            #其他表单的数据更新
            inters = Interview.objects.filter(resume=resume_id).filter(Active=1).filter(Turn=F('resume__Turn'))
            for inter in inters:
               levels = inter.Level
               level += levels
            level = level/(len(inters))
            Resume.objects.filter(pk=resume_id).update(Level = level)
            if Status1==u"淘汰" or Status1==u"推荐": 
                pass
            else:
                Resume.objects.filter(pk=resume_id).update(Status = (cd['Status']))
            Resume.objects.filter(pk=resume_id).update(Station = station)
            if show.Agency:
                Resume.objects.filter(pk=resume_id).update(Agency=None)
            show.NextUser.clear()
            for reuser in inter2.NextUser.all():

                show.NextUser.add(reuser)
            if Status1==u"淘汰" or Status1==u"推荐":
                if Status1==u"淘汰":
                    new_inter.NextUser.add(show.UserID)
                    Resume.objects.filter(pk=resume_id).update(UserID = None)
                    Resume.objects.filter(pk=resume_id).update(Status = u"未处理")
                    Resume.objects.filter(pk=resume_id).update(Station = None)
                    Resume.objects.filter(pk=resume_id).update(LockTime=None)
                if Status1==u"推荐":
                    new_inter.NextUser.add(show.UserID)
                    Resume.objects.filter(pk=resume_id).update(UserID = nextusers)
                    Resume.objects.filter(pk=resume_id).update(Status = u"未处理")
                if show.Turn:
                    turn = show.Turn + 1
                    Resume.objects.filter(pk=resume_id).update(Turn = turn)
                else:
                    Resume.objects.filter(pk=resume_id).update(Turn = 1)
            '''
            #废弃
            if Status1==u"一面":
                if show.Agency:
                    pass
                else:
                    finish="goto"
                    return render_to_response("newinterview.html",{'form': form,'finish':finish,'member': User,'dis': dis,'show':show,'Inp':Inp,'nextuers':nextuers,'station':station,'positions':positions},context_instance=RequestContext(request))
                    #return HttpResponseRedirect("/side/invitation/"+inter2_id)                
           
            if Status1==u"填写offer信息":
                if show.Agency:
                    pass
                else:
                    finish="goto"
                    #return HttpResponseRedirect("/side/offer/"+inter2_id)
                    return render_to_response("newinterview.html",{'form': form,'finish':finish,'member': User,'dis': dis,'show':show,'Inp':Inp,'nextuers':nextuers,'station':station,'positions':positions},context_instance=RequestContext(request))
            '''
            #跳转
            finish="goto"
            return render_to_response("newinterview.html",{'form': form,'finish':finish,'member': User,'dis': dis,'show':show,'Inp':Inp,'nextuers':nextuers,'station':station,'positions':positions},context_instance=RequestContext(request))
            #return HttpResponseRedirect("/side/stucked")
        else:
            error1="请选择下一步候选人状态"
            return render_to_response('newinterview.html', {'form': form,'finish':finish,'member': User,'dis': dis,'nextuers':nextuers,'show':show,'Inp':Inp,'station':station,'positions':positions,'error1':error1}, context_instance=RequestContext(request)) 
            
    else:
        #获得表单对象
        form = InterviewForm() 

    #context_instance=RequestContext(request)防止crsf错误
    return render_to_response("newinterview.html",{'form': form,'finish':finish,'member': User,'dis': dis,'show':show,'Inp':Inp,'nextuers':nextuers,'station':station,'positions':positions},context_instance=RequestContext(request))
#追回
@login_required 
def recover(request,interview_id):
    #从cookie得到当前登录用户ID及用户对象
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    #数据
    finish="goback"     
    #填写offer信息暂时无效
    inter = Interview.objects.filter(id = interview_id).filter(user=user_id).filter(Active=1).filter(Q(resume__Status=u"一面",InterviewProcess=u"电话面试",InterStatus=u"发邀请函") | Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"发邀请函") | Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"发邀请函")|Q(resume__Status=u"填写offer信息",InterviewProcess=u"二面",InterStatus=u"填写offer信息")|Q(resume__Status=u"填写offer信息",InterviewProcess=u"三面",InterStatus=u"填写offer信息")).filter(Active=1).filter(Turn=F('resume__Turn'))
    for inte in inter:
        pass
    if inter:
        pass
    else:
        error="对不起！该事项不能追回"
        #finish="goto"
        #return render_to_response("recover.html",{'error': error},context_instance=RequestContext(request))
        return HttpResponse(error)
    if request.method == 'POST':
        form = ChangeRecordForm(request.POST)    
        
        if form.is_valid():
            #cleaned_data读取表单返回的值
            cd = form.cleaned_data
            recover=form.save(commit=False) 
            recover.interview=inte
            #保存基本信息
            recover.save()
            #保存关联信息
            form.save_m2m()
            Interview.objects.filter(pk=interview_id).update(Active = 0)
            if inte.resume.Status==u"三面" and inte.InterStatus==u"发邀请函" : 
                Resume.objects.filter(pk=inte.resume.id).update(Status = u"二面")
            if inte.resume.Status==u"二面" and inte.InterStatus==u"发邀请函" : 
                Resume.objects.filter(pk=inte.resume.id).update(Status = u"一面")
            if inte.resume.Status==u"一面" and inte.InterStatus==u"发邀请函" : 
                Resume.objects.filter(pk=inte.resume.id).update(Status = u"未处理")
            #暂时无用
            if inte.resume.Status==u"填写offer信息": 
                Resume.objects.filter(pk=inte.resume.id).update(Status = inte.InterviewProcess)
            #跳转
            finish="goto"
            return render_to_response("recover.html",{'finish':finish,'username':user.username,'form': form},context_instance=RequestContext(request))
            #return HttpResponseRedirect("/side/stucked")
            
        else:
            pass
    else:
        #获得表单对象
        form = ChangeRecordForm() 

    #context_instance=RequestContext(request)防止crsf错误
    return render_to_response("recover.html",{'form': form,'finish':finish,'username':user.username},context_instance=RequestContext(request))
#退回
def retreat(request,interview_id):
    #从cookie得到当前登录用户ID及用户对象
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    #数据
    finish="goback"     
    inter = Interview.objects.filter(id = interview_id).filter(NextUser=user_id).filter(Active=1).filter(Turn=F('resume__Turn'))
    for inte in inter:
        pass
    if inter:
        pass
    else:
        error="权限不够不能退回"
        #return render_to_response("retreat.html",{'error': error},context_instance=RequestContext(request))
        return HttpResponse(error)
    if request.method == 'POST':
        form = ChangeRecordForm(request.POST)
        ctype  = request.POST['Ctype']    
        if form.is_valid():
            #cleaned_data读取表单返回的值
            cd = form.cleaned_data
            retreat=form.save(commit=False) 
            retreat.interview=inte
            #保存基本信息
            retreat.save()
            #保存关联信息
            form.save_m2m()
            if  ctype==u"退回上一步": 
                Interview.objects.filter(pk=interview_id).update(Active = 0)
                if inte.resume.Status==u"三面": 
                    Resume.objects.filter(pk=inte.resume.id).update(Status = u"二面")
                if inte.resume.Status==u"二面": 
                    Resume.objects.filter(pk=inte.resume.id).update(Status = u"一面")
                if inte.resume.Status==u"一面": 
                    Resume.objects.filter(pk=inte.resume.id).update(Status = u"未处理")
                #if inte.resume.Status==u"填写offer信息": 
                 #   Resume.objects.filter(pk=inte.resume.id).update(Status = u"二面")
            if ctype ==u"退回开始":
                Interview.objects.filter(resume=inte.resume.id).update(Active = 0)
                Resume.objects.filter(pk=inte.resume.id).update(Status = u"未处理")
                
            #跳转
            finish="goto"
            return render_to_response("retreat.html",{'form': form,'finish':finish,'username':user.username},context_instance=RequestContext(request))
            #return HttpResponseRedirect("/side/stucked")
            
        else:
            pass
    else:
        #获得表单对象
        form = ChangeRecordForm() 

    #context_instance=RequestContext(request)防止crsf错误
    return render_to_response("retreat.html",{'form': form,'finish':finish,'username':user.username},context_instance=RequestContext(request))
#处理过的面试
def worked(request):
    #从cookie得到当前登录用户ID及用户对象
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    #数据
    inters=[]
    Inter1s = ChangeRecord.objects.filter(Ctype=u"审批offer信息").filter(Cname=user.username).exclude(Cname=F('interview__user__username')).order_by("-id")
    if Inter1s:
        for Inter1 in Inter1s:
            inter=Interview.objects.get(id=Inter1.interview.id)
            changes=ChangeRecord.objects.filter(interview=inter.id)
            interss = str(inter.id)+"ss"
            inters.append([inter,changes,interss])
    Inters = Interview.objects.filter(user=user_id).order_by("-id")
    if Inters:
        for inter in Inters:
            changes=ChangeRecord.objects.filter(interview=inter.id)
            interss = str(inter.id)+"ss"
            inters.append([inter,changes,interss])
        
    #分页
    if not request.GET.get('page_size'):
        page_size = 15 
    else:
        page_size = int(request.GET.get('page_size'))
    paginator=Paginator(inters,page_size)
    page_num=request.GET.get('page')
    try:
        inters=paginator.page(page_num)
    except PageNotAnInteger:
        inters=paginator.page(1)
    except EmptyPage:
        inters=paginator.page(paginator.num_pages)
    paging = inters
    page_right = page_size * paging.number if (page_size * paging.number < len(Inters)) else len(Inters)
    page_left = page_size * (paging.number - 1) + 1 if (paging.number - 1) > 0 else 1
    #context_instance=RequestContext(request)防止crsf错误
    #加载模版（模版由django自动从文件template里查找）
    t = loader.get_template("worked.html")
    #Context一组字典用于传递数据
    c = Context({'localuser':user,'inters':inters,'paging':paging,'page_size':page_size,'page_left':page_left,'page_right':page_right})
    #t.render(c)通过context调用Template对象的render()方法来填充模板
    #以字符串的形式传递给页面
    return HttpResponse(t.render(c))
#处理过的面试搜索
def worked_search(request):
    if 'PName' in request.GET and request.GET['PName']: 
        q1 = ''
        q1=request.GET['PName']
        #从cookie得到当前登录用户ID及用户对象
        UserModel = get_user_model()
        session_id = request.COOKIES['sessionid']
        user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
        user = UserModel.objects.get(id = user_id)
        #数据
        inters=[]
        Inter1s = ChangeRecord.objects.filter(Q(interview__resume__CandidateName__icontains=q1)|Q(Ctime__contains=q1)|Q(Cname__icontains=q1)|Q(Cnotes__icontains=q1)|Q(Ctype__icontains=q1)|Q(Creason__icontains=q1)).filter(Ctype=u"审批offer信息").filter(Cname=user.username).exclude(Cname=F('interview__user__username')).order_by("-id")
        if Inter1s:
            for Inter1 in Inter1s:
                inter=Interview.objects.get(id=Inter1.interview.id)
                changes=ChangeRecord.objects.filter(interview=inter.id)
                interss = str(inter.id)+"ss"
                inters.append([inter,changes,interss])
        Inters = Interview.objects.filter(Q(resume__CandidateName__icontains=q1)|Q(resume__Station__PositionName__icontains=q1)|Q(user__username__icontains=q1)|Q(InterviewResults__icontains=q1)|Q(Time__contains=q1)|Q(Level__icontains=q1)|Q(InterviewProcess__icontains=q1)|Q(lockuser__username__icontains=q1)|Q(InterStatus__icontains=q1)|Q(Notes__icontains=q1)|Q(Agency__username__icontains=q1)|Q(NextUser__username__icontains=q1)).filter(user=user_id).order_by("-id")
        if Inters:
            for inter in Inters:
                changes=ChangeRecord.objects.filter(interview=inter.id)
                interss = str(inter.id)+"ss"
                inters.append([inter,changes,interss])
        
        #分页
        if not request.GET.get('page_size'):
            page_size = 15 
        else:
            page_size = int(request.GET.get('page_size'))
        paginator=Paginator(inters,page_size)
        page_num=request.GET.get('page')
        try:
            inters=paginator.page(page_num)
        except PageNotAnInteger:
            inters=paginator.page(1)
        except EmptyPage:
            inters=paginator.page(paginator.num_pages)
        paging = inters
        page_right = page_size * paging.number if (page_size * paging.number < len(Inters)) else len(Inters)
        page_left = page_size * (paging.number - 1) + 1 if (paging.number - 1) > 0 else 1
        #context_instance=RequestContext(request)防止crsf错误
        #加载模版（模版由django自动从文件template里查找）
        t = loader.get_template("worked.html")
        #Context一组字典用于传递数据
        c = Context({'inters':inters,'paging':paging,'page_size':page_size,'page_left':page_left,'page_right':page_right})
        #t.render(c)通过context调用Template对象的render()方法来填充模板
        #以字符串的形式传递给页面
        return HttpResponse(t.render(c))
    else:
        return render_to_response("worked.html")
#需要抢占的简历
#代码可优化
#废弃
@login_required 
def seize(request):
    #从cookie得到当前登录用户ID及用户对象
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    #数据
    inters2 = user.Interview_NextUser.filter(Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"发邀请函")|Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"发邀请函")).filter(Active=1).filter(Turn=F('resume__Turn'))
    #inters2 = Interview.objects.filter(Q(resume__Status=u"一面",InterviewProcess=u"电话面试") | Q(resume__Status=u"二面",InterviewProcess=u"一面")| Q(resume__Status=u"三面",InterviewProcess=u"二面")|Q(InterStatus=u"发邮件中")).filter(Q(NextUser=user_id,resume__Agency=None)|Q(resume__Agency=user_id)).filter(lockuser=F('resume__UserID'))
    sides=[] 
    if inters2:
        for inter2 in inters2: 
            inters = inter2.NextUser.all() 
            
            if len(inters) > 1:
                inte = Interview.objects.filter(id=inter2.id).filter(Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"发邀请函")|Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"发邀请函")).filter(Active=1).filter(Turn=F('resume__Turn'))
                for inter in inte:
                    pass
                if inter:
                    side1 = Interview.objects.filter(resume=inter.resume.id)
                    interss = str(inter.resume.id)+"ss"
                    sides.append([inter,side1,interss])
    #加载模版（模版由django自动从文件template里查找）
    t = loader.get_template("seize.html")
    #Context一组字典用于传递数据
    c = Context({'member':user,'sides':sides})
    #t.render(c)通过context调用Template对象的render()方法来填充模板
    #以字符串的形式传递给页面
    return HttpResponse(t.render(c))
#填写offer信息
def offer(request,interview_id):
    #从cookie得到当前登录用户ID及用户对象
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    #数据
    inter = Interview.objects.filter(id = interview_id).filter(resume__Status=u"填写offer信息",InterStatus=u"填写offer信息").filter(NextUser=user_id).filter(Active=1).filter(Turn=F('resume__Turn'))
    for inte in inter:
        pass
    if inter:
        pass
    else:
        error="对不起！权限不够"
        return HttpResponse(error)
    
    finish="goback"     
    inter = Interview.objects.filter(id = interview_id).filter(Active=1)
    for inte in inter:
        pass
    offers = Mail_Offer.objects.filter(resume = inte.resume.id) 
    for offer in offers:
        pass
    shows = Resume.objects.filter(id=inte.resume.id)
    for show in shows:
        dis = show.CandidateName
    boss=get_boss(user)
    fridepart=get_fridepart(boss)
    num=1
    need1=0
    #positions=Position.objects.filter(Q(Depart=fridepart.id)|Q(SecondDepartment=fridepart.id)).filter(Filing=0)
    positions=Position.objects.filter(Filing=0)
    for position1 in positions:
        if num==1:
           need1=position1.NeedPersonNum-position1.recruitednum 
           break
    Ename = show.CandidateName
    Ephone = show.CandidatePhone
    Email = show.CandidateEmail
    Ejob = show.Station
    Ejob_name = None
    Eprojects = Third_project.objects.all()
    #POST方式接受数据
    if request.method == 'POST':
        form = Mail_OfferForm(request.POST)
        Ename = request.POST.get('Ename','')
        Ephone = request.POST.get('Ephone','')
        Email = request.POST.get('Email','')
        Ejob = request.POST.get('Ejob','')
        Eproject = request.POST.get('Eproject','')
        if Ejob:
            position=Position.objects.get(id=Ejob)
            Ejob_name=position.PositionName
        else:
            Ejob_name=None

        if form.is_valid():
            #cleaned_data读取表单返回的值
            cd = form.cleaned_data
            new_offer=form.save(commit=False) 
            new_offer.resume=show
            new_offer.Ename=Ename
            new_offer.Ephone=Ephone
            new_offer.Email=Email
            new_offer.Ejob=Ejob_name
            new_offer.handleuser=user
            if len(offers):
                new_offer.id=offer.id
            #保存基本信息
            new_offer.save()
            #保存关联信息
            form.save_m2m()
            Resume.objects.filter(pk=show.id).update(Status = u"审批offer信息")
            Resume.objects.filter(pk=show.id).update(Station = Ejob)
            Interview.objects.filter(id=interview_id).update(InterStatus=u"审批offer信息")
            inte.NextUser.clear()
            
            inte.NextUser.add(boss)
            #if show.Agency:
                #Resume.objects.filter(pk=resume_id).update(Agency=None)
            finish="goto"     
            return render_to_response("offer.html",{'form': form,'finish':finish,'Ename':Ename,'Ephone':Ephone,'Email':Email,'Ejob':Ejob,'Eproject':Eproject,'positions':positions},context_instance=RequestContext(request))
            #return HttpResponseRedirect("/side/stucked")
        else:
            pass
    else:
        #获得表单对象
        form = Mail_OfferForm() 

    #context_instance=RequestContext(request)防止crsf错误
    return render_to_response("offer.html",{'form': form,'finish':finish,'Ename':Ename,'Ephone':Ephone,'Email':Email,'Ejob':Ejob,'Eprojects':Eprojects,'positions':positions,'need1':need1},context_instance=RequestContext(request))
#查看offer信息
def lookoffer(request,interview_id):
    #从cookie得到当前登录用户ID及用户对象 
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    #数据
    inter = Interview.objects.filter(id = interview_id).filter(Q(user=user_id)|Q(NextUser=user_id))
    for inte in inter:
        pass
    if inter:
        pass
    else:
        error="对不起！权限不够"
        return HttpResponse(error)
    
    offers = Mail_Offer.objects.filter(resume = inte.resume.id)
    for offer in offers:
        pass
    return render_to_response("lookoffer.html",{'offer':offer},context_instance=RequestContext(request))
    
#审批offer信息
def exoffer(request,interview_id):
     #从cookie得到当前登录用户ID及用户对象
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    finish="goback"     
    
    #数据
    inter = Interview.objects.filter(id = interview_id).filter(resume__Status=u"审批offer信息",InterStatus=u"审批offer信息").filter(NextUser=user_id).filter(Active=1).filter(Turn=F('resume__Turn'))
    for inte in inter:
        pass
    if inter:
        pass
    else:
        error="对不起！权限不够"
        return HttpResponse(error)
        #return render_to_response("exoffer.html",{'error': error},context_instance=RequestContext(request))
    offers = Mail_Offer.objects.filter(resume = inte.resume.id) 
    for offer in offers:
        pass
    inter_id = str(inte.id)
    if request.method == 'POST':
        form = ChangeRecordForm(request.POST)    
        judge = request.POST.get('judge','')
        
            
            
        if form.is_valid():
            #cleaned_data读取表单返回的值
            cd = form.cleaned_data
            exoffer=form.save(commit=False) 
            exoffer.interview=inte
            if judge==u"同意":
                exoffer.Cnotes=u"同意"
            if judge==u"不同意":
                exoffer.Cnotes=u"不同意"
            #保存基本信息
            exoffer.save()
            #保存关联信息
            form.save_m2m()
            if judge==u"同意":
                Resume.objects.filter(pk=inte.resume.id).update(Status = u"发邮件")
                Interview.objects.filter(id=interview_id).update(InterStatus=u"发邮件")
                finish="goto"     
                return render_to_response("exoffer.html",{'form': form,'finish':finish,'username':user.username,'offer':offer},context_instance=RequestContext(request))
                
                #return HttpResponseRedirect("/side/sent_omail/"+inte_id)
            if judge==u"不同意":
                Resume.objects.filter(pk=inte.resume.id).update(Status = u"淘汰")
                Interview.objects.filter(id=interview_id).update(InterStatus=u"通过")
                Interview.objects.filter(id=interview_id).update(Notes=None)
                finish="goto"     
                return render_to_response("exoffer.html",{'form': form,'finish':finish,'username':user.username,'offer':offer},context_instance=RequestContext(request))
                #return HttpResponseRedirect("/side/stucked")
        
        else:
            pass
    else:
        #获得表单对象
        form = ChangeRecordForm() 

    #context_instance=RequestContext(request)防止crsf错误

    return render_to_response("exoffer.html",{'form': form,'finish':finish,'username':user.username,'offer':offer},context_instance=RequestContext(request))
#邀请函邮件
def sent_invitation(interview_id,email,bcc):   
    fmail=Email.objects.get(mail="nt_si_hr@nantian.com.cn")
    password=base64.b16decode(fmail.password,False)
    invit=Invitation.objects.get(interview=interview_id)
    name = str(invit.interview.resume.CandidateName)
    subject,from_email,to,bcc,auth_password=u'北京南天软件有限公司面试邀请函'+'('+name+')',fmail.mail,invit.Imail,bcc,password
    text_content = 'This is an important message.'
    if invit.Iaddr==u"公司":
        t=loader.get_template("invitation_gong.html")
        c=Context({'invit': invit})
    if invit.Iaddr==u"中国银行黑山扈数据中心":
        t=loader.get_template("invitation_BOC.html")
        c=Context({'invit': invit})
    if invit.Iaddr==u"建行洋桥数据中心":
        t=loader.get_template("invitation_CCB.html")
        c=Context({'invit': invit})
    if invit.Iaddr==u"光大银行西二旗数据中心":
        t=loader.get_template("invitation_CEB.html")
        c=Context({'invit': invit})
    html_content = t.render(c)
    connection =mail.get_connection(username=from_email,password=auth_password,fail_silently=False)
    msg = EmailMultiAlternatives(subject, text_content,from_email,to=[to],bcc=bcc,connection=connection,headers = {"Bcc":",".join(bcc)},cc=[email])
    msg.attach_alternative(html_content, "text/html")
    if invit.Iaddr==u"公司":
        s='/home/resume/project/static/img/'+'公司地址.png'
        msg.attach_file(s)
    if invit.Iaddr==u"中国银行黑山扈数据中心":
        s='/home/resume/project/static/img/'+'中国银行黑山扈数据中心.png'
        msg.attach_file(s)
    if invit.Iaddr==u"建行洋桥数据中心":
        s='/home/resume/project/static/img/'+'建行洋桥数据中心.png'
        msg.attach_file(s)
    try:
        msg.send()
    except:
        return False
    else:
        return True
#offer邮件
def sent_offer(interview_id,tomail,ccmail,departname):   
    fmail=Email.objects.get(mail="nt_si_hr@nantian.com.cn")
    password=base64.b16decode(fmail.password,False)
    inte=Interview.objects.get(id=interview_id)
    changes=ChangeRecord.objects.filter(interview=interview_id)
    offer=Mail_Offer.objects.get(resume=inte.resume.id)
    subject,from_email,to,cc,auth_password=u'offer信息'+u'_'+u'集成_'+departname,fmail.mail,tomail,ccmail,password
    text_content = 'This is an important message.'
    t=loader.get_template("offermail.html")
    c=Context({'offer': offer,'changes':changes})
    html_content = t.render(c)
    connection =mail.get_connection(username=from_email,password=auth_password,fail_silently=False)
    msg = EmailMultiAlternatives(subject, text_content,from_email, [to],cc,connection=connection,headers = {"Cc":",".join(cc)})
    msg.attach_alternative(html_content, "text/html")
    s='/home/resume/project'+offer.resume.Addr.encode('utf8')
    if os.path.getsize(s)/1024 > 100:
        pass
    else:
        msg.attach_file(s)
    #msg.send()
    try:
        msg.send()
    except:
        return False
    else:
        return True
#处理中的面试
@login_required	
def processed(request):
    #从cookie获得数据
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    #数据查询
    inter2s = []
    Inter2s = Resume.objects.filter(Status=u"未处理").filter(UserID=user_id).exclude(Agency=None)
    inte2s=[]
    if Inter2s:
        for inter2 in Inter2s:   
            intes = Interview.objects.filter(resume=inter2.id)
            for inte in intes:
                change1s=ChangeRecord.objects.filter(interview=inte.id)
                inte2s.append([inte,change1s]) 
            inter2ss = str(inter2.id)+"ss"
            inter2s.append([inter2,inte2s,inter2ss])
            inte2s=[]
    inters=[]
    #特殊处理
    inter1s=[]
    cor1=Cor_role_user_depart.objects.filter(UserID = user.id)
    for cor in cor1:
        if cor.RoleID.name=="总经理":
            inter1s = Interview.objects.filter(Q(resume__Status=u"发offer",InterviewProcess=u"二面",Notes=u"发offer")| Q(resume__Status=u"发offer",InterviewProcess=u"三面",Notes=u"发offer")).filter(lockuser=user_id).filter(lockuser=F('resume__UserID')).filter(Active=1).filter(Turn=F('resume__Turn'))

    Inters = Interview.objects.filter(Q(resume__Status=u"一面",InterviewProcess=u"电话面试",InterStatus=u"通过")|Q(resume__Status=u"一面",InterviewProcess=u"电话面试",InterStatus=u"发邀请函") | Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"通过")| Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"发邀请函")| Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"通过")| Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"发邀请函")|Q(resume__Status=u"填写offer信息",InterviewProcess=u"二面",InterStatus=u"填写offer信息")|Q(resume__Status=u"填写offer信息",InterviewProcess=u"三面",InterStatus=u"填写offer信息")|Q(resume__Status=u"审批offer信息",InterviewProcess=u"二面",InterStatus=u"审批offer信息")|Q(resume__Status=u"审批offer信息",InterviewProcess=u"三面",InterStatus=u"审批offer信息")|Q(resume__Status=u"发邮件",InterviewProcess=u"二面",InterStatus=u"发邮件")|Q(resume__Status=u"发邮件",InterviewProcess=u"三面",InterStatus=u"发邮件")| Q(resume__Status=u"发offer",InterviewProcess=u"二面",Notes=u"发offer")| Q(resume__Status=u"发offer",InterviewProcess=u"三面",Notes=u"发offer")).filter(lockuser=user_id).filter(lockuser=F('resume__UserID')).exclude(Q(NextUser=user_id,resume__Agency=None)|Q(resume__Agency=user_id)).filter(Active=1).filter(Turn=F('resume__Turn'))
    paging = []
    side1=[]
    if Inters:
        for inter in Inters:   
            sides = Interview.objects.filter(resume=inter.resume.id)
            for side in sides:
                changes=ChangeRecord.objects.filter(interview=side.id)
                side1.append([side,changes])
            interss = str(inter.resume.id)+"ss"
            inters.append([inter,side1,interss])
            side1=[]
    else:
        intes=Inters
    if inter1s:
        for inter1 in inter1s:   
            side1s = Interview.objects.filter(resume=inter1.resume.id)
            for side2 in side1s:
                change2s=ChangeRecord.objects.filter(interview=side2.id)
                side1.append([side2,change2s])
            inter1ss = str(inter1.resume.id)+"ss"
            inters.append([inter1,side1,inter1ss])
            side1=[]

    #分页
    if not request.GET.get('page_size'):
        page_size = 15 
    else:
        page_size = int(request.GET.get('page_size'))
    paginator=Paginator(inters,page_size)
    page_num=request.GET.get('page')
    try:
        inters=paginator.page(page_num)
    except PageNotAnInteger:
        inters=paginator.page(1)
    except EmptyPage:
        inters=paginator.page(paginator.num_pages)
    paging = inters
    page_right = page_size * paging.number if (page_size * paging.number < len(Inters)) else len(Inters)
    page_left = page_size * (paging.number - 1) + 1 if (paging.number - 1) > 0 else 1
    #数据返回网页
    t = loader.get_template("processed.html")
    c = Context({'inters':inters,'member':user,'inter2s':inter2s,'paging':paging,'page_size':page_size,'page_left':page_left,'page_right':page_right})
    return HttpResponse(t.render(c))
#已完成的面试
@login_required	
def interviews(request):
    date = datetime.datetime.now()
    #cookie
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    #数据
    Inters = Resume.objects.filter(Q(Status=u"发offer未入职") | Q(Status=u"已入职")).filter(UserID=user_id)
    inters = []
    side1=[]
    for inter in Inters:
        sides = Interview.objects.filter(resume=inter.id)
        for side in sides:
                changes=ChangeRecord.objects.filter(interview=side.id)
                side1.append([side,changes])
        interss = str(inter.id)+"ss"
        inters.append([inter,side1,interss])
        side1=[]
    tt=[u'淘汰']
    #分页
    if not request.GET.get('page_size'):
        page_size = 15 
    else:
        page_size = int(request.GET.get('page_size'))
    paginator=Paginator(inters,page_size)
    page_num=request.GET.get('page')
    try:
        inters=paginator.page(page_num)
    except PageNotAnInteger:
        inters=paginator.page(1)
    except EmptyPage:
        inters=paginator.page(paginator.num_pages)
    paging = inters
    page_right = page_size * paging.number if (page_size * paging.number < len(Inters)) else len(Inters)
    page_left = page_size * (paging.number - 1) + 1 if (paging.number - 1) > 0 else 1
    #数据返回网页
    t = loader.get_template("interviews.html")
    c = Context({'inters':inters,'member':user,'tt':tt,'date':date,'paging':paging,'page_size':page_size,'page_left':page_left,'page_right':page_right})
    return HttpResponse(t.render(c))
#面试记录
@login_required
def Interview_resume(request,resume_id):
    #获得数据
    inters=[]
    Inters = Interview.objects.filter(resume=resume_id)
    for inter in Inters:
        changes=ChangeRecord.objects.filter(interview=inter.id)
        interss = str(inter.id)+"ss"
        inters.append([inter,changes,interss])
    #数据返回页面
    t = loader.get_template("Interview_resume.html")
    c = Context({'inters':inters})
    return HttpResponse(t.render(c))
'''
#推荐
@login_required
def recommend(request):
    UN=request.REQUEST.get('name')    
    RID=request.REQUEST.get('RID')    
    users=MyUser.objects.filter(username=UN)
    if len(users):
        pass
    else:
        return HttpResponse("该用户不存在")
    for user in users:
            pass
    inters=Interview.objects.filter(resume=RID).filter(lockuser=user.id)
    if len(inters):
        return HttpResponse("候选人已被该用户锁定过")
        
    Resume.objects.filter(id=RID).update(UserID = user.id)
    Resume.objects.filter(id=RID).update(Status = u"未处理")
    Resume.objects.filter(id=RID).update(Level=None)
    
    Resume.objects.filter(pk=RID).update(Ephone=None)
    Resume.objects.filter(pk=RID).update(Email=None)
    Resume.objects.filter(pk=RID).update(Eentrytime=None)
    Resume.objects.filter(pk=RID).update(Epost=None)
    Resume.objects.filter(pk=RID).update(Epostgrade=None)
    Resume.objects.filter(pk=RID).update(Ejob=None)
    Resume.objects.filter(pk=RID).update(Ejobin=None)
    Resume.objects.filter(pk=RID).update(Ejobaim=None)
    Resume.objects.filter(pk=RID).update(Eprimary=None)
    Resume.objects.filter(pk=RID).update(Esecond=None)
    Resume.objects.filter(pk=RID).update(Eproject=None)
    Resume.objects.filter(pk=RID).update(Ecompacttime=None)
    Resume.objects.filter(pk=RID).update(Eapplytime=None)
    return HttpResponse("推荐成功")
    
'''    
#代处理
@login_required
def agency(request):
    #cookie
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user1 = UserModel.objects.get(id = user_id)

    UN=request.REQUEST.get('name')    
    RID=request.REQUEST.get('RID')    
    users=MyUser.objects.filter(username=UN)
    if len(users):
        pass
    else:
        return HttpResponse("该用户不存在")
    for user in users:
            pass     
    if user1==user:
        return HttpResponse("请选择其他处理人")
    noID=""
    yesID=""
    ids=RID.split('|')
    for Id in ids:
        if Id:
            resume = Resume.objects.filter(id=Id).filter(Q(Status="填写offer信息")|Q(Status="审批offer信息")|Q(Status="发邮件"))
            if len(resume):
                for resume1 in resume:
                    pass
                if noID=="":
                    noID=str(resume1.CandidateName)
                else:
                    noID= noID + "、" + str(resume1.CandidateName)
                #return HttpResponse("该事项不能代处理")
            else:
                resume = Resume.objects.filter(id=Id)
                for resume1 in resume:
                    pass
                Resume.objects.filter(id=Id).update(Agency = user.id)
                if yesID=="":
                    yesID=str(resume1.CandidateName)
                else:
                    yesID=yesID + "、" + str(resume1.CandidateName)
    if noID=="":
        return HttpResponse(yesID+"操作成功")
    elif yesID=="":
        return HttpResponse(noID+"不能代处理")
    else:
        return HttpResponse(noID+"不能代处理"+"；"+yesID+"操作成功")
    
    
#待入职
@login_required	
def entry(request):
    #cookie
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    
    inters = Resume.objects.filter(Status=u"发offer")
    inters2=[] 
    for inter2 in inters:   
            side1 = Interview.objects.filter(resume=inter2.id)
            inter2ss = str(inter2.id)+"ss"
            inters2.append([inter2,side1,inter2ss])
    #分页
    if not request.GET.get('page_size'):
        page_size = 15 
    else:
        page_size = int(request.GET.get('page_size'))
    paginator=Paginator(inters2,page_size)
    page_num=request.GET.get('page')
    try:
        inters2=paginator.page(page_num)
    except PageNotAnInteger:
        inters2=paginator.page(1)
    except EmptyPage:
        inters2=paginator.page(paginator.num_pages)
    paging = inters2
    page_right = page_size * paging.number if (page_size * paging.number < len(inters2)) else len(inters2)
    page_left = page_size * (paging.number - 1) + 1 if (paging.number - 1) > 0 else 1
    #返回
    t = loader.get_template("entry.html")
    c = Context({'inters2':inters2,'member':user,'paging':paging,'page_size':page_size,'page_left':page_left,'page_right':page_right})
    return HttpResponse(t.render(c))
#已入职
@login_required	
def entryed(request):
    #cookie
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    #数据
    inters = Entry.objects.filter(resume__Status=u"已入职").order_by('-Time')
    #分页
    if not request.GET.get('page_size'):
        page_size = 15 
    else:
        page_size = int(request.GET.get('page_size'))
    paginator=Paginator(inters,page_size)
    page_num=request.GET.get('page')
    try:
        inters=paginator.page(page_num)
    except PageNotAnInteger:
        inters=paginator.page(1)
    except EmptyPage:
        inters=paginator.page(paginator.num_pages)
    paging = inters
    page_right = page_size * paging.number if (page_size * paging.number < len(inters)) else len(inters)
    page_left = page_size * (paging.number - 1) + 1 if (paging.number - 1) > 0 else 1
    #返回
    t = loader.get_template("entryed.html")
    c = Context({'inters':inters,'member':user,'paging':paging,'page_size':page_size,'page_left':page_left,'page_right':page_right})
    return HttpResponse(t.render(c))
#未入职
@login_required	
def noentryed(request):
    #cookie
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    #数据
    inters = Entry.objects.filter(resume__Status=u"发offer未入职").order_by('-Time')
    #分页
    if not request.GET.get('page_size'):
        page_size = 15 
    else:
        page_size = int(request.GET.get('page_size'))
    paginator=Paginator(inters,page_size)
    page_num=request.GET.get('page')
    try:
        inters=paginator.page(page_num)
    except PageNotAnInteger:
        inters=paginator.page(1)
    except EmptyPage:
        inters=paginator.page(paginator.num_pages)
    paging = inters
    page_right = page_size * paging.number if (page_size * paging.number < len(inters)) else len(inters)
    page_left = page_size * (paging.number - 1) + 1 if (paging.number - 1) > 0 else 1
    #返回
    t = loader.get_template("noentryed.html")
    c = Context({'inters':inters,'member':user,'paging':paging,'page_size':page_size,'page_left':page_left,'page_right':page_right})
    return HttpResponse(t.render(c))
#入职记录
@login_required	
def entryrecord(request,resume_id):
    #cookie
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    #数据
    erecords = Entry.objects.filter(resume=resume_id)
    #返回
    t = loader.get_template("entryrecord.html")
    c = Context({'erecords':erecords})
    return HttpResponse(t.render(c))
#新的入职
@login_required	
def newentry(request,resume_id):
    date = datetime.datetime.now()
    #cookie
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    User = UserModel.objects.get(id = user_id)
    
    finish="goback"     
    shows = Resume.objects.filter(id=resume_id)
    for show in shows:
        dis = show.CandidateName
    position = show.Station
    stations = Position.objects.filter(Filing=0)
    #POST
    if request.method == 'POST':
        form = EntryForm(request.POST)
        position1 = request.POST['position']
        check = Entry.objects.filter(resume=resume_id)
        #错误处理                                  
        if len(check):
            print "记录已存在"
            return render_to_response('newentry.html', {'form': form,'finish':finish,'date':date,'error1': '记录已存在','member': User,'dis': dis,'position':position,'stations':stations}, context_instance=RequestContext(request))
                                          
        #表单验证                                                                              
        if form.is_valid():
            cd = form.cleaned_data
            new_inter=form.save(commit=False)
            for show in shows:
                new_inter.resume=show
            new_inter.user=User
            
            new_inter.save()
            form.save_m2m()
            #数据更新
            positions = Position.objects.get(id = position1)
            positions.recruitednum += 1 
            positions.ExistingPersonNum += 1
            if positions.recruitednum==positions.NeedPersonNum:
                    positions.Filing = 1 
            positions.save()
            Resume.objects.filter(pk=resume_id).update(Status = (cd['Status1']))
            #跳转
            finish="goto"     
            return render_to_response('newentry.html',{'form': form,'finish':finish,'date':date,'member': User,'dis': dis,'position':position,'stations':stations},context_instance=RequestContext(request))
            #return HttpResponseRedirect('/side/entry')
        else:
            #print form
            print 'en_error1'
           
            print form['EntryResults'].errors
            print form['Status1'].errors
            print form['Time'].errors
    else:
        form = EntryForm() 
    return render_to_response('newentry.html',{'form': form,'finish':finish,'date':date,'member': User,'dis': dis,'position':position,'stations':stations},context_instance=RequestContext(request))
 
#按月统计数据
def statisticsmon(request):
    date = time.localtime(time.time())
    yea=date.tm_year
    mon=date.tm_mon
    if request.method == 'POST':
           yea = request.POST.get('year','')
           mon = request.POST.get('month','')
           yea = string.atoi(yea)
           mon = string.atoi(mon)
    if yea <= 2015 and mon <= 12:     
        readnum=len(Resume.objects.filter(Time__year=yea).filter(Time__month=mon))
        suitnum=len(Resume.objects.filter(Time__year=yea).filter(Time__month=mon).exclude(UserID=None))
        nosuitnum=readnum-suitnum

        infromnum=len(Interview.objects.filter(Time__year=yea).filter(Time__month=mon).filter(InterviewProcess=u"电话面试").exclude(InterStatus=u"淘汰"))
        internum=len(Interview.objects.filter(Time__year=yea).filter(Time__month=mon).filter(InterviewProcess=u"一面"))
        nointernum=infromnum-internum
        if nointernum < 0:
           nointernum = 0
        offernum=len(ChangeRecord.objects.filter(Ctime__year=yea).filter(Ctime__month=mon).filter(interview__resume__Status=u"发offer").filter(Cnotes=u"同意"))
        staffnum=len(Entry.objects.filter(Time__year=yea).filter(Time__month=mon).filter(resume__Status=u"已入职"))
        nostaffnum=offernum-staffnum
        if nostaffnum < 0:
           nostaffnum = 0
        return render_to_response('statisticsmon.html',{'year':yea ,'month':mon,'nosuitnum':nosuitnum,'suitnum': suitnum,'nointernum':nointernum,'internum':internum,'nostaffnum':nostaffnum,'staffnum':staffnum ,'readnum':readnum,'infromnum':infromnum,'offernum':offernum},context_instance=RequestContext(request))
    elif yea > 2015:
        readnum=len(Resume.objects.filter(Time__year=yea).filter(Time__month=mon))
        suitnum=len(Resume.objects.filter(LockTime__year=yea).filter(LockTime__month=mon).exclude(UserID=None))
        nosuitnum=readnum-suitnum

        infromnum=len(Interview.objects.filter(Time__year=yea).filter(Time__month=mon).filter(InterviewProcess=u"电话面试").exclude(InterStatus=u"淘汰"))
        internum=len(Interview.objects.filter(Time__year=yea).filter(Time__month=mon).filter(InterviewProcess=u"一面"))
        nointernum=infromnum-internum

        offernum=len(EmailRecord.objects.filter(handletime__year=yea).filter(handletime__month=mon).filter(Type="offer邮件").filter(notes="发送成功"))
        staffnum=len(Entry.objects.filter(Time__year=yea).filter(Time__month=mon).filter(resume__Status=u"已入职"))
        nostaffnum=offernum-staffnum
        return render_to_response('statisticsmon.html',{'year':yea ,'month':mon,'nosuitnum':nosuitnum,'suitnum': suitnum,'nointernum':nointernum,'internum':internum,'nostaffnum':nostaffnum,'staffnum':staffnum ,'readnum':readnum,'infromnum':infromnum,'offernum':offernum},context_instance=RequestContext(request))
    else:
        return render_to_response('statisticsmon.html',{'year':yea ,'month':mon},context_instance=RequestContext(request))
#按年统计数据
def statisticsyea(request):
    date = time.localtime(time.time())
    yea=date.tm_year
    readnum=[]
    suitnum=[]
    infromnum=[]
    internum=[]
    offernum=[]
    staffnum=[]
    if request.method == 'POST':
           yea = request.POST.get('year','')
           yea = string.atoi(yea)
    if yea <= 2015:
        readnumy=len(Resume.objects.filter(Time__year=yea))
        suitnumy=len(Resume.objects.filter(Time__year=yea).exclude(UserID=None))

        infromnumy=len(Interview.objects.filter(Time__year=yea).filter(InterviewProcess=u"电话面试").exclude(InterStatus=u"淘汰"))
        internumy=len(Interview.objects.filter(Time__year=yea).filter(InterviewProcess=u"一面"))

        offernumy=len(ChangeRecord.objects.filter(Ctime__year=yea).filter(interview__resume__Status=u"发offer").filter(Cnotes=u"同意"))
        staffnumy=len(Entry.objects.filter(Time__year=yea).filter(resume__Status=u"已入职"))
        for mon in range(1,13):
            readnum.append(len(Resume.objects.filter(Time__year=yea).filter(Time__month=mon)))
            suitnum.append(len(Resume.objects.filter(Time__year=yea).filter(Time__month=mon).exclude(UserID=None)))
    
            infromnum.append(len(Interview.objects.filter(Time__year=yea).filter(Time__month=mon).filter(InterviewProcess=u"电话面试").exclude(InterStatus=u"淘汰")))
            internum.append(len(Interview.objects.filter(Time__year=yea).filter(Time__month=mon).filter(InterviewProcess=u"一面")))
        
            offernum.append(len(ChangeRecord.objects.filter(Ctime__year=yea).filter(Ctime__month=mon).filter(interview__resume__Status=u"发offer").filter(Cnotes=u"同意")))
            staffnum.append(len(Entry.objects.filter(Time__year=yea).filter(Time__month=mon).filter(resume__Status=u"已入职")))
        return render_to_response('statisticsyea.html',{'year':yea ,'readnum':readnum,'suitnum': suitnum,'infromnum':infromnum,'internum':internum,'offernum':offernum,'staffnum':staffnum,'readnumy':readnumy,'suitnumy': suitnumy,'infromnumy':infromnumy,'internumy':internumy,'offernumy':offernumy,'staffnumy':staffnumy },context_instance=RequestContext(request))

    elif yea > 2015:
        readnumy=len(Resume.objects.filter(Time__year=yea))
        suitnumy=len(Resume.objects.filter(LockTime__year=yea).exclude(UserID=None))

        infromnumy=len(Interview.objects.filter(Time__year=yea).filter(InterviewProcess=u"电话面试").exclude(InterStatus=u"淘汰"))
        internumy=len(Interview.objects.filter(Time__year=yea).filter(InterviewProcess=u"一面"))

        offernumy=len(EmailRecord.objects.filter(handletime__year=yea).filter(Type="offer邮件").filter(notes="发送成功"))
        staffnumy=len(Entry.objects.filter(Time__year=yea).filter(resume__Status=u"已入职"))
        for mon in range(1,13):
            readnum.append(len(Resume.objects.filter(Time__year=yea).filter(Time__month=mon)))
            suitnum.append(len(Resume.objects.filter(LockTime__year=yea).filter(LockTime__month=mon).exclude(UserID=None)))
    
            infromnum.append(len(Interview.objects.filter(Time__year=yea).filter(Time__month=mon).filter(InterviewProcess=u"电话面试").exclude(InterStatus=u"淘汰")))
            internum.append(len(Interview.objects.filter(Time__year=yea).filter(Time__month=mon).filter(InterviewProcess=u"一面")))
        
            offernum.append(len(EmailRecord.objects.filter(handletime__year=yea).filter(handletime__month=mon).filter(Type="offer邮件").filter(notes="发送成功")))
            staffnum.append(len(Entry.objects.filter(Time__year=yea).filter(Time__month=mon).filter(resume__Status=u"已入职")))
        return render_to_response('statisticsyea.html',{'year':yea ,'readnum':readnum,'suitnum': suitnum,'infromnum':infromnum,'internum':internum,'offernum':offernum,'staffnum':staffnum,'readnumy':readnumy,'suitnumy': suitnumy,'infromnumy':infromnumy,'internumy':internumy,'offernumy':offernumy,'staffnumy':staffnumy },context_instance=RequestContext(request))
    else:
        return render_to_response('statisticsyea.html',{'year':yea },context_instance=RequestContext(request))


#发offer邮件
@login_required	
def sent_omail(request,interview_id):
    #从cookie获得数据
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    finish="goback"     
       
    inter = Interview.objects.filter(id = interview_id).filter(NextUser=user_id).filter(resume__Status=u"发邮件").filter(Active=1)
    for inte in inter:
        pass
    if inter:
        pass
    else:
        error="对不起！权限不够"
        return HttpResponse(error)
    cc=user.email
    cc=user.email+"\r\n"+"lidong@nantian.com.cn"
    departname=get_fridepart(user).name
    tomail="jiangfengli@nantian.com.cn"
    #tomail="***@nantian.com.cn"
    mailerror = "其他数据已保存。请输入收件邮箱和抄送人邮箱!"
    if request.method == 'POST':
        tomail = request.POST['tomail']
        cc = request.POST['cc']
        ccmail=[]
        if len(tomail):
            pass
        else:
            mailerror="收件邮箱不能为空"
            return render_to_response("sent_omail.html",{'tomail':tomail,'finish':finish,'cc':cc,'mailerror':mailerror},context_instance=RequestContext(request))
        if len(cc)>0:
            ccss=cc.split("\r\n")
            for ccs in ccss:
                ccs=ccs.strip()
                ccmail.append(ccs)
        else:
            cc=None
		
        mails=EmailRecord.objects.filter(resume=inte.resume.id,interview=inte.id,handleuser=user_id,touser=tomail,Type="offer邮件",notes="发送成功")
        if len(mails):
            pass
        else:
            if sent_offer(interview_id,tomail,ccmail,departname) is False:
                mailerror = "邮件发送失败！...请重新输入!"
                #记录发送情况
                mailtime(inte.resume,inte,user,tomail,"offer邮件",cc,None,"发送失败")
                return render_to_response("sent_omail.html",{'tomail':tomail,'finish':finish,'cc':cc,'mailerror':mailerror},context_instance=RequestContext(request))
            else:
                mailtime(inte.resume,inte,user,tomail,"offer邮件",cc,None,"发送成功")
                Resume.objects.filter(pk=inte.resume.id).update(Status=u"发offer")
                Interview.objects.filter(id=interview_id).update(InterStatus=u"通过")
                finish="goto"     
                return render_to_response("sent_omail.html",{'tomail':tomail,'finish':finish,'mailerror':mailerror,'cc':cc},context_instance=RequestContext(request)) 
        finish="goto"     
        return render_to_response("sent_omail.html",{'tomail':tomail,'finish':finish,'mailerror':mailerror,'cc':cc},context_instance=RequestContext(request)) 

            #return HttpResponseRedirect("/side/stucked")
    else:
        return render_to_response("sent_omail.html",{'tomail':tomail,'finish':finish,'mailerror':mailerror,'cc':cc},context_instance=RequestContext(request)) 
#得到一级部门总经理对象
def get_boss(user):
    #如果自己是总经理
    cor1=Cor_role_user_depart.objects.filter(UserID = user.id)
    for cor in cor1:
        if cor.RoleID.name=="总经理":
            boss=MyUser.objects.get(id = cor.UserID.id) 
            return boss
    #如果上级是总经理或者更上级是总经理
    for i in range(10):
        user = get_leader(user)
        cor1=Cor_role_user_depart.objects.filter(UserID = user.id)
        for cor in cor1:
            if cor.RoleID.name=="总经理":
                boss=MyUser.objects.get(id = cor.UserID.id) 
                return boss
#由总经理得到一级部门
def get_fridepart(boss):
    cor1=Cor_role_user_depart.objects.filter(UserID = boss.id).filter(RoleID__name=u"总经理")
    for cor in cor1:  
        return cor.RoleID.DepartmentID
#由一级部门得到总经理
def get_boss1(depart):
    cor1=Cor_role_user_depart.objects.filter(RoleID__DepartmentID=depart).filter(RoleID__name=u"总经理")
    for cor in cor1:  
        return cor.UserID
#得到所有拥有Offer发送权的用户 因流程变化废弃
def myuser():
    user=[]
    temps=Cor_user_Power.objects.filter(PowerID__name="Offer发送权")
    for temp in temps:
        user.append(temp.UserID)
    return user 
#得到所有拥有简历筛选权的用户
def myuser_res():
    user=[]
    temps=Cor_user_Power.objects.filter(PowerID__name="简历筛选权")
    for temp in temps:
        user.append(temp.UserID)
    return user 
#ajax得到对应职位相关信息
def get_content(request):
    #从cookie获得数据
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    pos=''
     
    #得到职位id
    oid= request.GET['id']
    #获取职位对象
    position=Position.objects.get(id=oid)
    #得到相关信息并放入pos
    need=position.NeedPersonNum-position.recruitednum
    pos= '^'.join([str(position.RecruitWay),str(position.RecruitReason),str(position.Depart.name),str(position.SecondDepartment.name),str(position.ProjectName),str(need)])
    return HttpResponse(pos)
#用户操作记录
def handletime(resume=None,interview=None,user=None,Type=None,active=1,notes=None):
    try:
        handle1=HandleRecord(resume=resume,interview=interview,handleuser=user,Type=Type,active=active,notes=notes)
        handle1.save()
        return "操作记录保存成功"
    except:
        return "操作记录保存失败"
#邮件发送记录
def mailtime(resume=None,interview=None,user=None,touser=None,Type=None,cc=None,bcc=None,notes=None):
    try:
        mailrecord1=EmailRecord(resume=resume,interview=interview,handleuser=user,touser=touser,Type=Type,cc=cc,bcc=bcc,notes=notes)
        mailrecord1.save()
        return "邮件记录保存成功"
    except:
        return "邮件记录保存失败"
#获得用户邮箱ajax    
def get_emails(request):
    '''获取所有的用户信息'''
    users = MyUser.objects.filter(is_active = 1)
    key=['label','value']
    str_users = ""
    for user in users:
        temp ={'label':str(user.username)+" "+str(user.email),'value':str(user.email)}
        str_user=json.dumps(temp,ensure_ascii = False)
        str_user=str(str_user)+";"
        str_users += str_user
    return HttpResponse(str_users)
'''    
 #邮箱出错处理
@login_required	
def sent_omail(request,resume_id):
    #从cookie获得数据
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    email=user.email
    
    
    mailerror = "其他数据已保存。请输入邮箱或密码!"
    if request.method == 'POST':
        email = request.POST.get('email','')
        mailpass = request.POST.get('mailpass','')
        if sent_offer(resume_id,email,mailpass) is False:
            mailerror = "邮箱或密码错误...请重新输入!"
            return render_to_response("sent_omail.html",{'email':email,'mailpass':mailpass,'mailerror':mailerror},context_instance=RequestContext(request))
        else:
            
            Resume.objects.filter(pk=resume_id).update(Status=u"发offer")
            return HttpResponseRedirect("/side/stucked")
    else:
        return render_to_response("sent_omail.html",{'email':email,'mailerror':mailerror},context_instance=RequestContext(request))    
'''
