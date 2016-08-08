#-*- encoding: utf-8 -*-
import os
import thread
import hashlib
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core import mail
import datetime
from django.utils import timezone
from django.utils.timezone import now,timedelta
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader,Context,RequestContext
from talents.models import Position as Position1,Examine
from talents.forms import PositionForm,ExamineForm
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from resume.models import Resume,import_ID
from accounts.models import MyUser
from manager.models import Cor_role_user_depart,Roles,Department,Power,Cor_user_Power,Email,Third_project,Customer
from side.models import Interview
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth import get_user_model
from django.db.models import Q,F
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.http import HttpResponseRedirect
import codecs,string
import base64
# Create your views here.

#显示所申请职位的详细信息
@login_required    
def positionprofile(request,position_id):
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    User = UserModel.objects.get(id = user_id)
    position=Position1.objects.get(pk=position_id)
    return render(request,'positionprofile.html',{'position':position})

#职位审批
@login_required
def examine(request,position_id):
    shu = 0        #html中刷新父窗口关闭当前窗口的判断
    #date=datetime.datetime.now()
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    User = UserModel.objects.get(id = user_id)
    position=Position1.objects.get(pk=position_id)
    errors=[]
    roles = get_role(User) #获取当前用户的角色
    for role in roles:
        if role.name == u"总经理":
            rule = u"总经理"
            break
        else: 
            rule = "其他"
    
    #POST方式接受数据
    examines=Examine.objects.filter(PositionID=position.id).filter(PositionID__Filing=2)
    if request.method == 'POST':
        #从POST得到表单
        form = ExamineForm(request.POST)
       
        #form表单验证
        if form.is_valid():
            #cleaned_data读取表单返回的值
            cd = form.cleaned_data
            shu=1
            result=request.POST['Result']
            comment = request.POST['comment']
            time=timezone.now()
            Examine.objects.filter(PositionID=position,UserID=User).update(Result=result,comment=comment,Time=time) #更新审批数据
            #保存关联信息
            #form.save_m2m()
            #approver = get_leader( User )

            if rule == "其他":
                if request.POST['Result'] == u"不同意":
                    exa=Examine.objects.get(PositionID=position,UserID=User)
                    Position1.objects.filter(pk=position_id).update(States=u"被退回",Approver=exa.last_user)
                    if approver:
                        pass
                        #Examine.objects.filter(PositionID=position,UserID=approver).update(Result="")
                else: 
                    exa=Examine.objects.get(PositionID=position,UserID=User)
                    Position1.objects.filter(pk=position_id).update(States=u"审批中",Approver=exa.next_approver)
                    Examine.objects.filter(PositionID=position,UserID=exa.next_approver).update(Result="审批中")
                    '''
                    Position1.objects.filter(pk=position_id).update(Filing=0)
                    else:
                        
                        #最高领导审批完给罗艳丽发邮件
                        user=MyUser.objects.get(username="罗艳丽")
                        positions=Position1.objects.filter(pk=position_id).update(Approver=user,States = "待发布",Filing=4)
                        email=Email.objects.get(mail="nt_si_hr@nantian.com.cn")
                        password=base64.b16decode(email.password,False)
                        subject,from_email, auth_password=u'您有一个待发布职位申',email.mail,password
                        #to=['luoyanli@nantian.com.cn','zhenghong@nantian.com.cn']
                        to=['linana@nantian.com.cn']
                        examines=Examine.objects.filter(PositionID=position_id)
                        # posititon=Position1.Objects.get(pk=position_id)
                        text_content = 'This is an important message.'
                        t=loader.get_template("pub_position.html")
                        c=Context({'position': position,'examines': examines})
                        html_content = t.render(c)
                        connection =mail.get_connection(username=from_email,password=auth_password,fail_silently=False)
                        msg = EmailMultiAlternatives(subject, text_content,from_email, to,connection=connection)
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                    '''
            if rule == u"总经理":
                if request.POST['Result'] == u"不同意":
                    exa=Examine.objects.get(PositionID=position,UserID=User)
                    Position1.objects.filter(pk=position_id).update(States=u"被退回",Approver=exa.last_user)
                else:
                    #Position1.objects.filter(pk=position_id).update(States=u"待发布",Filing=4)
                    #最高领导审批完给罗艳丽发邮件
                    user=MyUser.objects.get(username="罗艳丽")
                    positions=Position1.objects.filter(pk=position_id).update(Approver=user,States = "待发布",Filing=4)
                    email=Email.objects.get(mail="nt_si_hr@nantian.com.cn")
                    password=base64.b16decode(email.password,False)
                    subject,from_email, auth_password=u'您有一个待发布职位申',email.mail,password
                    to=['luoyanli@nantian.com.cn','zhenghong@nantian.com.cn','jiangfengli@nantian.com.cn','wanghui@nantian.com.cn']
                    #to=['linana@nantian.com.cn']
                    examines=Examine.objects.filter(PositionID=position_id)
                    # posititon=Position1.Objects.get(pk=position_id)
                    text_content = 'This is an important message.'
                    t=loader.get_template("pub_position.html")
                    c=Context({'position': position,'examines': examines})
                    html_content = t.render(c)
                    connection =mail.get_connection(username=from_email,password=auth_password,fail_silently=False)
                    msg = EmailMultiAlternatives(subject, text_content,from_email, to,connection=connection)
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    #Position1.objects.filter(pk=position_id).update(Approver=approver)                 
                    #Examine.objects.filter(PositionID=position,UserID=approver).update(Result="审批中")
                    #thread.start_new_thread(set_Email,(position_id,))
                    #set_Email(position_id)
            return render(request,'examine.html',{'examines':examines,'position':position,'User':User,'form':form,'member': User,'rule': rule,'shu':shu})
        else:
            return render(request,'examine.html',{'examines':examines,'position':position,'User':User,'form':form,'member': User,'rule': rule,'shu':shu})
    else:
        ##获得表单对象
        form = ExamineForm() 
        print form
        print 'examine_error2'
    return render(request,'examine.html',{'examines':examines,'position':position,'User':User,'form':form,'member': User,'rule': rule,'shu':shu})

#招聘完成情况
@login_required    
def positiontask(request):
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    roles=get_role(user)
    positions=[]
    for role in roles:
        if role.name == "招聘专员":
           department=role.DepartmentID
           positions=Position1.objects.filter(Q(Depart=department)|Q(SecondDepartment=department)).filter(Filing = 0)
           num=len(positions)
           break
        else:
           positions=Position1.objects.filter(UserID=user).filter(Filing = 0)
           break
    #positions=Position1.objects.filter(UserID=user_id).filter(Filing=0)
    t=loader.get_template("positiontask.html")
    c=Context({'positions': positions})
    return HttpResponse(t.render(c))

#对应某一个职位招聘完成情况    
@login_required    
def positiontask1(request,position_id):    
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    positions=Position1.objects.filter(pk=position_id)
    t=loader.get_template("positiontask1.html")
    c=Context({'positions': positions})
    return HttpResponse(t.render(c))

