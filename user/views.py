from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

# from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone as datetime

from user.models import *
from .forms import *
from .utils.SendEmail import sendActivateCode
from .utils.JsonEncoder import jsonBack, getJson
from .utils.OperationLogs import saveLogs
from .utils.Arrange import arrangeEvent

import random
# import datetime
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

							# 更新事务state
							events = u.event_set.filter(state=1)
							now = datetime.now()
							for each in events:
								if now > each.sysEndTime:
									each.state = 3
									each.save()

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
					birthday = detailForm.cleaned_data['birthday']	# birthday:2018-04-24 只要是 yyyy-MM-dd 的字符串就行
					# 将offset-naive(不含时区) 转换为 offset-aware(含时区)
					# age = (datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))-birthday).days//365	# 粗略计算一下年龄
					age = (datetime.now()-birthday).days//365
					birthplace = detailForm.cleaned_data['birthplace']
					liveplace = detailForm.cleaned_data['liveplace']
					if not UserDetail.objects.filter(userDefault=u).exists():
						userDetail = UserDetail(userDefault=u, gender=gender, weight=weight, birthday=birthday, age=age, birthplace=birthplace, liveplace=liveplace)
						userDetail.save()
					else:
						ud = UserDetail.objects.get(userDefault=u)
						ud.gender = gender
						ud.weight = weight
						ud.birthday = birthday
						ud.age = age
						ud.birthplace = birthplace
						ud.liveplace = liveplace
						ud.save()
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
		u = UserDefault.objects.get(name=name)
		if not u.isDeleted:
			if UserDetail.objects.filter(userDefault=u).exists():
				userDetail = u.userdetail
			else:
				userDetail = UserDetail()
			userInfo = {'default': u, 'detail': userDetail}
			return HttpResponse( getJson(code=0, msg='', data=userInfo) )
		else:
			return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )
	else:
		return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )

# 事务操作####################################################################################################

# 获取用户的事务类型 根据用户name GET
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

# 新增或修改事务类型 用户name POST
@csrf_exempt
def addOrUpdateEventType(request):
	if request.method == 'POST':
		eventTypeForm = EventTypeForm(request.POST)
		if eventTypeForm.is_valid():
			name = eventTypeForm.cleaned_data['name']
			if UserDefault.objects.filter(name=name).exists():
				u = UserDefault.objects.get(name=name)
				typeName = eventTypeForm.cleaned_data['typeName']
				description = eventTypeForm.cleaned_data['description']

				if EventType.objects.filter(userDefault=u).filter(name=typeName).exists():
					eventType = EventType.objects.get(userDefault=u, name=typeName)
					eventType.description = description
					eventType.save()
					saveLogs(userDefault=u, content='更新事务类型', request=request)	# 日志记录
					return HttpResponse( getJson(code=0, msg='事务类型已更新', data=[]) )
				else:
					EventType.objects.create(userDefault=u, name=typeName, description=description)
					saveLogs(userDefault=u, content='新增事务类型', request=request)	# 日志记录
					return HttpResponse( getJson(code=0, msg=u'事务类型已新增', data=[]) )

			else:
				return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )
	else:
		eventTypeForm = EventTypeForm()
	return render(request, 'user/addOrUpdateEventType.html', {'eventTypeForm':eventTypeForm})

# 删除事务类型 用户name 事务name POST
@csrf_exempt
def deleteEventType(request):
	if request.method == 'POST':
		eventTypeDeleteForm = EventTypeDeleteForm(request.POST)
		if eventTypeDeleteForm.is_valid():
			name = eventTypeDeleteForm.cleaned_data['name']
			typeName = eventTypeDeleteForm.cleaned_data['typeName']
			if UserDefault.objects.filter(name=name).exists():
				u = UserDefault.objects.get(name=name)
				eventType = EventType.objects.filter(userDefault=u).filter(name=typeName)
				eventType.delete()
				print(eventType)
				saveLogs(userDefault=u, content='删除事务类型', request=request)	# 日志记录
				return HttpResponse( getJson(code=0, msg=u'事务类型已删除', data=[]) )
			else:
				return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )
	else:
		eventTypeDeleteForm = EventTypeDeleteForm()
	return render(request, 'user/deleteEventType.html', {'eventTypeDeleteForm':eventTypeDeleteForm})

# 获取用户的事务(按ctime最近 排序) 根据用户name GET
def getUserEventByUserName(request):
	name = request.GET.get('name', '')
	order = request.GET.get('order', 'ctime')
	reverse = request.GET.get('reverse', 'true')
	num = request.GET.get('num', '20')

	reverseChoice = ['false', 'true']
	orderChoice = ['ctime', 'eventType', 'userStartTime', 'sysStartTime', 'length']
	if reverse not in reverseChoice:
		reverse = 'true'
	if order not in orderChoice:
		order = 'ctime'
	try:
		num = abs(int(float(num)))
	except ValueError:
		num = 20

	if UserDefault.objects.filter(name=name).exists():
		userDefault = UserDefault.objects.get(name=name)
		if reverse=='true':
			events = userDefault.event_set.all().order_by(order).reverse()
		else:
			events = userDefault.event_set.all().order_by(order)
		if len(events) > 0:
			return HttpResponse( getJson(code=0, msg='', data=events[:num]) )
		else:
			return HttpResponse( getJson(code=0, msg='未查询到事务', data=[]) )
	else:
		return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )

