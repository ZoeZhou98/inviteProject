# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 09:26:14 2015

@author: libaokun
"""

from django import forms
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput

class ChangepwdForm(forms.Form):  
    oldpassword = forms.CharField(  
        required=True,  
        label=u"原密码",  
        error_messages={'required': u'请输入原密码'},  
        widget=forms.PasswordInput(  
            attrs={  
                'placeholder':u"原密码",  
            }  
        ),  
    )   
    newpassword1 = forms.CharField(  
        required=True,  
        label=u"新密码",  
        error_messages={'required': u'请输入新密码'},  
        widget=forms.PasswordInput(  
            attrs={  
                'placeholder':u"新密码",  
            }  
        ),  
    )  
    newpassword2 = forms.CharField(  
        required=True,  
        label=u"确认密码",  
        error_messages={'required': u'请再次输入新密码'},  
        widget=forms.PasswordInput(  
            attrs={  
                'placeholder':u"确认密码",  
            }  
        ),  
     )  
    def clean(self):  
        if not self.is_valid():  
            raise forms.ValidationError(u"所有项都为必填项")  
        elif self.cleaned_data['newpassword1'] <> self.cleaned_data['newpassword2']:  
            raise forms.ValidationError(u"两次输入的新密码不一样")  
        else:  
            cleaned_data = super(ChangepwdForm, self).clean()  
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(  
        required=True,  
        label=u"用户名",  
        error_messages={'required': '请输入用户名'},  
        widget=forms.TextInput(  
            attrs={  
                'placeholder':u"用户名",  
            }  
        ),  
    )    
    password = forms.CharField(  
        required=True,  
        label=u"密码",  
        error_messages={'required': u'请输入密码'},  
        widget=forms.PasswordInput(  
            attrs={  
                'placeholder':u"密码",  
            }  
        ),  
    )
    def clean(self):  
        if not self.is_valid():  
            raise forms.ValidationError(u"用户名和密码为必填项")  
        else:  
            cleaned_data = super(LoginForm, self).clean()
'''
class Change_account_form(forms.Form):
	username = forms.CharField(
		required = True,
		label = u"用户名",
		error_messages={'required': u'请输入用户名'},
		widget = forms.TextInput(attrs={'value' : get_username,}),
	)
	mobile = forms.CharField(
		required = True,
		label = u"手机号",
		error_messages = {'requried':u'请输入手机号'},
		widget = forms.TextInput(attrs={'value':get_mobile,}),
	)
	email = forms.EmailField(
		required = True,
		label = u"邮箱",
		error_messages = {'required': u'请输入邮箱'},
		widget = forms.EmailInput(attrs={'value':get_email,}),
	)
	def clean(self):  
		if not self.is_valid():  
			raise forms.ValidationError(u"用户名、手机和邮箱是必填项")  
		else:  
			cleaned_data = super(Change_account_form, self).clean()
'''