#将所发布职位显示出来    
@login_required    
def position(request):
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)    
    positions=Position1.objects.filter(Filing=0).order_by('-id')
    Position_Exam = []
    for position in positions:
        needperson=position.NeedPersonNum-position.recruitednum
        position_exams = Examine.objects.filter(PositionID = position.id)
        position_exam_id = str(position.id)+'id'
        Position_Exam.append([position,needperson,position_exams,position_exam_id])
    if not request.GET.get('page_size'):
        page_size = 15
    else:
        page_size = int(request.GET.get('page_size'))
    paginator=Paginator(Position_Exam,page_size)
    page_num=request.GET.get('page')
    try:
        Position_Exam=paginator.page(page_num)
    except PageNotAnInteger:
        Position_Exam=paginator.page(1)
    except EmptyPage:
        Position_Exam=paginator.page(paginator.num_pages)
    page_right = page_size * Position_Exam.number if (page_size * Position_Exam.number < len(Position_Exam)) else len(Position_Exam)
    page_left = page_size * (Position_Exam.number - 1) + 1 if ((Position_Exam.number - 1) > 1) else 1
    t=loader.get_template("positionmanage.html")
    c=Context({'Position_Exam':Position_Exam,'record_count':len(Position_Exam),'page_size':page_size,'page_left':page_left,'page_right':page_right})
    return HttpResponse(t.render(c))

#职位申请表    
@login_required    
def positionform(request):
    departments=[]

    #projects=Third_project.objects.all()
    #projects=[]
    roles=[]
    UserModel=get_user_model()
    date=datetime.datetime.now()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    projects=Third_project.objects.filter(recruiter=user)
    customers=Customer.objects.filter(customer_manager=user)
    for cus in customers:
        pro = Third_project.objects.filter(customer=cus)
        projects = list(set(projects).union(set(pro)))

    #project=Third_project.objects.all()
    roles=get_role(user)
    departments = get_depart( user )
    errors=[]
    shu=0
    # PositionForm.UserID = user_id
    Awarding = ''
    NeedPersonNum = ''
    ExistingPersonNum = ''
    #ProjectName = ''
    Workplace = ''
    Salary = ''
    RecruitTime = ''
    CandidateRequirement = ''
    WorkContent =''
    PositionName = ''
    add_reason=''
    get_leader(user)
    #roles=get_Role(user)
    #return HttpResponse(get_leader(user))
    if request.method == 'POST':
        #form = PositionForm(request.POST)
        #tmps = request.POST.get('fromStationText','')
        Awarding = request.POST.get('Awarding','')
        department = request.POST['SecondDepartment']
        NeedPersonNum = request.POST['staff_invite']
        ExistingPersonNum = request.POST['staff_now']
        ProjectName = request.POST['project']
        Workplace = request.POST['place']
        Salary = request.POST['salary']
        RecruitTime = request.POST['period']
        RecruitReason = request.POST['reason']
        RecruitWay = request.POST['RecruitWay']
        CandidateRequirement = request.POST['CandidateRequirement']
        WorkContent = request.POST['WorkContent']
        PositionName = request.POST['position']
        add_reason=request.POST.get('add_reason','')
        if PositionName and Salary and ExistingPersonNum and NeedPersonNum and Workplace and RecruitReason and WorkContent and CandidateRequirement and RecruitWay and RecruitTime:
            shu=1
            position1=Position1()
            position1.PositionName=PositionName
            position1.ExistingPersonNum=ExistingPersonNum
            position1.NeedPersonNum=NeedPersonNum
            position1.Workplace=Workplace
            position1.RecruitReason=RecruitReason
            position1.WorkContent=WorkContent
            position1.CandidateRequirement=CandidateRequirement
            position1.RecruitWay=RecruitWay
            position1.RecruitTime=RecruitTime
            #proj=Third_project(id=ProjectName)
            position1.ProjectName=ProjectName
            depar=Department.objects.get(id = department)
            position1.Depart = depar.superior_department
            #depar=Department.objects.get(id = department)
            position1.SecondDepartment = depar
            position1.UserID = user
            project = Third_project.objects.get(name=ProjectName)
            role=Roles.objects.filter(DepartmentID = project.customer.depart,name="总经理")
            cor=Cor_role_user_depart.objects.get(RoleID=role)
            if user == project.customer.customer_manager:
                approver = cor.UserID
            else:
                approver = project.customer.customer_manager
            position1.Approver = approver
            position1.Awarding = Awarding
            position1.Salary=Salary
            position1.States="审批中"
            position1.Headline=timezone.now()
            position1.add_reason = add_reason
            position1.save()
            
            if user == project.customer.customer_manager:
                examine = Examine()
                examine.UserID = cor.UserID
                examine.PositionID = position1
                examine.last_user = position1.UserID  
                examine.count=1
                examine.save()
            else:
                examine = Examine()
                examine.UserID = project.customer.customer_manager
                examine.PositionID = position1
                examine.last_user = position1.UserID
                examine.next_approver = cor.UserID
                examine.count=1
                examine.save()
                examine1 = Examine()
                examine1.UserID = cor.UserID
                examine1.PositionID = position1
                examine1.last_user = project.customer.customer_manager
                examine1.count=1
                examine1.save()

            '''
            for i in range(10):
                roles=get_role(user)
                for role in roles:
                    if role.name == '总经理':
                        break
                    else:
                        role ='其他'

                if role == '其他':
                    user = get_leader(user)
                    if user:
                        examine = Examine()
                        examine.UserID = user
                        examine.PositionID = position1
                        if get_leader(user):
                            examine.next_approver = get_leader(user)
                        if user == position1.Approver:
                            examine.last_user = position1.UserID
                        else:
                            exa = Examine.objects.get(next_approver = user,PositionID = position1 )
                            examine.last_user = exa.UserID
                        examine.Is_resultful = 1
                        examine.conut=1
                        examine.save()
                    else:
                       break
                else:
                    break
            '''
            Examine.objects.filter(PositionID=position1,UserID=approver).update(Result="审批中")                
        else:
            errors="所有字段均不可以为空"
            return render_to_response('positionform.html',RequestContext(request,{'add_reason':add_reason,'shu':shu,'date':date,'errors':errors,'Awarding':Awarding,'PositionName':PositionName,'departments':departments,'ExistingPersonNum':ExistingPersonNum,'NeedPersonNum':NeedPersonNum,'Workplace':Workplace,'RecruitReason':RecruitReason,'WorkContent':WorkContent,'CandidateRequirement':CandidateRequirement,'RecruitWay':RecruitWay,'RecruitTime':RecruitTime,'Salary':Salary, 'projects':projects}))
        #roles=get_role(user)
        '''
        position_id =str( position1.id)
        for role in roles:
            if role.name == u"总经理":
                rule = u"总经理"
                break;
            else:
                rule = "其他"
        if rule == "总经理":
            set_Email(position_id)
            Position1.objects.filter(id=position1.id).update(Approver=approver)
        else:
            pass 
        '''
            #return HttpResponseRedirect('/talents/handleingposition')
    return render(request,'positionform.html',{'add_reason':add_reason,'shu':shu,'date':date,'departments':departments,'Awarding':Awarding,'PositionName':PositionName,'ExistingPersonNum':ExistingPersonNum,'NeedPersonNum':NeedPersonNum,'Workplace':Workplace,'WorkContent':WorkContent,'CandidateRequirement':CandidateRequirement,'RecruitTime':RecruitTime,'Salary':Salary,'projects':projects})

