# -*- coding: utf-8 -*-
import codecs
import sgmllib
import re
resume_list=[]
resume_info={'path':'','registered_addr':'','name':'', 'sex':'', 'age':'', 'work_experience':'', 'now_addr':'', 'id':'', 'phone':'', 'E-mail':'', 'education':'','marital':''}
class ShowStructure(sgmllib.SGMLParser):
    ''' 解析智联的html文件的类,继承自sgmllib.SGMLParser.
    
    instructions:单纯的解析智联的html简历，没有别的功能
    
    Attributes: 
        p:    值改变，表示遇到了<p>
        span:    值改变，表示遇到了<span>
        td:    值改变，表示遇到了<td>
        strong:    值改变，表示遇到了<td>
    Returns:
       NO retrun
        
    Raises:
        not found
    
    '''
    div=''
    p=''
    strong=''
    span=''
    def start_div(self,attrs):
        div_class = [v for k, v in attrs if k=='class'] 
        if div_class==["summary-top"]:
            self.div=1
        if div_class==["summary-bottom"]:
            self.div=2
        if div_class==["resume-left-tips-span"]:
            self.div=3
        if div_class==["main-title-fl fc6699cc"]:
            self.div=4
    def end_div(self):
        if self.div != '':
            self.div=''
    def start_span(self,attrs):
        span_class = [v for k, v in attrs if k=='class'] 
        self.span=1
        if span_class==["resume-left-tips-id"]:
            self.span=3
    def end_span(self):
        if self.span != '':
            self.span=''       
    def handle_data(self, data):
        global resume_list

        global resume_info
        if self.div==1 and self.span==1:
            resume_list.append(data)
        if self.div==2 :
            m = re.match(r'^[\s\S]{3}([0-9]{11})$',data)
            if m!=None:
                resume_info['phone']=m.group(1)

            m = re.match(r'^([\s\S]*?@[\s\S]*?\.com)$',data)
            if m!=None:
                resume_info['E-mail']=m.group(1)
        if self.div==3 and self.span==3:
            m = re.match(r'^ID:([\s\S]*)$',data)
            if m!=None:
                resume_info['id']=m.group(1)
        if self.div==4:
            resume_info["name"]=data
#         if self.strong==1 and self.td==1 and self.p==1:
#             resume_list.append(data)
#         if self.td==1 and self.p==2 and self.span==1:
#             phone_and_email.append(data)
#         if self.td==1 and self.p==2 and self.span==2:
#             phone_and_email.append(data)
#         if self.td==2 and self.p==3 and self.strong==1 and self.span==3:
#             name=data
#         if self.p==4 and self.span==4 and len(data)>10:
#             m = re.match(r'^([0-9a-zA-Z\_]+)[\s\S]*?$',data)
#             if m!=None:
#                 searchid=m.group(1)

# def parser_with_zhilian(txt):
#     '''外部调用解析的接口，主要是将核实的数据填入字典，解析功能在ShowStructure()中完成。
#     
#     Args:
#         txt:需要解析的文本
#     Returns:
#         resume_info:装有所需数据的dict
#     '''
def parser_with_zhilian(txt):
    global resume_list
    global resume_info

    resume_list=[]
    resume_info={'path':'','registered_addr':'','name':'', 'sex':'', 'age':'', 'work_experience':'', 'now_addr':'', 'id':'', 'phone':'', 'E-mail':'', 'education':'','marital':''}
    ShowStructure().feed(txt)
    
    # print resume_list[0],resume_list[9],resume_list[18],resume_list[27]
    if len(resume_list)>=1:
        resume_info['sex']=resume_list[0]
    if len(resume_list)>=2:
        m = re.match(r'^[\s\S]*?\(([0-9]{4})[\s\S]*?([0-9]+)[\s\S]*\)$',resume_list[1])
        if m!=None:
            resume_info['age'] ='.'.join([m.group(1),m.group(2)])
            print 'age:',resume_info['age']
    if len(resume_list)>=3:
        if resume_list[2].find(u'大专')!=-1 or resume_list[2].find(u'本科')!=-1 or resume_list[2].find(u'硕士')!=-1 or resume_list[2].find(u'博士')!=-1 or resume_list[2].find(u'博士后')!=-1:
            resume_info['education']=resume_list[2]
        else:
            resume_info['work_experience']=resume_list[2]
    
    
    
#     for i in resume_info.keys():
#         print i,resume_info[i]

    return resume_info
    
