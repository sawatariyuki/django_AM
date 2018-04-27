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
	url(r'^user/register$', user_views.register, name='register'),					# 注册用户
	
	# GET user/activate?name=[ ]&code=[ ]
	url(r'^user/activate$', user_views.activate, name='activate'),					# 激活用户
	
	# POST user/activatePage
	url(r'^user/activatePage$', user_views.activatePage, name='activatePage'),		# 激活用户
	
	# POST user/loginPage
	url(r'^user/loginPage$', user_views.loginPage, name='loginPage'),				# 登录用户

	# POST user/detailPage
	url(r'^user/detailPage$', user_views.updateUserDetail, name='detailPage'),		# 修改用户详情

	# GET user/userInfo?name=[ ]
	url(r'^user/userInfo$', user_views.getUserInfo, name='userInfo'),				# 获取用户信息

	# GET event/getEvent?name=[ ]
	url(r'^event/getEvent$', user_views.getUserEventByUserName, name='getEvent'),	# 获取用户存储的事务

	# GET event/getType?name=[ ]
	url(r'^event/getType$', user_views.getUserEventTypeByUserName, name='getType'),	# 获取用户存储的事务类型
	
	# GET user/log?name=[ ]
	url(r'^user/log$', user_views.getUserLogsByUserName, name='getLog'),		# 获取用户操作记录

	

	url(r'^admin/', admin.site.urls),
]