#显示人才库中的简历     
@login_required    
def talents_pool(request):
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    delete=[u'未处理']
    inters1 = Resume.objects.filter(Status=u"未处理")
    inters = inters1.filter(Q(UserID=user_id,Agency=None)|Q(Agency=user_id))
    inters2 = Interview.objects.filter(Q(resume__Status=u"一面",InterviewProcess=u"电话面试") | Q(resume__Status=u"二面",InterviewProcess=u"一面")| Q(resume__Status=u"三面",InterviewProcess=u"二面")|Q(resume__Agency=user_id)).filter(NextUser=user_id,resume__Agency=None).filter(lockuser=F('resume__UserID')).values_list('resume__id',flat=True)
    resumes=Resume.objects.filter(UserID= user_id).exclude(Q(Status=u'淘汰')|Q(Status=u'已入职')).order_by('-Time')
    RESUIN=[]
    for resume in resumes:
       if resume in inters or resume.id in inters2:
           inte=1
       else:
           inte=0
       RESUIN.append([resume,inte])
           
    paginator=Paginator(resumes,15)
    page_num=request.GET.get('page')
    try:
        resumes=paginator.page(page_num)
    except PageNotAnInteger:
        resumes=paginator.page(1)
    except EmptyPage:
        resumes=paginator.page(paginator.num_pages)
    t=loader.get_template("talents_pool.html")
    c=Context({'RESUIN': RESUIN,'delete':delete})
    #Position.objects.annotate(Count(resumes))
    return HttpResponse(t.render(c))

#查询人才库
@login_required    
def search_talentform(request):
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    delete=[u'未处理']
    RESUIN=[]
    inters1 = Resume.objects.filter(Status=u"未处理")
    inters = inters1.filter(Q(UserID=user_id,Agency=None)|Q(Agency=user_id))
    inters2 = Interview.objects.filter(Q(resume__Status=u"一面",InterviewProcess=u"电话面试") | Q(resume__Status=u"二面",InterviewProcess=u"一面")| Q(resume__Status=u"三面",InterviewProcess=u"二面")|Q(resume__Agency=user_id)).filter(NextUser=user_id,resume__Agency=None).filter(lockuser=F('resume__UserID')).values_list('resume__id',flat=True)
    if 'PName' in request.GET and request.GET['PName']:
        q1=request.GET['PName']
        resumes=Resume.objects.filter(Q(PositionName__icontains=q1)|Q(CandidateName__icontains=q1)|Q(UserID__username__icontains=q1)|Q(CandidateSex__icontains=q1)|Q(CandidateAge__icontains=q1)|Q(Status__icontains=q1)).filter(UserID=user_id).order_by('-Time')
        for resume in resumes:
            if resume in inters or resume.id in inters2:
                inte=1
            else:
                inte=0
            RESUIN.append([resume,inte])
        return render_to_response('talents_pool.html',{'RESUIN': RESUIN, 'query': q1,'delete':delete})
    else:
        return HttpResponse('Please submit a search term.')

"""
简历一览
2015-11-13 by 李宝焜
增加简历过滤功能，在过滤基础上进行服务器端分页
"""
@login_required    
def resumemanage(request):
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    #获取该用户的所有权限 
    #2016-4-27 by 冯岩
    Powers=[]
    powers=Cor_user_Power.objects.filter(UserID=user_id)
    for power in powers:
        Powers.append(power.PowerID.id)

    q_name = ''
    q_sex = ''
    q_pos = ''
    q_pro = ''
    q_age = ''
    q_edu = ''
    age_id = 1
    exper_id = 3
    edu_id = 5
    date_id = 0
    departs=get_depart(user)
    positions = []
    temp = []
    for depart in departs:
        position=Position1.objects.filter(Q(Depart=depart.id)|Q(SecondDepartment=depart.id)).filter(Filing=0)
        positions=list(set(position).union(set(positions)))
        
    resumelist = Resume.objects.all()
    if 'Csex' in request.GET and request.GET['Csex']: 
        q_sex = request.GET['Csex']
        resumelist = resumelist.filter(CandidateSex__icontains=q_sex)
    if 'Cpos' in request.GET and request.GET['Cpos']:
        q_pos = request.GET['Cpos']
        resumelist = resumelist.filter(PositionName__icontains=q_pos)
    if 'Cpro' in request.GET and request.GET['Cpro']:
        q_pro = request.GET['Cpro']
        pro=q_pro.split('-')
        if len(pro) == 2:
            resumelist = resumelist.filter(CandidateProfile__gte=pro[0])
            resumelist = resumelist.filter(CandidateProfile__lte=pro[1])
        else:
            resumelist = resumelist.filter(CandidateProfile_gte=q_pro)
    if 'Cage' in request.GET and request.GET['Cage']:
        q_age = request.GET['Cage']
        age=q_age.split('-')
        if len(age)==2:
            resumelist = resumelist.filter(CandidateAge__gte=age[0])
            resumelist = resumelist.filter(CandidateAge__lte=age[1])
        else:
            resumelist = resumelist.filter(CandidateAge__gte=q_age)
    if 'Cedu' in request.GET and request.GET['Cedu']:
        q_edu = request.GET['Cedu']
        if q_edu:
            resumelist = resumelist.filter(Candidate_edu__gte=q_edu)
    if 'Cname' in request.GET and request.GET['Cname']:
        q_name = request.GET['Cname']
        resumelist = resumelist.filter(CandidateName__icontains=q_name)
    resumelist = resumelist.filter(Q(UserID__isnull=True)|Q(UserID__isnull=False,Status ="淘汰")).order_by('-Time')
    if not request.GET.get('page_size'):
        page_size = 15
    else:
        page_size = int(request.GET.get('page_size'))
    #根据request中的每页大小，对生成的简历列表进行切片
    paginator = Paginator(resumelist,page_size)
    page_num = request.GET.get('page')
    try:
        resumes = paginator.page(page_num)
    except PageNotAnInteger:
        resumes = paginator.page(1)
    except EmptyPage:
        resumes = paginator.page(paginator.num_pages)
    page_right = page_size * resumes.number if (page_size * resumes.number < len(resumelist)) else len(resumelist)
    page_left = page_size * (resumes.number - 1) + 1 if (resumes.number - 1) > 0 else 1
    t=loader.get_template("resumemanage.html")
    c=Context({'Powers':Powers,'resumes': resumes,'positions':positions,'resumelist':resumelist,'page_size':page_size,'record_count':len(resumelist),'age_id':age_id,'date_id':date_id,'exper_id':exper_id,'edu_id':edu_id,'Csex':q_sex,'Cpos':q_pos,'Cpro':q_pro,'Cage':q_age,'Cedu':q_edu,'page_right':page_right,'page_left':page_left,'Cname':q_name})
    return HttpResponse(t.render(c))
    
