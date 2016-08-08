# -*- coding: utf-8 -*-
import re
import codecs
import sgmllib

resume_list=[]
resume_info={'path':'','registered_addr':'','name':'', 'sex':'', 'age':'', 'work_experience':'', 'now_addr':'', 'id':'', 'phone':'', 'E-mail':'', 'education':'','marital':''}
class ShowStructure_51(sgmllib.SGMLParser):
    ''' 解析51job的html文件的类,继承自sgmllib.SGMLParser.
    
    instructions:单纯的解析51的html简历，没有别的功能
    
    Attributes: 
        p:    值改变，表示遇到了<p>
        span:    值改变，表示遇到了<span>
        td:    值改变，表示遇到了<td>

    Returns:
       resume_info 是一个字典，保存了需要的数据 
        
    Raises:
        not found
    
    '''
    p=''
    span=''
    td=''
    b=""
    def start_td(self,attrs): 
        style = [v for k, v in attrs if k=='style'] 
        colspan =[v for k, v in attrs if k=='colspan'] 
        width = [v for k, v in attrs if k=='width']
        rowspan = [v for k, v in attrs if k=='rowspan']
        for i in style:
            if  i.find('border:none;border-bottom:dashed #88B4E0 1.0pt;mso-border-bottom-alt:')!=-1 and i.find('dashed #88B4E0 .75pt;padding:6.0pt 0cm 0cm 6.0pt;')!=-1:
                self.td=1
            if width==["17%"] and i.find('width:17.0%;padding:0cm 0cm 0cm 0cm;')!=-1 and i.find('height')!=-1:
                self.td=4
        if colspan==['4'] and style==['padding:0cm 0cm 0cm 0cm;height:19.5pt']:
            self.td=2
        if colspan==['3'] and style==['padding:0cm 0cm 0cm 0cm;height:15.0pt']:
            self.td=3
        
    def end_td(self):
        if self.td!='':
            self.td=''
    def start_p(self,attrs): 
        cls = [v for k, v in attrs if k=='class'] 
        style = [v for k, v in attrs if k=='style'] 
        if cls==['MsoNormal'] :
            self.p=2
        if cls==['MsoNormal'] and style==['text-align:center']:
            self.p=3
    def end_p(self):
        if self.p!='':
            self.p=''
    def start_b(self,attrs): 
        self.b=1
    def end_b(self):
        if self.b!='':
            self.b=''
    
    def start_span(self,attrs): 
        style = [v for k, v in attrs if k=='style'] 
        for i in style:
            if i.find('font-size:19.0pt;mso-ascii-font-family:')!=-1 and i.find('Arial;mso-hansi-font-family:Arial;mso-bidi-font-fa')!=-1:
                self.span=1
            if i.find('font-size:9.0pt;font-family:')!=-1 and i.find('"Arial')!=-1:
                self.span=3
        if style==['font-size:9.0pt;font-family:"Arial",sans-serif']:
            self.span=2
    def end_span(self):
        if self.span!='':
            self.span=''
    def handle_data(self, data):

        global resume_list
        global resume_info
        if self.b==1 and self.span==1 and self.td==1:
            resume_info['name']=data
        if self.td==2 and self.p==2 :
            resume_list.append(data)
        if self.td==3 and self.span==3 and self.p==2:
            m = re.match(r'^([\s\S]*?[0-9]{11})$',data)
            if m!=None:
                resume_info['phone']=m.group(1)

            m = re.match(r'^([\s\S]*?@[\s\S]*?\.com)$',data)
            if m!=None:
                resume_info['E-mail']=m.group(1)
        if self.td==4  and self.p==3: 
            m = re.match(r'^[\s\S]*?ID:([0-9]+)[\s\S]*?$',data)
            if m!=None:
                resume_info['id']=m.group(1)
                print data
def parser_with_51(txt):
    '''外部调用解析的接口，主要是将核实的数据填入字典，解析功能在ShowStructure_51()中完成。
     
    Args:
    txt:需要解析的文本
    Returns:
    resume_info:装有所需数据的dict
    '''
    global resume_list
    global resume_info
    
    txt=txt.decode('gb2312','ignore').encode('UTF-8','ignore')
    txt=txt.replace('gb2312','utf-8') 
     
    
    resume_list=[]
    str_info=''
    resume_info={'path':'','registered_addr':'','name':'', 'sex':'', 'age':'', 'work_experience':'', 'now_addr':'', 'id':'', 'phone':'', 'E-mail':'', 'education':'','marital':''}
    ShowStructure_51().feed(txt)
     
    for i in range(len(resume_list)):
        str_info+=resume_list[i]
     
    buf=str_info.split(' |')
    resume_info['work_experience']=buf[0]
    resume_info['sex']=buf[1]
    m = re.match(r'^[\s\S]*?([0-9]{4})[\s\S]*?([0-9]+)[\s\S]*$',buf[2])
    if m!=None:
        resume_info['age']= '.'.join([m.group(1),m.group(2)])

#     for i in resume_info:
#         print i,resume_info[i]
    return resume_info
# f=open('51job_jinke(311417926).htm','r')
# txt=f.read()
# dict=parser_with_51(txt)
# for i in resume_info:
#         print i,resume_info[i]
