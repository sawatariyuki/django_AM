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
from .utils.JsonEncoder import jsonBack, getJson
from .utils.OperationLogs import saveLogs

import random
import datetime
import pytz  

# 用户操作####################################################################################################

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
				return HttpResponse( getJson(code=0, msg=u'两次输入的密码不同', data=[]) )

			is_name_exist = UserDefault.objects.filter(name=name).exists()
			if is_name_exist:
				return HttpResponse( getJson(code=0, msg=u'用户名已存在', data=[]) )

			is_email_exist = UserDefault.objects.filter(email=email).exists()
			if is_email_exist:
				return HttpResponse( getJson(code=0, msg=u'该邮箱已被注册', data=[]) )

			codeRange = [chr(i) for i in range(65,91)] + [chr(i) for i in range(48,58)]
			aCode = ''.join(random.choice(codeRange) for _ in range(6))
			
			# md5
			# pw = make_password(pw, None, 'md5')

			userDefault = UserDefault(name=name, pw=pw, email=email, isActivated=False, activateCode=aCode)
			userDefault.save()
			saveLogs(userDefault=userDefault, content='用户注册', request=request)	# 日志记录

			# sendActivateCode(name, email, aCode)

			return HttpResponse( getJson(code=0, msg=u'用户:' + name + u' 注册成功，激活码已发送到注册邮箱', data=[]) )

	else:
		registerForm = RegisterForm()
	return render(request, 'user/register.html', {'registerForm':registerForm})

# 激活用户 用户的name和code GET
def activate(request):
	name = request.GET.get('name', '')
	aCode = request.GET.get('code', '')
	if UserDefault.objects.filter(name=name).exists():
		u = UserDefault.objects.get(name=name)
		if not u.isDeleted:
			if u.isActivated:
				return HttpResponse( getJson(code=0, msg=u'用户已激活', data=[]) )
			else:
				if u.activateCode == aCode:
					UserDefault.objects.filter(name=name).update(isActivated=True)
					saveLogs(userDefault=u, content='用户激活', request=request)	# 日志记录
					return HttpResponse( getJson(code=0, msg=u'用户已激活', data=[]) )
				else:
					return HttpResponse( getJson(code=0, msg=u'激活码不正确', data=[]) )
		else:
			return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )
	else:
		return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )

# 激活用户 用户的name和code POST
@csrf_exempt
def activatePage(request):
	if request.method == 'POST':
		activateForm = ActivateForm(request.POST)
		if activateForm.is_valid():

			name = activateForm.cleaned_data['name']
			aCode = activateForm.cleaned_data['code']

			if UserDefault.objects.filter(name=name).exists():
				u = UserDefault.objects.get(name=name)
				if not u.isDeleted:
					if u.isActivated:
						return HttpResponse( getJson(code=0, msg=u'用户已激活', data=[]) )
					else:
						if u.activateCode == aCode:
							UserDefault.objects.filter(name=name).update(isActivated=True)
							saveLogs(userDefault=u, content='用户激活', request=request)	# 日志记录
							return HttpResponse( getJson(code=0, msg=u'用户已激活', data=[]) )
						else:
							return HttpResponse( getJson(code=0, msg=u'激活码不正确', data=[]) )
				else:
					return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )
			else:
				return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )
	else:
		activateForm = ActivateForm()
	return render(request, 'user/activate.html', {'activateForm':activateForm})

# 登录判断用户名密码是否正确 用户的name和pw POST
@csrf_exempt
def loginPage(request):
	if request.method == 'POST':
		loginForm = LoginForm(request.POST)
		if loginForm.is_valid():

			name = loginForm.cleaned_data['name']
			pw = loginForm.cleaned_data['pw']

			if UserDefault.objects.filter(name=name).exists():
				u = UserDefault.objects.get(name=name)
				if not u.isDeleted:
					if u.isActivated:
						if u.pw == pw:

							u.save()	# save()用于更新用户最后登录时间 last_joined
							saveLogs(userDefault=u, content='用户登录', request=request)	# 日志记录

							return HttpResponse( getJson(code=0, msg=u'登陆成功', data=[]) )
						else:
							return HttpResponse( getJson(code=0, msg=u'用户名或密码错误', data=[]) )
					else:
						return HttpResponse( getJson(code=0, msg=u'请先激活用户', data=[]) )
				else:
					return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )
			else:
				return HttpResponse( getJson(code=0, msg=u'用户名或密码错误', data=[]) )
	else:
		loginForm = LoginForm()
	return render(request, 'user/login.html', {'loginForm':loginForm})	