#简历排序  
def resume_sort(request,id):
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)

    #获取该用户的所有权限 
    #2016-4-27 by 冯岩
    Powers=[]
    powers=Cor_user_Power.objects.filter(UserID=user_id)
    for power in powers:
        Powers.append(power.PowerID.id)
    q1=''
    q2=''
    q3=''
    q4=''
    q5=''
    q6=''
    q=''
    date_id = 0
    age_id = 1
    exper_id = 3
    edu_id = 5
    
    departs=get_depart(user)
    positions = []
    temp = []
    for depart in departs:
        position=Position1.objects.filter(Q(Depart=depart.id)|Q(SecondDepartment=depart.id)).filter(Filing=0)
        positions=list(set(position).union(set(positions)))

    resumes=Resume.objects.filter(Q(UserID = None)|Q(UserID__isnull=False,Status ="淘汰"))
   
    if 'Csex' in request.GET and request.GET['Csex']: 
        q1=request.GET['Csex']
        resumes=resumes.filter(CandidateSex__icontains=q1)
    if 'Cpos' in request.GET and request.GET['Cpos']:
        q2=request.GET['Cpos']
        resumes=resumes.filter(PositionName__icontains=q2)
    if 'Cpro' in request.GET and request.GET['Cpro']:
        q3=request.GET['Cpro']
        pro=q3.split('-')
        if len(pro)==2:
            resumes= resumes.filter(CandidateProfile__gte=pro[0])
            resumes = resumes.filter(CandidateProfile__lte=pro[1])
        else:
            resumes=resumes.filter(CandidateProfile__gte=q3)
    if 'Cage' in request.GET and request.GET['Cage']: 
        q4=request.GET['Cage']
        age=q4.split('-')
        if len(age)==2:
            resumes = resumes.filter(CandidateAge__gte=age[0])
            resumes=resumes.filter(CandidateAge__lte=age[1])
        else:
            resumes=resumes.filter(CandidateAge__gte=q4)
    if 'Cedu' in request.GET and request.GET['Cedu']: 
        
        q5=request.GET['Cedu']
        if q5:
            resumes=resumes.filter(Candidate_edu__gte=q5)
   
    if 'Cname' in request.GET and request.GET['Cname']:
        q6 = request.GET['Cname']
        resumes = resumes.filter(CandidateName__icontains=q6)
    resumelist = resumes
    if id == '1':
        resumes=resumes.order_by('-CandidateAge')
        age_id = 2
    elif id =='2':
        resumes=resumes.order_by('CandidateAge')
        age_id= 1
    elif id == '3':
        resumes=resumes.order_by('-CandidateProfile')
        exper_id= 4
    elif id == '4':
        resumes=resumes.order_by('CandidateProfile')
        exper_id= 3
    elif id == '5':
        resumes=resumes.order_by('-Candidate_edu')
        edu_id = 6
    elif id == '6':
        resumes=resumes.order_by('Candidate_edu')
        edu_id = 5
    elif id == '0':
        resumes=resumes.order_by('-Time')
        date_id = 7
    elif id == '7':
        resumes=resumes.order_by('Time')
        date_id = 0
    if not request.GET.get('page_size'):
        page_size = 15
    else:
        page_size = int(request.GET.get('page_size'))
    paginator=Paginator(resumes,page_size)
    page_num=request.GET.get('page')
    try:
        resumes=paginator.page(page_num)
    except PageNotAnInteger:
        resumes=paginator.page(1)
    except EmptyPage:
        resumes=paginator.page(paginator.num_pages)
    page_right = page_size * resumes.number
    page_left = page_size * (resumes.number - 1) + 1 if (page_size * (resumes.number - 1) > 0) else 1
    p=1

    t=loader.get_template("resumemanage.html")
    c=Context({'Powers':Powers,'resumes':resumes,'positions':positions,'page_size':page_size,'record_count':len(resumelist),'p':p,'date_id':date_id,'age_id':age_id,'exper_id':exper_id,'edu_id':edu_id,'Csex':q1,'Cpos':q2,'Cpro':q3,'Cage':q4,'Cedu':q5,'page_right':page_right,'page_left':page_left,'Cname':q6})
    return HttpResponse(t.render(c))
#锁定简历
@login_required    
def input_pool(request,resume_id):
    
    session_id = request.COOKIES['sessionid']
    station=request.REQUEST.get('sta')    
    if station=="None":
        station=None
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    resume1 = Resume.objects.filter(id=resume_id).exclude(Status="未处理").exclude(Status="淘汰")
    if resume1:
        return HttpResponse("该简历已被锁定")
    else:
        Resume.objects.filter(pk=resume_id).update(UserID=user_id)
        Resume.objects.filter(pk=resume_id).update(Agency = None)
        Resume.objects.filter(pk=resume_id).update(Station=station)
        Resume.objects.filter(pk=resume_id).update(Status="未处理")
        Resume.objects.filter(pk=resume_id).update(LockTime=timezone.now())

        return HttpResponse("锁定成功")

#解除锁定
@login_required
def delete(request,resume_id):
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    Resume.objects.filter(pk=resume_id).update(UserID = None)
    Resume.objects.filter(pk=resume_id).update(Agency = None)
    Resume.objects.filter(pk=resume_id).update(Station = None)
    Resume.objects.filter(pk=resume_id).update(LockTime=None)
    return HttpResponse('成功解除锁定')
      
#锁定简历按钮保存id        
def mywrite(request,resume_id):
    with codecs.open(r'/home/resume/project/media/TMP/data', 'w', 'UTF-8') as f:
                          f.write(resume_id)
    return HttpResponse("ok")

#防止多次点击事件触发保护//废弃
def xie():
    with codecs.open(r'/home/resume/project/media/TMP/data', 'w', 'UTF-8') as f:
                          f.write("l")
    
#锁定简历按钮读取id并锁定        
def myread(request):    
    with codecs.open(r'/home/resume/project/media/TMP/data', 'r', 'UTF-8') as f:
               resume_id = f.read()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    resume1 = Resume.objects.filter(id=resume_id).exclude(UserID=None)
    station=request.REQUEST.get('sta')    
    if station=="None":
        station=None
    if resume1:
        return HttpResponse("该简历已被锁定")
    else:
        Resume.objects.filter(pk=resume_id).update(UserID=user_id)
        Resume.objects.filter(pk=resume_id).update(Station=station)
        Resume.objects.filter(pk=resume_id).update(LockTime=timezone.now())

        return HttpResponse("锁定成功")

#查找函数
def maych_with_position(postions,resumes):
    rt_list = []
    for position in postions:
        count_list = []
        need_pos_list = []
        length = len(position.PositionName)
        for resume in resumes:          
            if not resume.PositionName:
                continue
            count=0
            index=0      
            for i in range(length):
                if i+1 <=  length:
                    c = resume.PositionName.find(position.PositionName[i:i+1])
                    if c != -1:
                        count += 1
            if count > 0.7*length:
    
                if  len( count_list)!=0:
               
                    for i in count_list:
                        index += 1
                        if i < count:
                            break
                    count_list.insert(index-1,count)
                    need_pos_list.insert(index-1,resume)
                         
                else:
                    need_pos_list.append(resume)
                    count_list.append(count)
        rt_list.append([position,need_pos_list])
    return rt_list

#符合所发布职位的简历
@login_required
def find_suitable(request):
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    positions=Position1.objects.filter(UserID=user_id,Filing=0)
    length=len(positions)
    positionlength=range(length)
    resumes=[]
    if positions:
        resume1=Resume.objects.filter(UserID=None).order_by('-Time')
        resumes = maych_with_position(positions,resume1)
    t=loader.get_template("suitresume.html")
    c=Context({'resumes': resumes})
    return HttpResponse(t.render(c))

