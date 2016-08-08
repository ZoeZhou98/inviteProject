# -*- coding: utf-8 -*-
#this demo is test for who named <td> and valign="top".

import sgmllib,sys,os,string
import re
html = """<head><title>Advice</title></head><body>
<p>The <a href="http://ietf.org">IETF admonishes:
<i>Be strict in what you <b>send</b>.</i></a></p>
<tr><td><table width="580" align="center" cellpadding="0" cellspacing="0" border="0">

		<tr><td colspan="3" height="10"></td></tr>

		<tr><td valign="top" width="1%" nowrap="nowrap"><span style="font-size:40px;font-weight:bold;color:#000000;">&#24222;&#35946;</span></td>

		<td valign="top" align="right">男  | 1992

		    年12月生   | 户口：河南南阳 | 现居住于北京 | 本科<br> 1年工作经验 

		    

					 <br>

					13521470493<br>

				  E-mail: <a href='mailto:13521470493@163.com'>13521470493@163.com</a> </td><td width="1%" nowrap><div class="photo" style="display:none;padding:0 5px 5px 5px;"></div></td></tr>

<tr><td colspan="3" height="10"></td></tr>

		</table></td></tr>
</body>
"""

tagstack = []
info_list = []
resume_info=[]
class ShowStructure(sgmllib.SGMLParser):
	is_a = ''
# 	def handle_starttag(self, tag, method,attrs): tagstack.append(tag)  
	#def handle_endtag(self, tag): tagstack.pop()  
#     def handle_data(self, data):  
#         if data.strip():  
#             for tag in tagstack: 
#                 sys.stdout.write('/'+tag)  
#             sys.stdout.write(' >> %s ' % data[:40].strip())
	def start_td(self,attrs):		
		valign = [v for k, v in attrs if k=='valign']		
		if valign == ['top']:
			self.is_a=1
	def end_td(self):
		if self.is_a == 1:
			self.is_a=""  
	def handle_data(self, data):
		
		if self.is_a == 1:
			info_list.append(data)
					
ShowStructure().feed(html)
for l in [0,1,2,3,4,5]:
	print info_list[l]

for info_list_number in [0,1,2,3,4]:
	if info_list_number == 0:
		n=re.match(r'([\s\S]*)\|([\s\S]*)\|([\s\S]*)\|([\s\S]*)\|\s+(.*)\s+\|([\s\S]*)',info_list[info_list_number])
		for i in [1,2,3,4,5,6]:
			if i == 1:
				m = re.match(r'^(.*)\s+[\s\S]*$',n.group(i))
				resume_info.append(m.group(1))
			elif i == 2:
				m = re.match(r'^\s+(.*)\s+$',n.group(i))
				resume_info.append(m.group(1))
			elif i  == 3:
				m = re.match(r'^\s+(.*)\s+(.*)\s+$',n.group(i))
				resume_info.append(m.group(1)+m.group(2))
			elif i == 4:
				m = re.match(r'^\s+(.*)\s+$',n.group(i))
				resume_info.append(m.group(1))
			elif i == 5:
				resume_info.append(n.group(i).decode('utf8'))
			elif i == 6:
				m = re.match(r'^\s+(.*)$',n.group(i))
				resume_info.append(m.group(1))
	elif info_list_number == 1:
		n=re.match(r'^\s(.*)\s+',info_list[info_list_number])
		resume_info.append(n.group(1))
	elif info_list_number == 2:
		#print info_list[info_list_number]
		n=re.match(r'^[\s\S]*?([0-9]*)$',info_list[info_list_number])
		resume_info.append(n.group(1))
	elif info_list_number == 3:
		n=re.match(r'^[\s\S]*?(E\-mail\:)\s$',info_list[info_list_number])
		resume_info.append(n.group(1))
	elif info_list_number == 4:
		n=re.match(r'(^[\s\S]*)',info_list[info_list_number])
		resume_info.append(n.group(1))
for p in [0,1,2,3,4,5,6,7,8,9]:
	print resume_info[p]
