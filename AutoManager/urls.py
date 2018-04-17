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
    url(r'^getAll$', user_views.getAll, name='getAll'),

    url(r'^register$', user_views.register, name='register'),               # 注册用户
    url(r'^activate$', user_views.activate, name='activate'),               # 激活用户 get
    url(r'^activatePage$', user_views.activatePage, name='activatePage'),   # 激活用户 post
	

    url(r'^admin/', admin.site.urls),
]