#在符合所发布职位中查询需要的简历
@login_required
def suitresume_search(request):
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    positions=Position1.objects.filter(UserID=user_id).filter(Filing=0)
    resumes=[]
    if positions:
        resume1=Resume.objects.filter(UserID=None).order_by('-Time')
        resumes2 = maych_with_position(positions,resume1)
        for position,resumelist in resumes2:
            re_list=[]
            for resume in resumelist:
                if 'Csex' in request.GET and request.GET['Csex']: 
                    q1=request.GET['Csex']
                    if resume.CandidateSex.find(q1) == -1:
                        continue
                    else:
                        pass
                if 'Cpos' in request.GET and request.GET['Cpos']:
                    q2=request.GET['Cpos']
                    if resume.PositionName.find(q2) == -1:
                        continue
                    else:
                        pass
                if 'Cpro' in request.GET and request.GET['Cpro']: 
                    q3=request.GET['Cpro']
                    if resume.CandidateProfile < int(q3):
                        continue
                    else:
                        pass
                if 'Cage' in request.GET and request.GET['Cage']: 
                    q4=request.GET['Cage']
                    if resume.CandidateAge < q4:
                        continue
                    else:
                        pass

                if 'Cedu' in request.GET and request.GET['Cedu']: 
                    q5=request.GET['Cedu']
                    if resume.Candidate_edu.find(q5) == -1:
                        continue
                    else:
                        pass
                re_list.append(resume)
            position_exam_id=str(position.id) +'id'
    #positions=Position.objects.filter(Q(Depart=fridepart.id)|Q(SecondDepartment=fridepart.id)).filter(Filing=0)

            resumes.append([position,re_list,position_exam_id])
        t=loader.get_template("suitresume.html")
        c=Context({'resumes': resumes})
        return HttpResponse(t.render(c))
    else:
        return HttpResponse('Please submit a search term.')

#复制别人发布的职位
@login_required
def copy_position(request,position_id):
    UserModel=get_user_model()
    #projects=Third_project.objects.all()
    #projects=Third_project.objects.filter(recruiter=user)
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    projects=Third_project.objects.filter(recruiter=user)
    approver = get_leader(user)
    departments = get_depart( user )
    errors=[]
    shu=0
    date=datetime.datetime.now()
    position=Position1.objects.get(pk=position_id)
    if position.Filing == 2 and position.UserID == position.Approver:
        Position1.objects.filter(pk=position_id).update(Filing = 3,States="已取消")
    PositionName=position.PositionName
    ExistingPersonNum=position.ExistingPersonNum
    NeedPersonNum=position.NeedPersonNum
    Workplace=position.Workplace
    ProjectName=position.ProjectName
    Salary=position.Salary
    add_reason = position.add_reason
    #HighSalary=position.HighSalary
    RecruitReason=position.RecruitReason
    WorkContent=position.WorkContent
    CandidateRequirement=position.CandidateRequirement
    RecruitWay=position.RecruitWay
    RecruitTime=position.RecruitTime
    Awarding=position.Awarding
    if request.method == 'POST':
        Awarding = request.POST.get('Awarding','')
        department = request.POST['SecondDepartment']
        NeedPersonNum = request.POST['staff_invite']
        ExistingPersonNum = request.POST['staff_now']
        ProjectName = request.POST['project']
        Workplace = request.POST['place']
        Salary = request.POST['salary']
        RecruitTime = request.POST['period']
        RecruitReason = request.POST['reason']
        RecruitWay = request.POST['RecruitWay']
        CandidateRequirement = request.POST['CandidateRequirement']
        WorkContent = request.POST['WorkContent']
        PositionName = request.POST['position']
        add_reason = request.POST.get('add_reason','')
        if PositionName and Salary and ExistingPersonNum and NeedPersonNum and Workplace and RecruitReason and WorkContent and CandidateRequirement and RecruitWay and RecruitTime  and  ProjectName:
            position1=Position1()
            shu=1
            position1.PositionName=PositionName
            position1.ExistingPersonNum=ExistingPersonNum
            position1.NeedPersonNum=NeedPersonNum
            position1.Workplace=Workplace
            position1.RecruitReason=RecruitReason
            position1.WorkContent=WorkContent
            position1.CandidateRequirement=CandidateRequirement
            position1.RecruitWay=RecruitWay
            position1.RecruitTime=RecruitTime
            position1.ProjectName=ProjectName
            depar=Department.objects.get(id = department)
            position1.Depart = depar.superior_department
            position1.SecondDepartment = depar
            position1.UserID = user
            approver=get_leader( user )
            position1.Approver = get_leader( user )
            position1.Awarding = Awarding
            position1.Salary=Salary
            position1.States="审批中"
            position1.add_reason=add_reason
            position1.Headline=timezone.now()
            position1.save()
            for i in range(10):
                if user:
                    user = get_leader(user)
                    if user:
                        examine = Examine()
                        examine.UserID = user
                        examine.PositionID = position1
                        if get_leader(user):
                            examine.next_approver = get_leader(user)
                        if user == position1.Approver:
                            examine.last_user = position1.UserID
                        else:
                            exa = Examine.objects.get(next_approver = user,PositionID = position1 )
                                                                  
                            examine.last_user = exa.UserID
                        examine.Is_resultful = 1
                        examine.conut=1
                        examine.save()
                    else:
                        break
                else:
                    break
        
            Examine.objects.filter(PositionID=position1,UserID=approver).update(Result="审批中")                
        else:
            errors="所有字段均不可以为空"
            return render_to_response('positionform.html',RequestContext(request,{'add_reason':add_reason,'shu':shu,'date':date,'errors':errors,'Awarding':Awarding,'PositionName':PositionName,'departments':departments,'ExistingPersonNum':ExistingPersonNum,'NeedPersonNum':NeedPersonNum,'Workplace':Workplace,'RecruitReason':RecruitReason,'WorkContent':WorkContent,'CandidateRequirement':CandidateRequirement,'RecruitWay':RecruitWay,'RecruitTime':RecruitTime,'Salary':Salary, 'projects':projects}))
    return render(request,'positionform.html',{'add_reason':add_reason,'shu':shu,'date':date,'departments':departments,'Awarding':Awarding,'PositionName':PositionName,'ExistingPersonNum':ExistingPersonNum,'NeedPersonNum':NeedPersonNum,'Workplace':Workplace,'WorkContent':WorkContent,'CandidateRequirement':CandidateRequirement,'RecruitTime':RecruitTime,'Salary':Salary, 'projects':projects})

#处理申请的招聘职位
@login_required   
def pending_application(request,position_id):
    position=Position1.objects.get(pk=position_id)
    return render(request,'pending_application.html',{'position':position })

#归档的职位
@login_required
def filing(request):    
    positions=Position1.objects.filter(Filing=1).order_by('-id')
    Position_Exam = []
    for position in positions:
        needperson=position.NeedPersonNum-position.recruitednum
        position_exam = Examine.objects.filter(PositionID = position.id)
        position_exam_id = str(position.id)+'id'
        Position_Exam.append([position,needperson,position_exam,position_exam_id])
    if not request.GET.get('page_size'):
        page_size = 15
    else:
        page_size = int(request.GET.get('page_size'))
    paginator=Paginator(Position_Exam,page_size)
    page_num=request.GET.get('page')
    try:
        Position_Exam=paginator.page(page_num)
    except PageNotAnInteger:
        Position_Exam=paginator.page(1)
    except EmptyPage:
        Position_Exam=paginator.page(paginator.num_pages)
    page_right = page_size * Position_Exam.number if (page_size * Position_Exam.number < len(Position_Exam)) else len(Position_Exam)
    page_left = page_size * (Position_Exam.number - 1)+ 1 if (page_size * (Position_Exam.number - 1) > 0) else 1
    t=loader.get_template("filing.html")
    c=Context({'Position_Exam': Position_Exam,'record_count':len(positions),'page_size':page_size,'page_left':page_left,'page_right':page_right,})
    return HttpResponse(t.render(c))

