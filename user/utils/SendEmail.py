from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# 发送激活码
def sendActivateCode(name, email, aCode):
	"""
	向邮箱发送验证码
	name: 用户名
	email: 邮箱
	aCode: 激活码
	"""
	from_email = settings.DEFAULT_FROM_EMAIL
	subject = u'[网站信息]激活码'
	# net ip here

	hrefSrt = 'http://127.0.0.1:8000/activate?name=' + name + '&code=' + aCode
	href = '<a href="' + hrefSrt + '">' + aCode + '</a>'
	content = u'这是你的激活码: ' + href + '<br>' + hrefSrt
	to_addr = email

	msg = EmailMultiAlternatives(subject, content, from_email, [to_addr])
	msg.content_subtype = 'html'
	msg.send()