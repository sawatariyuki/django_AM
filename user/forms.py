from django import forms
from django.forms import widgets

# 注册
class RegisterForm(forms.Form):
	name = forms.CharField(	widget=forms.TextInput(
								attrs={'placeholder': '请输入用户名', 'value': '', 'required': 'required',}
								),  
							max_length=20, 
							error_messages={'required': '用户名不能为空',}
							)
	pw = forms.CharField(	widget=forms.PasswordInput(
								attrs={'placeholder': '请输入密码', 'value': '', 'required': 'required',}
								),  
							min_length=8, 
							max_length=20, 
							error_messages={'required': '密码不能为空',}
							)
	pwConfirm = forms.CharField(	widget=forms.PasswordInput(
										attrs={'placeholder': '请确认密码', 'value': '', 'required': 'required',}
										),  
									min_length=8, 
									max_length=20, 
									error_messages={'required': '密码不能为空',}
									)
	email = forms.EmailField(	widget=forms.TextInput(
									attrs={'class': 'form-control', 'placeholder': '请输入邮箱', 'value': '', 'required': 'required',}
									), 
								error_messages={'required': '邮箱不能为空',}
								)

# 激活用户
class ActivateForm(forms.Form):
	name = forms.CharField(	widget=forms.TextInput(
								attrs={'placeholder': '请输入用户名', 'value': '', 'required': 'required',}
								), 
							max_length=20, 
							error_messages={'required': '用户名不能为空',}
							)
	code = forms.CharField(	widget=forms.TextInput(
								attrs={'placeholder': '请输入激活码', 'value': '', 'required': 'required',}
								), 
							min_length=6, 
							max_length=6, 
							error_messages={'required': '激活码不能为空',}
							)

# 登录
class LoginForm(forms.Form):
	name = forms.CharField(	widget=forms.TextInput(
								attrs={'placeholder': '请输入用户名', 'value': '', 'required': 'required',}
								), 
							max_length=20,
							error_messages={'required': '用户名不能为空',}
							)
	pw = forms.CharField(	widget=forms.PasswordInput(
								attrs={'placeholder': '请输入密码', 'value': '', 'required': 'required',}
								), 
							min_length=8, 
							max_length=20, 
							error_messages={'required': '密码不能为空',}
							)

# 修改用户详情
class DetailForm(forms.Form):
	name = forms.CharField(	widget=forms.TextInput(
								attrs={'placeholder': '请输入用户名', 'value': '', 'required': 'required',}
								),  
							max_length=20, 
							error_messages={'required': '用户名不能为空',}
							)
	gender = forms.ChoiceField(	choices=(('男', '男'), ('女', '女'),),	# 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
								initial='男',							# 默认选中第一个option
								widget=forms.RadioSelect			# 插件表现形式为单选按钮
							)

	weight = forms.FloatField( widget=forms.NumberInput(
									attrs={'placeholder': '请输入体重 单位kg', 'value': 0}
									)
								)

	birthday = forms.DateTimeField( widget=forms.DateTimeInput(
										attrs={'type': 'date'}
										)
									)
	birthplace = forms.CharField(	max_length=100, 
									widget=forms.TextInput(
										attrs={'placeholder': '请输入出生地', 'value': '未填写', }
										)
								)
	liveplace = forms.CharField(	max_length=100, 
									widget=forms.TextInput(
										attrs={'placeholder': '请输入暂住地', 'value': '未填写', }
										)
								)