# 新增事务 根据用户name POST
@csrf_exempt
def addEvent(request):
	if request.method == 'POST':
		eventForm = EventForm(request.POST)
		if eventForm.is_valid():
			name = eventForm.cleaned_data['name']
			title = eventForm.cleaned_data['title']
			description = eventForm.cleaned_data['description']
			typeName = eventForm.cleaned_data['typeName']
			userLevel = eventForm.cleaned_data['userLevel']
			userStartTime = eventForm.cleaned_data['userStartTime'].replace(tzinfo=pytz.timezone('UTC'))	# 格式yyyy-MM-dd hh:mm
			userEndTime = eventForm.cleaned_data['userEndTime'].replace(tzinfo=pytz.timezone('UTC'))		# 格式yyyy-MM-dd hh:mm

			length = eventForm.cleaned_data['length']
			_length = int((userEndTime-userStartTime).total_seconds()//60)

			_length = _length if length>_length else length 		# 最终时长

			if int((userStartTime-datetime.now()).total_seconds())<0:
				return HttpResponse( getJson(code=0, msg=u'事务开始时间已不可到达', data=[]) )


			if UserDefault.objects.filter(name=name).exists():
				u = UserDefault.objects.get(name=name)
				eventType = EventType.objects.filter(userDefault=u).filter(name=typeName)[0]
				eventType.useTimes += 1
				eventType.save()

				event = Event(userDefault=u, title=title, description=description, eventType=eventType, 
					userLevel=userLevel, userStartTime=userStartTime, userEndTime=userEndTime, length=_length, 
					sysStartTime=userStartTime, sysEndTime=userEndTime)
				event.save()

				saveLogs(userDefault=u, content='新增事务', request=request)	# 日志记录
				return HttpResponse( getJson(code=0, msg=u'事务已新增', data=[]) )
			else:
				return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )
	else:
		eventForm = EventForm()
	return render(request, 'user/addEvent.html', {'eventForm':eventForm})

# 删除事务 根据用户name 事务pk POST
@csrf_exempt
def deleteEvent(request):
	if request.method == 'POST':
		eventDeleteForm = EventDeleteForm(request.POST)
		if eventDeleteForm.is_valid():
			name = eventDeleteForm.cleaned_data['name']
			pk = eventDeleteForm.cleaned_data['pk']
			if UserDefault.objects.filter(name=name).exists():
				u = UserDefault.objects.get(name=name)
				event = Event.objects.get(userDefault=u, pk=pk)
				event.delete()
				saveLogs(userDefault=u, content='删除事务', request=request)	# 日志记录
				return HttpResponse( getJson(code=0, msg=u'事务已删除', data=[]) )
			else:
				return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )
	else:
		eventDeleteForm = EventDeleteForm()
	return render(request, 'user/deleteEvent.html', {'eventDeleteForm':eventDeleteForm})

# 取消事务 根据用户name 事务pk POST
@csrf_exempt
def cancelEvent(request):
	if request.method == 'POST':
		eventCancelForm = EventCancelForm(request.POST)
		if eventCancelForm.is_valid():
			name = eventCancelForm.cleaned_data['name']
			pk = eventCancelForm.cleaned_data['pk']
			cancelOrReactive = eventCancelForm.cleaned_data['cancelOrReactive']
			if UserDefault.objects.filter(name=name).exists():
				u = UserDefault.objects.get(name=name)
				event = Event.objects.get(userDefault=u, pk=pk)
				if cancelOrReactive=='0':
					event.state = 2
					event.save()
					saveLogs(userDefault=u, content='取消事务', request=request)	# 日志记录
					return HttpResponse( getJson(code=0, msg=u'事务已取消', data=[]) )
				elif cancelOrReactive=='1':
					event.state = 0
					event.save()
					saveLogs(userDefault=u, content='重新安排事务', request=request)	# 日志记录
					return HttpResponse( getJson(code=0, msg=u'事务已在等待安排', data=[]) )
			else:
				return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )
	else:
		eventCancelForm = EventCancelForm()
	return render(request, 'user/cancelEvent.html', {'eventCancelForm':eventCancelForm})

# 安排事务 
def arrange(request):
	name = request.GET.get('name', '')
	if UserDefault.objects.filter(name=name).exists():
		u = UserDefault.objects.get(name=name)
		count = arrangeEvent(userDefault=u)
		events = u.event_set.all()
		if len(events) > 0:
			saveLogs(userDefault=u, content='安排事务', request=request)	# 日志记录
			return HttpResponse( getJson(code=0, msg=str(count)+u'件事务已安排', data=events) )
		else:
			return HttpResponse( getJson(code=0, msg='未查询到事务', data=[]) ) 
	else:
		return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )

# def func(request):
# 	if request.method == 'POST':
# 		yourForm = YourForm(request.POST)
# 		if yourForm.is_valid():
# 			name = yourForm.cleaned_data['name']
# 			if UserDefault.objects.filter(name=name).exists():
# 				u = UserDefault.objects.get(name=name)
#
# 				saveLogs(userDefault=u, content='新增事务类型', request=request)	# 日志记录
# 				return HttpResponse( getJson(code=0, msg=u'事务类型已更新', data=[]) )
# 			else:
# 				return HttpResponse( getJson(code=0, msg=u'该用户不存在', data=[]) )
# 	else:
# 		yourForm = YourForm()
# 	return render(request, 'user/addEventType.html', {'yourForm':yourForm})



# 日志操作####################################################################################################

# 获取用户操作记录 根据用户name GET
def getUserLogsByUserName(request):
	name = request.GET.get('name', '')
	if UserDefault.objects.filter(name=name).exists():
		userDefault = UserDefault.objects.get(name=name)
		logs = userDefault.operationlog_set.all().order_by("ctime").reverse()[:20]	# 最近20条
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

	