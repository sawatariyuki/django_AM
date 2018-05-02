"""AutoManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from user import views as user_views


urlpatterns = [
	# GET getAll
	url(r'^getAll$', user_views.getAll, name='getAll'),
	# GET getLogs
	url(r'^getLogs$', user_views.getLogs, name='getLogs'),
	
	# POST user/register
	# name pw pwConfirm email
	url(r'^user/register$', user_views.register, name='register'),					# 注册用户
	
	# GET user/activate?name=[ ]&code=[ ]
	url(r'^user/activate$', user_views.activate, name='activate'),					# 激活用户
	
	# POST user/activatePage
	# name code
	url(r'^user/activatePage$', user_views.activatePage, name='activatePage'),		# 激活用户
	
	# POST user/loginPage
	# name pw
	url(r'^user/loginPage$', user_views.loginPage, name='loginPage'),				# 登录用户

	# POST user/detailPage
	# name gender weight birthday birthplace liveplace
	# 注意 birthday 为UTC+0的数据
	url(r'^user/detailPage$', user_views.updateUserDetail, name='detailPage'),		# 修改用户详情

	# GET user/userInfo?name=[ ]
	url(r'^user/userInfo$', user_views.getUserInfo, name='userInfo'),				# 获取用户信息




	# GET event/getEvent?name=[ ]&order=[ ]&reverse=[ ]&num=[ ]
	# order指定排序方式: ctime, eventType, userStartTime, sysStartTime, length等,默认ctime
	# reverse指定排序方向: true为从大到小,false为从小到大,默认true
	# num指定返回数据的数量: 默认20
	url(r'^event/getEvent$', user_views.getUserEventByUserName, name='getEvent'),	# 获取用户的事务

	# GET event/getType?name=[ ]
	url(r'^event/getType$', user_views.getUserEventTypeByUserName, name='getType'),	# 获取用户的事务类型
	
	# POST event/addOrUpdateEventType
	# name typeName description
	url(r'^event/addOrUpdateEventType$', user_views.addOrUpdateEventType, name='addOrUpdateEventType'),	# 新增或修改事务类型

	# POST event/deleteEventType
	# name typeName
	url(r'^event/deleteEventType$', user_views.deleteEventType, name='deleteEventType'),	# 删除事务类型

	# POST event/addEvent
	# name title description typeName userLevel userStartTime userEndTime length
	# 注意 userStartTime userEndTime 为UTC+0的数据
	url(r'^event/addEvent$', user_views.addEvent, name='event/addEvent'),			# 新增事务

	# POST event/deleteEvent
	# name pk
	url(r'^event/deleteEvent$', user_views.deleteEvent, name='event/deleteEvent'),	# 删除事务

	# POST event/cancelEvent
	# name pk cancelOrReactive
	# cancelOrReactive: 0表示取消 1表示激活
	url(r'^event/cancelEvent$', user_views.cancelEvent, name='event/cancelEvent'),	# 取消或激活事务

	# GET event/arrange?name=[ ]
	url(r'^event/arrange$', user_views.arrange, name='arrange'),					# 安排事务

	# GET user/log?name=[ ]
	url(r'^user/log$', user_views.getUserLogsByUserName, name='getLog'),			# 获取用户操作记录

	

	url(r'^admin/', admin.site.urls),
]