#达到截止时间是归档处理
def inspectiontime():
    date = now().date() + timedelta(days=-365)    
    inters = Position1.objects.filter(Headline__lte=date).exclude(Filing=1)
    for p in inters:
        Position1.objects.filter(pk = p.id).update(Filing = 1)

#待处理的职位申请，任务
@login_required
def handleposition(request):
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    positions=Position1.objects.filter(Approver=user_id,Filing=2).order_by('-id')
    if 'PName' in request.GET and request.GET['PName']: 
        q1 = ''
        q1=request.GET['PName']
        positions=positions.filter(Q(PositionName__icontains=q1)|Q(Workplace__icontains=q1)|Q(UserID__username__icontains=q1)|Q(Depart__name__icontains=q1)|Q(SecondDepartment__name__icontains=q1))
    Position_Exam = []
    for position in positions:
        position_exams = Examine.objects.filter(PositionID = position.id)
        position_exam_id = str(position.id)+'id'
        Position_Exam.append([position,position_exams,position_exam_id])
    t=loader.get_template("handleposition.html")
    c=Context({'Position_Exam':Position_Exam})
    return HttpResponse(t.render(c))

#我发布的岗位申请
@login_required
def handleingposition(request):    
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    positions=[]
    positions=Position1.objects.filter(UserID=user_id).order_by('-id')

    if 'PName' in request.GET and request.GET['PName']: 
        q1 = ''
        q1=request.GET['PName']
        positions=positions.filter(Q(PositionName__icontains=q1)|Q(Workplace__icontains=q1)|Q(UserID__username__icontains=q1)|Q(Depart__name__icontains=q1)|Q(SecondDepartment__name__icontains=q1))
    examines=Examine.objects.filter(PositionID__UserID=user_id)
    Position_Exam = []
    for position in positions:
        position_exams = Examine.objects.filter(PositionID = position.id)
        position_exam_id = str(position.id)+'id'
        Position_Exam.append([position,position_exams,position_exam_id])
    pids=[]
    for examine in examines:
        pids.append(examine.PositionID)
    if not request.GET.get('page_size'):
        page_size = 15
    else:
        page_size = int(request.GET.get('page_size'))
    paginator=Paginator(Position_Exam,page_size)
    page_num=request.GET.get('page')
    try:
        result=paginator.page(page_num)
    except PageNotAnInteger:
        result=paginator.page(1)
    except EmptyPage:
        result=paginator.page(paginator.num_pages)
    #page_right=page_size * result.number
    page_right = page_size * result.number if (page_size * result.number < len(result)) else len(result)
    page_left = page_size * (result.number - 1 )+ 1 if ((result.number - 1 ) > 0) else 1
    t=loader.get_template("handleingposition.html")
    c=Context({'positions': positions,'pids':pids,'Position_Exam':Position_Exam,'result':result,'page_size':page_size,'page_left':page_left,'page_right':page_right,'record_count':len(Position_Exam),})
    return HttpResponse(t.render(c))

@login_required
def handing(request,position_id):
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    examines=Examine.objects.filter(PositionID=position_id).filter(PositionID__Filing=2)
    t=loader.get_template("handing.html")
    c=Context({'examines': examines})
    return HttpResponse(t.render(c))

#发邮件时的页面
@login_required
def exrecord(request,position_id):    
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    position=Position1.objects.get(pk=position_id)
    examines=Examine.objects.filter(PositionID=position_id).filter(PositionID__Filing=2)
    t=loader.get_template("exrecord.html")
    c=Context({'examines': examines,'position':position})
    return HttpResponse(t.render(c))

#修改发布的职位
@login_required
def update_position(request,position_id):
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    approver = get_leader(user)
    departments = get_depart( user )
    date=datetime.datetime.now()
    errors=[]
    shu=0
    position=Position1.objects.get(pk=position_id)  
    PositionName=position.PositionName
    ExistingPersonNum=position.ExistingPersonNum
    NeedPersonNum=position.NeedPersonNum
    Workplace=position.Workplace
    ProjectName=position.ProjectName
    Salary=position.Salary
    RecruitReason=position.RecruitReason
    WorkContent=position.WorkContent
    CandidateRequirement=position.CandidateRequirement
    RecruitWay=position.RecruitWay
    RecruitTime=position.RecruitTime
    Awarding=position.Awarding
    if request.method == 'POST':
        Awarding = request.POST.get('Awarding','')
        department = request.POST['SecondDepartment']
        NeedPersonNum = request.POST['staff_invite']
        ExistingPersonNum = request.POST['staff_now']
        ProjectName = request.POST['project']
        Workplace = request.POST['place']
        Salary = request.POST['salary']
        RecruitTime = request.POST['period']
        RecruitReason = request.POST['reason']
        RecruitWay = request.POST['RecruitWay']
        CandidateRequirement = request.POST['CandidateRequirement']
        WorkContent = request.POST['WorkContent']
        PositionName = request.POST['position']
        if PositionName and Salary and ExistingPersonNum and NeedPersonNum and Workplace and RecruitReason and WorkContent and CandidateRequirement and RecruitWay and RecruitTime  and  ProjectName:
            shu=1
            position.PositionName=PositionName
            position.ExistingPersonNum=ExistingPersonNum
            position.NeedPersonNum=NeedPersonNum
            position.Workplace=Workplace
            position.RecruitReason=RecruitReason
            position.WorkContent=WorkContent
            position.CandidateRequirement=CandidateRequirement
            position.RecruitWay=RecruitWay
            position.RecruitTime=RecruitTime
            position.ProjectName=ProjectName
            depar=Department.objects.get(id = department)
            position.Depart = depar.superior_department
            position.SecondDepartment = depar
            position.UserID = user
            approver=get_leader( user )
            position.Approver = get_leader( user )
            position.Awarding = Awarding
            position.Salary=Salary
            position.Filing=2
            position.States="审批中"
            position.Headline=timezone.now()
            position.save()
            Examine.objects.filter(PositionID=position,UserID=approver).update(Result="审批中",comment="")
            Examine.objects.filter(PositionID=position).exclude(UserID=approver).update(Result="",comment="")
            Position1.objects.filter(id = position.id).update(States="未处理") 
        else:
            errors="所有字段均不可以为空"
            return render_to_response('positionform.html',RequestContext(request,{'shu':shu,'date':date,'errors':errors,'Awarding':Awarding,'PositionName':PositionName,'departments':departments,'ExistingPersonNum':ExistingPersonNum,'NeedPersonNum':NeedPersonNum,'Workplace':Workplace,'RecruitReason':RecruitReason,'WorkContent':WorkContent,'CandidateRequirement':CandidateRequirement,'RecruitWay':RecruitWay,'RecruitTime':RecruitTime,'Salary':Salary, 'ProjectName':ProjectName}))
    return render(request,'positionform.html',{'shu':shu,'date':date,'departments':departments,'Awarding':Awarding,'PositionName':PositionName,'ExistingPersonNum':ExistingPersonNum,'NeedPersonNum':NeedPersonNum,'Workplace':Workplace,'WorkContent':WorkContent,'CandidateRequirement':CandidateRequirement,'RecruitTime':RecruitTime,'Salary':Salary, 'ProjectName':ProjectName})

