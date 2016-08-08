# -*- encoding: utf-8 -*-
from django.shortcuts import render,render_to_response
from manager.forms import DepartmentForm,RoleForm,PowerForm,RuleForm,Cor_role_user_departForm,Cor_user_powerForm,EmailForm,Cor_User_RuleForm,Third_projectForm,CustomerForm
from manager.models import Roles,Department,Power,Cor_role_user_depart,Cor_user_Power,Email,Cor_Rule_Power,Rule,Cor_User_Rule,Third_project,Customer
from django.http import HttpResponseRedirect
from accounts.models import MyUser
from accounts.forms import ChangepwdForm
from django.template import loader,Context,RequestContext
from django.http import HttpResponse
from accounts.views import add
import base64
def add_department(request):
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST) 
        if form.is_valid():
            Department=form.save(commit=False)
            Department.save()
            form.save_m2m()
            return HttpResponseRedirect('/manager/department_manage')
    else:
        form = DepartmentForm()
    return render(request, 'add_department.html', {'form': form})
def department_manage(request):
    departs=Department.objects.all()
    t=loader.get_template("department_manage.html")
    c=Context({'departs':departs})
    return HttpResponse(t.render(c))
def add_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST) 
        if form.is_valid():
            cd = form.cleaned_data
            Roles=form.save(commit=False)
            Roles.save()
            form.save_m2m()
            return HttpResponseRedirect('/manager/role_manage')
    else:
        form = RoleForm()
    return render(request, 'add_role.html', {'form': form})
def role_manage(request):
    roles=Roles.objects.all()
    t=loader.get_template("role_manage.html")
    c=Context({'roles':roles})
    return HttpResponse(t.render(c))
def add_power(request):
    if request.method == 'POST':
        form = PowerForm(request.POST) 
        if form.is_valid():
            Power=form.save(commit=False)
            Power.save()
            form.save_m2m()
            return HttpResponseRedirect('/manager/power_manage')
    else:
        form = PowerForm()
    return render(request, 'add_power.html', {'form': form})
def power_manage(request):
    powers=Power.objects.all()
    t=loader.get_template("power_manage.html")
    c=Context({'powers':powers})
    return HttpResponse(t.render(c))
        
def add_user_role(request):
    if request.method == 'POST':
        form = Cor_role_user_departForm(request.POST) 
        if form.is_valid():
            cd = form.cleaned_data
            Cor_role_user_depart=form.save(commit=False) 
            Cor_role_user_depart.save()
            form.save_m2m()
            add()
            return HttpResponseRedirect('/manager/user_manage')
    else:
        form = Cor_role_user_departForm()
    return render(request, 'add_user_role.html', {'form': form})
def user_role_manage(request,user_id):
    user_roles=Cor_role_user_depart.objects.filter(UserID=user_id)
    t=loader.get_template("user_role_manage.html")
    c=Context({'user_roles':user_roles})
    return HttpResponse(t.render(c))          
def add_user_power(request):
    if request.method == 'POST':
        form =Cor_user_powerForm(request.POST) 
        if form.is_valid():
            Cor_user_Power=form.save(commit=False)
            Cor_user_Power.save()
            form.save_m2m()
            return HttpResponseRedirect('/manager/user_manage')
    else:
        form = Cor_user_powerForm()
    return render(request, 'add_user_power.html', {'form': form})
def user_power_manage(request,user_id):
    user_powers=Cor_user_Power.objects.filter(UserID=user_id)
    t=loader.get_template("user_power_manage.html")
    c=Context({'user_powers':user_powers})
    return HttpResponse(t.render(c))         
def add_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST) 
        if form.is_valid():
            cd = form.cleaned_data
            Email=form.save(commit=False)
            Email.password =base64.b16encode(Email.password) 
            Email.save()                                                                
            form.save_m2m()
            return HttpResponse('添加成功')
    else:
        form = EmailForm()
    return render(request,'add_email.html', {'form': form})
