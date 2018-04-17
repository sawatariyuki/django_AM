from django import forms

class RegisterForm(forms.Form):
	name = forms.CharField(	widget=forms.TextInput(
								attrs={"class": "form-control", "placeholder": "请输入用户名", "value": "", "required": "required",}),  
							max_length=20,error_messages={"required": "用户名不能为空",})
	pw = forms.CharField(	widget=forms.PasswordInput(
								attrs={"class": "form-control", "placeholder": "请输入密码", "value": "", "required": "required",}),  
							min_length=8, max_length=20,error_messages={"required": "密码不能为空",})
	pwConfirm = forms.CharField(	widget=forms.PasswordInput(
										attrs={"class": "form-control", "placeholder": "请确认密码", "value": "", "required": "required",}),  
									min_length=8, max_length=20,error_messages={"required": "密码不能为空",})
	email = forms.EmailField(	widget=forms.TextInput(
									attrs={"class": "form-control", "placeholder": "请输入邮箱", "value": "", "required": "required",}),  
								error_messages={"required": "邮箱不能为空",})

class ActivateForm(forms.Form):
	name = forms.CharField(	widget=forms.TextInput(
								attrs={"class": "form-control", "placeholder": "请输入用户名", "value": "", "required": "required",}),  
							max_length=20,error_messages={"required": "用户名不能为空",})
	code = forms.CharField(	widget=forms.TextInput(
								attrs={"class": "form-control", "placeholder": "请输入激活码", "value": "", "required": "required",}),  
							min_length=6, max_length=6,error_messages={"required": "激活码不能为空",})