#一级部门总经理同意时发邮件所调用的函数
def set_Email(position_id):   
    position=Position1.objects.get(pk=position_id)
    email=Email.objects.get(mail="nt_si_hr@nantian.com.cn")
    password=base64.b16decode(email.password,False)
    to=[]
    #to.append('libaokun@nantian.com.cn')
    to.append('linana@nantian.com.cn')
    subject,from_email,auth_password=position.PositionName+u'职位申请',email.mail,password
    examines=Examine.objects.filter(PositionID=position_id).filter(PositionID__Filing=2)
    text_content = 'This is an important message.'
    t=loader.get_template("exrecord.html")
    c=Context({'position': position,'examines': examines})
    html_content = t.render(c)
    connection =mail.get_connection(username=from_email,password=auth_password,fail_silently=True)
    msg = EmailMultiAlternatives(subject, text_content,from_email, to,connection=connection)
    msg.attach_alternative((html_content), "text/html") 
    msg.send()

#邮件中同意按钮
def agree_application(request,position_id):
    position=Position1.objects.get(pk=position_id)
    if position.Filing==2:
        time=timezone.now()
        position=Position1.objects.get(pk=position_id)
        user=MyUser.objects.get(username="罗艳丽")
        positions=Position1.objects.filter(pk=position_id).update(Approver=user,States = "待发布",Filing=4)
        position=Position1.objects.get(pk=position_id)
        Examine.objects.filter(PositionID=position,next_approver=None).update(Result="同意",Time=time)
        email=Email.objects.get(mail="nt_si_hr@nantian.com.cn")
        password=base64.b16decode(email.password,False)
        subject,from_email, auth_password=u'您有一个待发布职位申请',email.mail,password
        to=['linana@nantian.com.cn']
        examines=Examine.objects.filter(PositionID=position_id)
        text_content = 'This is an important message.'
        t=loader.get_template("pub_position.html")
        c=Context({'position': position,'examines': examines})
        html_content = t.render(c)
        connection =mail.get_connection(username=from_email,password=auth_password,fail_silently=False)
        msg = EmailMultiAlternatives(subject, text_content,from_email, to,connection=connection)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return HttpResponse('您同意了该岗位申请')
    else:
        return HttpResponse('该岗位的已经被审批')

#邮件中不同意按钮
def disagree_application(request,position_id):
    position=Position1.objects.get(pk=position_id)
    exa = Examine.objects.get(PositionID=position,next_approver=None)
    if position.Filing==2:
        time=timezone.now()
        Position1.objects.filter(pk=position_id).update(Approver=exa.last_user,States="被退回")   
        Examine.objects.filter(PositionID=position,next_approver=None).update(Result="不同意",Time=time)
        return HttpResponse('您拒绝了该岗位申请')
    else:
        return HttpResponse('该岗位的已经被审批')

#第一个页面
def first_page(request):
    UserModel = get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user = UserModel.objects.get(id = user_id)
    #特殊处理
    Powers=[]
    powers=Cor_user_Power.objects.filter(UserID=user_id)
    for power in powers:
        Powers.append(power.PowerID.id)
    #处理过的招聘申请
    examines=Examine.objects.filter(UserID=user).exclude(Result=None).exclude(Result='审批中')   
    positions=[]
    for examine in examines:
        position=Position1.objects.get(pk=examine.PositionID.id)
        positions.append(position)
    handled_posit_num=len(positions)
    positions=Position1.objects.filter(UserID=user_id).filter(Filing=0)
    #待处理的岗位申请
    handlepositions=Position1.objects.filter(Approver=user_id,Filing=2)
    amount=len(handlepositions)
    #待发布的岗位申请
    publishing=len(Position1.objects.filter(Approver=user_id,Filing=4))
    #handleingposition=Position1.objects.filter(UserID=user_id,Filing=2)
    #我提出的岗位申请
    handleingposition=Position1.objects.filter(UserID=user_id)
    handleing=len(handleingposition)
    #我发起的面试
    resumes=Resume.objects.filter(UserID=user)
    len_resume=len(resumes)
    #我处理过的面试
    inters = Interview.objects.filter(user=user_id)
    len_inter=len(inters)
    #待处理的面试
    inters1 = Resume.objects.filter(Status=u"未处理")
    inters = inters1.filter(Q(UserID=user_id,Agency=None)|Q(Agency=user_id))
    inters2 = Interview.objects.filter(Q(resume__Status=u"一面",InterviewProcess=u"电话面试",InterStatus=u"通过")|Q(resume__Status=u"一面",InterviewProcess=u"电话面试",InterStatus=u"发邀请函") | Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"通过")| Q(resume__Status=u"二面",InterviewProcess=u"一面",InterStatus=u"发邀请函")| Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"通过")| Q(resume__Status=u"三面",InterviewProcess=u"二面",InterStatus=u"发邀请函")|Q(resume__Status=u"填写offer信息",InterviewProcess=u"二面",InterStatus=u"填写offer信息")|Q(resume__Status=u"填写offer信息",InterviewProcess=u"三面",InterStatus=u"填写offer信息")|Q(resume__Status=u"审批offer信息",InterviewProcess=u"二面",InterStatus=u"审批offer信息")|Q(resume__Status=u"审批offer信息",InterviewProcess=u"三面",InterStatus=u"审批offer信息")|Q(resume__Status=u"发邮件",InterviewProcess=u"二面",InterStatus=u"发邮件")|Q(resume__Status=u"发邮件",InterviewProcess=u"三面",InterStatus=u"发邮件")).filter(Q(NextUser=user_id,resume__Agency=None)|Q(resume__Agency=user_id)).filter(lockuser=F('resume__UserID')).filter(Active=1).filter(Turn=F('resume__Turn'))
    length=len(inters)+len(inters2)
    #待抢占的简历
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
    Task=amount+length+seizelength
    #待入职人员
    staffs = Resume.objects.filter(Status=u"发offer")
    stalength=len(staffs)
    #待下载的简历
    downresumes = []
    
    lock_user_id = import_ID.objects.all()
    for s in lock_user_id:           
        inter = Resume.objects.filter(SearchID=s.resume_id)
        if len(inter)==0:           
           downresumes.append(s)
    downrelength=len(downresumes)
    #返回网页
    t = loader.get_template("first_page.html")
    c = Context({'Powers':Powers,'stalength':stalength,'handleing':handleing,'member' : user,'seizelength':seizelength,'length':length,'positions':positions,'amount':amount,'Task':Task,'len_post':handleing,'handled_posit_num':handled_posit_num,'len_resume':len_resume,'len_inter':len_inter,'publishing':publishing})
    return HttpResponse(t.render(c))