def user_manage(request): 
    qname=''
    qdepart=''
    qrole=''
    qpower=''
    qrule =''
    user_role_power=[]
    users=MyUser.objects.filter(is_active = True)
    name_users = MyUser.objects.all()
    depart_users = MyUser.objects.all()
    role_users = MyUser.objects.all()
    rule_users = MyUser.objects.all()
    power_users = MyUser.objects.all()
    if 'uname' in request.GET and request.GET['uname']:
        qname = request.GET['uname']
        name_users = users.filter(username__icontains=qname)
    if 'udepart' in request.GET and request.GET['udepart']:
        depart_users = []
        qdepart = request.GET['udepart']
        roles=Roles.objects.filter(DepartmentID = qdepart)
        for role in roles:
            user_roles = Cor_role_user_depart.objects.filter(RoleID = role)
            for user_role in user_roles:
                user=MyUser.objects.get(pk = user_role.UserID_id)
                depart_users.append(user)

    if 'urole' in request.GET and request.GET['urole']:
        qrole = request.GET['urole']
        role_users = []
        user_roles= Cor_role_user_depart.objects.filter(RoleID__name__icontains = qrole)
        for user_role in user_roles:
            user=MyUser.objects.get(pk = user_role.UserID_id)
            role_users.append(user)

    if 'upower' in request.GET and request.GET['upower']:
        qpower = request.GET['upower']
        user_powers = Cor_user_Power.objects.filter(PowerID__name__icontains=qpower)
        power_users = []
        for user_power in user_powers:
            user=MyUser.objects.get(pk = user_power.UserID_id)
            power_users.append(user)
    if 'urule' in request.GET and request.GET['urule']:
        qrule = request.GET['urule']
        user_rules = Cor_User_Rule.objects.filter(RuleID__name__icontains=qrule)
        rule_users = []
        for user_rule in user_rules:
            user=MyUser.objects.get(pk = user_rule.UserID)
            rule_users.append(user)
    users = list(set(users) & set(name_users) & set(depart_users) & set(role_users) & set(rule_users) & set(power_users))
    departments=Department.objects.all()
    for user in users:
        roles = Cor_role_user_depart.objects.filter(UserID = user)
        powers = Cor_user_Power.objects.filter(UserID = user)
        rules = Cor_User_Rule.objects.filter(UserID = user)
        user_role_power.append([user,roles,rules,powers])
    t=loader.get_template("user_manage.html")
    c=Context({'user_role_power':user_role_power,'departments':departments,'qname':qname,'qdepart':qdepart,'qrole':qrole,'qrule':qrule,'qpower':qpower})
    return HttpResponse(t.render(c))     
def update(request,user_id):
    t=loader.get_template("updates.html")
    c=Context({'user_id':user_id})
    return HttpResponse(t.render(c))
def update_user_role(request,corrole_id):
    user_role = Cor_role_user_depart.objects.get(id=corrole_id)
    roles=Roles.objects.all()
    if request.method == 'POST':
        role = request.POST.get('role','')
        Cor_role_user_depart.objects.filter(id=corrole_id).update(RoleID=role)
        add()
        return HttpResponseRedirect('/manager/user_role_manage/'+str(user_role.UserID.id))
    else:
        return render_to_response('update_user_role.html',RequestContext(request,{'user_role':user_role,'roles':roles}))
    #return HttpResponseRedirect('/manager/user_role_manage/'+user_role.UserID)
def update_user_power(request,corpower_id):
    user_power= Cor_user_Power.objects.get(id=corpower_id)
    powers=Power.objects.all()
    if request.method == 'POST':
        power = request.POST.get('power','')
        Cor_user_Power.objects.filter(id=corpower_id).update(PowerID=power)
        return HttpResponseRedirect('/manager/user_power_manage/'+str(user_power.UserID.id))
    else:
        return render_to_response('update_user_power.html',RequestContext(request,{'user_power':user_power,'powers':powers}))
    return HttpResponseRedirect('/manager/user_power_manage/'+str(user_power.UserID.id))
def delete_user_role(request,corrole_id):
    user_role = Cor_role_user_depart.objects.get(id=corrole_id)
    Cor_role_user_depart.objects.filter(id=corrole_id).delete()
    add()
    return HttpResponseRedirect('/manager/user_role_manage/'+str(user_role.UserID.id))
def delete_user_power(request,corpower_id):
    user_power= Cor_user_Power.objects.get(id=corpower_id)
    Cor_user_Power.objects.filter(id=corpower_id).delete()
    return HttpResponseRedirect('/manager/user_power_manage/'+str(user_power.UserID.id))
