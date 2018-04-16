from django.db import models

# Create your models here.

class UserDefault(models.Model):
	name = models.CharField(max_length=20, unique=True)			# 用户名 唯一
	pw = models.CharField(max_length=32)			# 密码 MD5加密
	email = models.EmailField()						# 电子邮箱 用于激活用户
	isActivated = models.BooleanField()				# 用户是否激活
	activateCode = models.CharField(max_length=6)	# 激活码

	def __str__(self):
		return self.name
