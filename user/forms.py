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
	gender = forms.CharField(	max_length=2,				
								widget=forms.TextInput(
									attrs={'placeholder': '男 or 女', 'value': '男', }
									)
							)

	weight = forms.FloatField( widget=forms.NumberInput(
									attrs={'placeholder': '请输入体重 单位kg', 'value': 0}
									)
								)

	birthday = forms.CharField(	widget=forms.TextInput(),
							max_length=40
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

# 新增或修改事务类型
class EventTypeForm(forms.Form):
	name = forms.CharField(	widget=forms.TextInput(
								attrs={'placeholder': '请输入用户名', 'value': '', 'required': 'required',}
								),  
							max_length=20, 
							error_messages={'required': '用户名不能为空',}
							)
	typeName = forms.CharField(	widget=forms.TextInput(
								attrs={'placeholder': '请输入事务类型名称', 'value': '', 'required': 'required',}
								),  
							max_length=20, 
							error_messages={'required': '事务类型名称不能为空',}
							)
	description = forms.CharField(	widget=forms.TextInput(
								attrs={'placeholder': '请输入事务类型描述', 'value': '', 'required': 'required',}
								),  
							max_length=100, 
							error_messages={'required': '描述不能为空',}
							)

class EventTypeDeleteForm(forms.Form):
	name = forms.CharField(	widget=forms.TextInput(
								attrs={'placeholder': '请输入用户名', 'value': '', 'required': 'required',}
								),  
							max_length=20, 
							error_messages={'required': '用户名不能为空',}
							)
	typeName = forms.CharField(	widget=forms.TextInput(
								attrs={'placeholder': '请输入事务类型名称', 'value': '', 'required': 'required',}
								),  
							max_length=20, 
							error_messages={'required': '事务类型名称不能为空',}
							)

class EventForm(forms.Form):
	name = forms.CharField(	widget=forms.TextInput(
								attrs={'placeholder': '请输入用户名', 'value': '', 'required': 'required',}
								),  
							max_length=20, 
							error_messages={'required': '用户名不能为空',}
							)
	title = forms.CharField(	widget=forms.TextInput(
								attrs={'placeholder': '请输入标题', 'value': '', 'required': 'required',}
								),  
							max_length=20, 
							error_messages={'required': '标题不能为空',}
							)
	description = forms.CharField(	widget=forms.TextInput(
								attrs={'placeholder': '请输入描述', 'value': '', 'required': 'required',}
								),  
							max_length=200, 
							error_messages={'required': '描述不能为空',}
							)
	typeName = forms.CharField(	widget=forms.TextInput(
								attrs={'placeholder': '请输入事务类型名称', 'value': '', 'required': 'required',}
								),  
							max_length=20, 
							error_messages={'required': '事务类型名称不能为空',}
							)
	userLevel = forms.ChoiceField(	choices=((0, '0'), (1, '1'), (2, '2'), (3, '3')),	# 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
								initial=0,							# 默认选中第一个option
								widget=forms.RadioSelect			# 插件表现形式为单选按钮
							)
	userStartTime = forms.CharField(	widget=forms.TextInput(),
							max_length=40
							)
	userEndTime = forms.CharField(	widget=forms.TextInput(),
							max_length=40
							)
	length = forms.IntegerField(	widget=forms.NumberInput(
									attrs={'placeholder': '请输入事务预计时长 单位分钟', 'value': 0}
									)
							)

class EventDeleteForm(forms.Form):
	name = forms.CharField(	widget=forms.TextInput(
								attrs={'placeholder': '请输入用户名', 'value': '', 'required': 'required',}
								),  
							max_length=20, 
							error_messages={'required': '用户名不能为空',}
							)
	pk = forms.IntegerField()

class EventCancelForm(forms.Form):
	name = forms.CharField(	widget=forms.TextInput(
								attrs={'placeholder': '请输入用户名', 'value': '', 'required': 'required',}
								),  
							max_length=20, 
							error_messages={'required': '用户名不能为空',}
							)
	pk = forms.IntegerField()
	cancelOrReactive = forms.ChoiceField(	choices=((0, 'cancel'), (1, 'Reactive')),
								initial=0,
								widget=forms.RadioSelect
							)