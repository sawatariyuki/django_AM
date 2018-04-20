from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.hashers import make_password, check_password


from user.models import *
from .forms import *
from .utils.SendEmail import sendActivateCode
import random

# 注册用户
@csrf_exempt
def register(request):
	if request.method == 'POST':
		registerForm = RegisterForm(request.POST)
		if registerForm.is_valid():

			name = registerForm.cleaned_data['name']
			pw = registerForm.cleaned_data['pw']
			pwConfirm = registerForm.cleaned_data['pwConfirm']
			email = registerForm.cleaned_data['email']

			if pw != pwConfirm:
				return HttpResponse(u'两次输入的密码不同')

			is_name_exist = UserDefault.objects.filter(name=name).exists()
			if is_name_exist:
				return HttpResponse(u'用户名已存在')

			is_email_exist = UserDefault.objects.filter(email=email).exists()
			if is_email_exist:
				return HttpResponse(u'该邮箱已被注册')

			# save
			codeRange = [chr(i) for i in range(65,91)] + [chr(i) for i in range(48,58)]
			aCode = ''.join(random.choice(codeRange) for _ in range(6))
			
			# md5
			pw = make_password(pw, None, 'md5')

			userDefault = UserDefault(name=name, pw=pw, email=email, isActivated=False, activateCode=aCode)
			userDefault.save()

			# sendActivateCode(name, email, aCode)

			return HttpResponse(u'用户:' + name + u' 注册成功，激活码已发送到注册邮箱')

	else:
		registerForm = RegisterForm()
	return render(request, 'user/register.html', {'registerForm':registerForm})


# 激活用户
def activate(request):
	name = request.GET.get('name', '')
	aCode = request.GET.get('code', '')
	if UserDefault.objects.filter(name=name).exists():
		u = UserDefault.objects.get(name=name)
		if u.isActivated:
			return HttpResponse(u'用户已激活')
		else:
			if u.activateCode == aCode:
				UserDefault.objects.filter(name=name).update(isActivated=True)
				return HttpResponse(u'用户已激活')
			else:
				return HttpResponse(u'激活码不正确')
	else:
		return HttpResponse(u'该用户不存在')

@csrf_exempt
def activatePage(request):
	if request.method == 'POST':
		activateForm = ActivateForm(request.POST)
		if activateForm.is_valid():

			name = activateForm.cleaned_data['name']
			aCode = activateForm.cleaned_data['code']

			if UserDefault.objects.filter(name=name).exists():
				u = UserDefault.objects.get(name=name)
				if u.isActivated:
					return HttpResponse(u'用户已激活')
				else:
					if u.activateCode == aCode:
						UserDefault.objects.filter(name=name).update(isActivated=True)
						return HttpResponse(u'用户已激活')
					else:
						return HttpResponse(u'激活码不正确')
			else:
				return HttpResponse(u'该用户不存在')
	else:
		activateForm = ActivateForm()
	return render(request, 'user/activate.html', {'activateForm':activateForm})







def getAll(request):
	allUsers = UserDefault.objects.all()
	return HttpResponse( serializers.serialize("json", allUsers) )



	