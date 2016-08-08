#encoding=UTF-8
from django import forms  
from accounts.models import MyUser
from django.db import models
from talents.models import Position,Examine
from django.forms import ModelForm

RECRUITWAY_CHOICES=(
                        (1,u'1.在招聘网站发布职位'),
                        (2,u'2.伯乐奖职位'),
                        (3,u'3.其他渠道'),
                        )
RECRUITREASEON_CHOICES=(
                            (1,'1.原有人员离职后增补人员'),
                            (2,'2.业务拓展后新增工作岗位'),
                            (3,'3.其他情况'),
                            )
IS_ACCEPT_CHOICES=(
                        (1,u'是'),
                        (0,u'否'),
                    )
RESULT_CHOICES=(
                    (u'同意',u'同意'),
                    (u'不同意',u'不同意'),
)
class PositionForm(ModelForm):
    #PositionID = forms.IntegerField()
    PositionName = forms.CharField(max_length=100,required=True,error_messages={'required': u'职位不能为空'},label=u'* 职位名称 ')
#    UserID = forms.IntegerField(required=True,label=u'用户编号')
    Phone1 = forms.CharField(max_length=11,required=True,error_messages={'required': u'电话不能为空'},label=u'* 联系电话  ')
    #Department = forms.CharField(max_length=32,required=True,error_messages={'required': u'部门名称不能为空'},label=u'* 一级部门')
    #SecondDepartment = forms.CharField(max_length=32,required=True,error_messages={'required': u'二级部门名称不能为空'},label=u'* 二级部门 ')
    ExistingPersonNum = forms.IntegerField(label=u'* 该岗位现有人数 ',required=True,min_value=0,error_messages={'min_value': u'请输入一个正数','required': u'现有人数不可为空'})
    NeedPersonNum = forms.IntegerField(label=u'* 招聘人数 ',required=True,error_messages={'required': u'招聘人数不能为空'},min_value=1)
    Workplace = forms.CharField(max_length=32,label=u'* 工作地点 ',required=True,error_messages={'required': u'工作地点不能为空'})
    ProjectName = forms.CharField(max_length=32,label=u'项目组名称',required=False)
    LowSalary = forms.IntegerField(label=u'最低工资 ',required=False,min_value=0,error_messages={'min_value': u'请输入一个正数'})
    HighSalary = forms.IntegerField(label=u'最高工资 ',required=False,min_value=0,error_messages={'min_value': u'请输入一个正数'})
    RecruitReason = forms.ChoiceField(choices=RECRUITREASEON_CHOICES,label=u'* 招聘原因 ')
    WorkContent = forms.CharField(label=u'* 工作内容 ',required=True,error_messages={'required': u'工作内容不能为空'},widget=forms.Textarea(  attrs={ 'placeholder':u"具体可以参考职位说明书",} ))
    #CandidateRequirement = forms.CharField(label=u'* 招聘要求 ',required=True,error_messages={'required': u'招聘要求不能为空'},widget=forms.Textarea(  attrs={ 'placeholder':u"请顺序写清性别、年龄、学历、经历、特殊技能要求", } ),)  
#    RecruitWay = forms.ChoiceField(choices=RECRUITWAY_CHOICES,label=u'招聘方式 ')
    RecruitTime = forms.DateTimeField(label=u'* 开始日期 ',required=True,error_messages={'required': u'开始日期不能为空'})
    Headline = forms.DateTimeField(label=u'* 截止日期 ',required=True,error_messages={'required': u'截止日期不能为空'})
  #  Approver = forms.ModelChoiceField(queryset=MyUser.objects.all(),label=u"下一步面试官",required=False,error_messages={'required': u'审批人'})
   # Accept=forms.ChoiceField(choices=IS_ACCEPT_CHOICES,label=u'是否自选简历')
 #   Awarding=forms.IntegerField(label=u'伯乐奖金额',required=False)
    class Meta:
        model = Position
        fields= ('PositionName','Phone1','ExistingPersonNum','NeedPersonNum', 'Workplace','ProjectName','LowSalary','HighSalary','RecruitReason','WorkContent','RecruitTime','Headline')

class ExamineForm(ModelForm):
    Result=forms.ChoiceField(choices=RESULT_CHOICES,label=u'审批结果',required=True,error_messages={'required': u'审批结果不能为空'})
    #Time=forms.DateTimeField(label=u'处理时间',required=True,error_messages={'required': u'时间不能为空'})
    comment=forms.CharField(label=u'* 审批意见',required=True,error_messages={'required':u'审批意见不能为空'},widget=forms.Textarea())   
   # Approver = forms.ModelChoiceField(queryset=MyUser.objects.all(),label=u"下一步审批人",required=False,error_messages={'required': u'审批人'})
    class Meta:
        model=Examine
        fields=('Result','comment')