#发布职位搜索
@login_required   
def position_search_form(request):
    positions=Position1.objects.filter(Filing=0)   
    if 'PName' in request.GET and request.GET['PName']: 
        q1 = ''
        q1=request.GET['PName']
        positions=positions.filter(Q(PositionName__icontains=q1)|Q(Workplace__icontains=q1)|Q(UserID__username__icontains=q1)|Q(Depart__name__icontains=q1)|Q(SecondDepartment__name__icontains=q1)).filter(Filing=0)
      
    Position_Exam = []
    for position in positions:
        position_exams = Examine.objects.filter(PositionID = position.id)
        needperson=position.NeedPersonNum-position.recruitednum
        position_exam_id = str(position.id)+'id'
        Position_Exam.append([position,needperson,position_exams,position_exam_id])
    if not request.GET.get('page_size'):
        page_size = 15
    else:
        page_size = int(request.GET.get('page_size'))
    paginator=Paginator(Position_Exam,page_size)
    page_num=request.GET.get('page')
    try:
        Position_Exam=paginator.page(page_num)
    except PageNotAnInteger:
        Position_Exam=paginator.page(1)
    except EmptyPage:
        Position_Exam=paginator.page(paginator.num_pages)
    t=loader.get_template("positionmanage.html")
    c=Context({'Position_Exam':Position_Exam,'page_size':page_size,})
    return HttpResponse(t.render(c))
    #else:
        #return render_to_response("positionmanage.html")
        #return HttpResponse('Please submit a search term.')

#归档职位搜索
@login_required
def Filing_search_form(request):
    positions=Position1.objects.filter(Filing=1)
    if 'PName' in request.GET and request.GET['PName']: 
        q1=request.GET['PName']
        positions=positions.filter(Q(PositionName__icontains=q1)|Q(Workplace__icontains=q1)|Q(UserID__username__icontains=q1)|Q(Depart__name__icontains=q1)|Q(SecondDepartment__name__icontains=q1)).filter(Filing=1)
    Position_Exam = []
    for position in positions:
        needperson=position.NeedPersonNum-position.recruitednum
        position_exams = Examine.objects.filter(PositionID = position.id)
        position_exam_id = str(position.id)+'id'
        Position_Exam.append([position,needperson,position_exams,position_exam_id])
    paginator=Paginator(Position_Exam,15)
    page_num=request.GET.get('page')
    try:
        Position_Exam=paginator.page(page_num)
    except PageNotAnInteger:
        Position_Exam=paginator.page(1)
    except EmptyPage:
        Position_Exam=paginator.page(paginator.num_pages)
    t=loader.get_template("filing.html")
    c=Context({'Position_Exam':Position_Exam})
    return HttpResponse(t.render(c))
    #else:
     #   return render_to_response("filing.html")


#发邮件通知人力去下载简历
def sentmail(zhilian_ID,job_ID,username):
    subject="招聘系统上有新的简历需要下载"
    email=Email.objects.get(mail="nt_si_hr@nantian.com.cn")
    password=base64.b16decode(email.password,False)
    from_email=email.mail
    recipient_list=['luoyanli@nantian.com.cn']
    auth_password=password
    text_content = 'This is an important message.'
    t=loader.get_template("resume_id.html")
    c=Context({'zhilian_ID': zhilian_ID,'job_ID':job_ID,'username':username})
    html_content = t.render(c)
    connection =mail.get_connection(username=from_email,password=auth_password,fail_silently=False)

#获得上级领导函数
def get_leader(user):
    sup_roles = []
    leader=''
    cor1=Cor_role_user_depart.objects.filter(UserID = user.id)
    for cor in cor1:
        role = Roles.objects.get(id=cor.RoleID.id)
        sup_role=role.superior_role
        sup_roles.append(sup_role)
    if sup_roles:
        for sup_role in sup_roles: 
            if sup_role:      
                cor2 = Cor_role_user_depart.objects.filter( RoleID = sup_role.id )
            #return cor.UserID.id
                for cor in cor2:
                    if user.id == cor.UserID.id:
                        continue
                    else:
                        leader = MyUser.objects.get(id = cor.UserID.id)            
    return leader
 
#获得部门函数
def get_depart( user ):
    departments = []
    roles=[]
    cors=Cor_role_user_depart.objects.filter( UserID = user.id)
    for cor1 in cors:
        role=Roles.objects.get( id = cor1.RoleID.id)

        roles.append(role)
    for role in roles:
        department=Department.objects.get( id = role.DepartmentID.id)
        departments.append(department)
    return departments

#获得角色函数
def get_role(user):
    roles=[]
    cors=Cor_role_user_depart.objects.filter( UserID = user.id)
    for cor1 in cors:
        role=Roles.objects.get( id=cor1.RoleID.id)
        roles.append(role)
    return roles
 
 #取消岗位申请
def cancel_position(request,position_id):
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    #reason=request.POST['reason']
    Position1.objects.filter(id = position_id).update(Filing=3,States="已取消",Approver=user.id)
    return HttpResponseRedirect('/talents/handleingposition')

#人力发布岗位
def publish_position(request,position_id):
    Position1.objects.filter(pk=position_id).update(Filing=0,Approver=None,States="已发布")
    return HttpResponseRedirect('/talents/publishing_position')

#已处理的招聘申请
def handledposition(request):
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    examines=Examine.objects.filter(UserID=user).exclude(Result='').exclude(Result='审批中').order_by('-PositionID')   
    positions=[]
    positionlist=[]
    roles = get_role(user)
    rule=True
    for role in roles:
        if role.name == '总经理':
            rule = False
            break
    for examine in examines:
        position=Position1.objects.get(pk=examine.PositionID.id)
        positions.append(position)
        positionlist.append(position)
    if 'PName' in request.GET and request.GET['PName']: 
        q1 = ''
        q1=request.GET['PName']
        positionlist=[]
        q_positions=Position1.objects.filter(Q(PositionName__icontains=q1)|Q(Workplace__icontains=q1)|Q(UserID__username__icontains=q1)|Q(Depart__name__icontains=q1)|Q(SecondDepartment__name__icontains=q1))
        #for position in q_positions:
            #if position in positions:
                #positionlist.append(position)
        positions = list(set(positions).intersection(set(q_positions)))
    Position_Exam = []
    recover=0 #标记是否可以追回
    for position in positions:
        recover=0
        position_exams = Examine.objects.filter(PositionID = position.id)
        position_exam_id = str(position.id)+'id'
        exas = position_exams.filter(UserID=user.id,PositionID__Filing=2)
        for exa in exas:
            pass
        if position.Filing == 2:
            if exa.last_user == position.Approver:
                recover=1
            if exa.next_approver == position.Approver and rule:
                recover=1
        Position_Exam.append([position,position_exams,position_exam_id,recover])
    t=loader.get_template("handledposition.html")
    c=Context({'Position_Exam':Position_Exam})
    return HttpResponse(t.render(c)) 

# 待发布的岗位申请
def publishing_position(request):
    positions=Position1.objects.filter(Filing=4).order_by('-id')
    Position_Exam=[]
    for position in positions:
    
        position_exams = Examine.objects.filter(PositionID = position.id)
        position_exam_id = str(position.id)+'id'

        Position_Exam.append([position,position_exams,position_exam_id])
    t=loader.get_template("publishing_position.html")
    c=Context({'Position_Exam':Position_Exam})
    return HttpResponse(t.render(c)) 

# 追回某次审批
def recover_examine(request,position_id):
    UserModel=get_user_model()
    session_id = request.COOKIES['sessionid']
    user_id = Session.objects.get(session_key=session_id).get_decoded().get('_auth_user_id')
    user=UserModel.objects.get(id=user_id)
    Position1.objects.filter(id=position_id).update(Approver=user,States="追回")
    Examine.objects.filter(UserID = user_id,PositionID = position_id).update(Result="审批中",comment=None)
    Examine.objects.filter(last_user = user_id,PositionID = position_id).update(Result="")
    return HttpResponseRedirect('/talents/handledposition')