# 修改用户详情 根据用户的name POST
@csrf_exempt
def updateUserDetail(request):
	if request.method == 'POST':
		detailForm = DetailForm(request.POST)
		if detailForm.is_valid():
			name = detailForm.cleaned_data['name']
			if UserDefault.objects.filter(name=name).exists():
				u = UserDefault.objects.get(name=name)
				if not u.isDeleted:
					gender = detailForm.cleaned_data['gender']
					weight = detailForm.cleaned_data['weight']
					birthday = detailForm.cleaned_data['birthday']	# birthday:2018-04-24 只要是 yyyy-mm-dd 的字符串就行
					# 将offset-naive(不含时区) 转换为 offset-aware(含时区)
					age = (datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))-birthday).days//365	# 粗略计算一下年龄
					birthplace = detailForm.cleaned_data['birthplace']
					liveplace = detailForm.cleaned_data['liveplace']
					userDetail = UserDetail(userDefault=u, gender=gender, weight=weight, birthday=birthday, age=age, birthplace=birthplace, liveplace=liveplace)
					userDetail.save()
					u.save()	# save()用于更新用户最后登录时间 last_joined
					saveLogs(userDefault=u, content='修改用户详情', request=request)	# 日志记录
					return HttpResponse( getJson(code=0, msg=u'用户详细资料已更新', data=[]) )
				else:
					return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )
			else:
				return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )
	else:
		detailForm = DetailForm()
	return render(request, 'user/detail.html', {'detailForm':detailForm})

# 获取用户信息(包括用户基本信息和用户详情) 根据用户的name GET
def getUserInfo(request):
	name = request.GET.get('name', '')
	if UserDefault.objects.filter(name=name).exists():
		userDefault = UserDefault.objects.get(name=name)
		if not u.isDeleted:
			if UserDetail.objects.filter(userDefault=userDefault).exists():
				userDetail = userDefault.userdetail
			else:
				userDetail = UserDetail()
			userInfo = {'default': userDefault, 'detail': userDetail}
			return HttpResponse( getJson(code=0, msg='', data=userInfo) )
		else:
			return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )
	else:
		return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )

# 事务操作####################################################################################################

# 获取用户存储的事务 根据用户name GET
def getUserEventByUserName(request):
	name = request.GET.get('name', '')
	if UserDefault.objects.filter(name=name).exists():
		userDefault = UserDefault.objects.get(name=name)
		events = userDefault.event_set.all()
		if len(events) > 0:
			return HttpResponse( getJson(code=0, msg='', data=events) )
		else:
			return HttpResponse( getJson(code=0, msg='未查询到事务', data=[]) )
	else:
		return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )

# 获取用户存储的事务类型 根据用户name GET
def getUserEventTypeByUserName(request):
	name = request.GET.get('name', '')
	if UserDefault.objects.filter(name=name).exists():
		userDefault = UserDefault.objects.get(name=name)
		types = userDefault.eventtype_set.all()
		if len(types) > 0:
			return HttpResponse( getJson(code=0, msg='', data=types) )
		else:
			return HttpResponse( getJson(code=0, msg='未查询到事务类型', data=[]) )
	else:
		return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )

# 日志操作####################################################################################################

# 获取用户操作记录 根据用户name GET
def getUserLogsByUserName(request):
	name = request.GET.get('name', '')
	if UserDefault.objects.filter(name=name).exists():
		userDefault = UserDefault.objects.get(name=name)
		logs = userDefault.operationlog_set.all()
		if len(logs) > 0:
			return HttpResponse( getJson(code=0, msg='', data=logs) )
		else:
			return HttpResponse( getJson(code=0, msg='未查询到操作记录', data=[]) )
	else:
		return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )	
##############################################################################################################
# 测试
def getAll(request):
	allUserDefault = UserDefault.objects.all()
	allUserDetail = UserDetail.objects.all()

	# print(allUserDefault[0].userdetail.birthday)
	# print(allUserDetail[0].userDefault.pw)

	strJson = getJson(code=0, msg='', data=[allUserDefault, allUserDetail])
	return HttpResponse( strJson )

def getLogs(request):
	logs = OperationLog.objects.all()
	return HttpResponse( getJson(code=0, msg='', data=logs) )

	