def change_mail_pwd(request):
    
    if request.method == 'GET':
        form = ChangepwdForm()  
        return render_to_response('changepwd.html', RequestContext(request, {'form': form,}))
    else:
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            form = ChangepwdForm(request.POST)
            oldpassword=request.POST.get('oldpassword','')
            oldpassword=base64.b16encode(oldpassword)
            emails=Email.objects.filter(mail='nt_si_hr@nantian.com.cn',password=oldpassword)
            for email in emails:
                pass
            if email:
                newpassword=request.POST.get('newpassword1','')
                email.password = base64.b16encode(newpassword)
                email.save()
                return HttpResponse('密码修改成功')
            else:
                return render_to_response('changepwd.html', RequestContext(request, {'form': form,'oldpassword_is_wrong':True}))
        else:
            return render_to_response('changepwd.html', RequestContext(request, {'form': form,}))
 
def add_rule(request):
    if request.method == 'POST':
        form = RuleForm(request.POST)
        if form.is_valid():
            rule=form.save(commit=False)
            rule.save()
            powerlist = request.POST.getlist('PowerID')
            #rulename = request.POST.get('name')
            ruleID = Rule.objects.filter( name = rule.name )
            for id in ruleID:
                pass
            for power in powerlist:
                pow=Power.objects.get(pk=power)
                Cor_Rule_Power.objects.get_or_create(RuleID=id,PowerID=pow)           
            form.save_m2m()
            return HttpResponseRedirect('/manager/rule_power_manage')
    else:
        form = RuleForm()
        return render(request,'add_rule.html',{'form':form})

def rule_power_manage(request):
    rules = Rule.objects.all()
    rule_powers=[]
    for rule in rules:
       powers = Cor_Rule_Power.objects.filter(RuleID_id = rule.id)
       rule_powers.append([rule,powers])
    t=loader.get_template("rule_power_manage.html")
    c=Context({'rule_powers':rule_powers})
    return HttpResponse(t.render(c))

def delete_user(request,user_id):
    MyUser.objects.filter(pk = user_id).update(is_active = False)
    add()
    return HttpResponseRedirect('/manager/user_manage')

def delete_depart(request,depart_id):
    Department.objects.filter(pk=depart_id).delete()
    return HttpResponseRedirect('/manager/department_manage')

def delete_rule(request,rule_id):
    Rule.objects.filter(pk=rule_id).delete()
    Cor_Rule_Power.objects.filter(RuleID = rule_id).delete()
    return HttpResponseRedirect('/manager/rule_power_manage')

def delete_role(request,role_id):
    Roles.objects.filter(pk=role_id).delete()
    add()
    return HttpResponseRedirect('/manager/role_manage')

def update_depart(request,depart_id):
    depart=Department.objects.get(pk=depart_id)
    departs=Department.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        depart = request.POST.get('superior_depart','')
        level=request.POST.get('level','')
        Department.objects.filter(id=depart_id).update(superior_department=depart,level=level,name=name)
        return HttpResponseRedirect('/manager/department_manage/')
    else:
        return render_to_response('update_depart.html',RequestContext(request,{'depart':depart,'departs':departs}))

def update_role(request,role_id):
    role=Roles.objects.get(pk=role_id)
    roles=Roles.objects.all()
    departs=Department.objects.all()
    if request.method == 'POST':
        depart = request.POST.get('depart','')
        role = request.POST.get('superior_role','')
        Roles.objects.filter(id=role_id).update(superior_role=role,DepartmentID = depart)
        return HttpResponseRedirect('/manager/role_manage/')
    else:
        return render_to_response('update_role.html',RequestContext(request,{'departs':departs,'roles':roles,'role':role}))

def update_rule(request,rule_id):

    rule=Rule.objects.get(pk=rule_id)
    #Cor_Rule_Power.objects.filter(RuleID = rule_id).delete()
    powers=Power.objects.all()
    if request.method == 'POST':
        Cor_Rule_Power.objects.filter(RuleID = rule_id).delete()
        powerlist = request.POST.getlist('PowerID','')
        for power in powerlist:
            pow=Power.objects.get(pk=power)
            Cor_Rule_Power.objects.get_or_create(RuleID=rule,PowerID=pow) 
        #rule = request.POST.get('rule','')
        #Cor_user_Power.objects.filter(id=rule_id).update(superior_role=role,DepartmentID = depart)
        return HttpResponseRedirect('/manager/rule_power_manage/')
    else:
        return render_to_response('update_rule.html',RequestContext(request,{'rule':rule,'powers':powers}))
def add_user_rule(request):
    if request.method == 'POST':
        form =Cor_User_RuleForm(request.POST) 
        if form.is_valid():
            Cor_User_Rule=form.save(commit=False)
            Cor_User_Rule.save()
            rule_powers=Cor_Rule_Power.objects.filter(RuleID=Cor_User_Rule.RuleID)
            for rule_power in rule_powers:
                Cor_user_Power.objects.get_or_create(UserID=Cor_User_Rule.UserID,PowerID=rule_power.PowerID)

            form.save_m2m()
            return HttpResponseRedirect('/manager/user_manage')
    else:
        form = Cor_User_RuleForm()
    return render(request, 'add_user_rule.html', {'form': form})
def user_rule_manage(request,user_id):
    user_rules=Cor_User_Rule.objects.filter(UserID=user_id)
    t=loader.get_template("user_rule_manage.html")
    c=Context({'user_rules':user_rules})
    return HttpResponse(t.render(c)) 
def delete_user_rule(request,user_rule_id):
    user_rule = Cor_User_Rule.objects.get(id = user_rule_id)
    rule_powers=Cor_Rule_Power.objects.filter(RuleID=user_rule.RuleID)
    for rule_power in rule_powers:
        Cor_user_Power.objects.filter(PowerID=rule_power.PowerID,UserID = user_rule.UserID).delete()
    Cor_User_Rule.objects.filter(id=user_rule_id).delete()
    return HttpResponseRedirect('/manager/user_rule_manage/'+str(user_rule.UserID.id))
 
def update_user_rule(request,user_rule_id):
    user_rule = Cor_User_Rule.objects.get(id = user_rule_id)
    rules=Rule.objects.all()
    if request.method == 'POST':
        rule = request.POST.get('rule','')
        Cor_User_Rule.objects.filter(id=user_rule_id).update(RuleID=rule)
        rule_powers=Cor_Rule_Power.objects.filter(RuleID=user_rule.RuleID)
        for rule_power in rule_powers:
            Cor_user_Power.objects.filter(UserID=user_rule.UserID,PowerID=rule_power.PowerID).delete()
        rule_powers=Cor_Rule_Power.objects.filter(RuleID=user_rule.RuleID)
        for rule_power in rule_powers:
            Cor_user_Power.objects.get_or_create(UserID=user_rule.UserID,PowerID=rule_power.PowerID)
        return HttpResponseRedirect('/manager/user_rule_manage/'+str(user_rule.UserID.id))
    else:
        return render_to_response('update_user_rule.html',RequestContext(request,{'user_rule':user_rule,'rules':rules}))
    return HttpResponseRedirect('/manager/use_rule_manage/'+str(user_rule.UserID.id))
def add_pro(request):
    
    if request.method == 'POST':
        form = Third_projectForm(request.POST) 
        if form.is_valid():
            Third_project=form.save(commit=False)
            Third_project.save()
            form.save_m2m()
            return HttpResponseRedirect('/manager/project_manage')
    else:
        form = Third_projectForm()
    return render(request, 'add_pro.html', {'form': form})

def project_manage(request):
    projects=Third_project.objects.all()
    t=loader.get_template("project_manage.html")
    c=Context({'projects':projects})
    return HttpResponse(t.render(c))

def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST) 
        if form.is_valid():
            Customer=form.save(commit=False)
            Customer.save()
            form.save_m2m()
            return HttpResponseRedirect('/manager/customer_manage')
    else:
        form = CustomerForm()
    return render(request, 'add_customer.html', {'form': form})
def customer_manage(request):
    customers=Customer.objects.all()
    t=loader.get_template("customer_manage.html")
    c=Context({'customers':customers})
    return HttpResponse(t.render(c))
def update_pro(request,pro_id):
    project = Third_project.objects.get(id = pro_id)
    users=MyUser.objects.filter(is_active = True)
    customers = Customer.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name','')
        project_manager = request.POST.get('project_manager','')
        recruiter = request.POST.get('recruiter','') 
        customer = request.POST.get('customer','')
        Third_project.objects.filter(id = pro_id).update(name=name)
        #project_managers=Myuser.objects.filter(username=project_manager)
        #recruiters = Myuser.objects.filter(username=recruiter) 
        #customer = Customer.object.filter(id=)
        Third_project.objects.filter(id=pro_id).update(project_manager=project_manager)
        Third_project.objects.filter(id=pro_id).update(recruiter=recruiter,customer=customer)
        return HttpResponseRedirect('/manager/project_manage/')
    else:
        return render_to_response('update_project.html',RequestContext(request,{'project':project,'users':users,'customers':customers}))
    
