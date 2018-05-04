from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import datetime, time
import pytz

# Create your models here.
now = timezone.now()
defaultTime = '1990-01-01 12:00:00'
defaultTime = datetime.datetime( * time.strptime(defaultTime, '%Y-%m-%d %H:%M:%S')[:6] ).replace(tzinfo=pytz.timezone('UTC'))

# 用户基本表
class UserDefault(models.Model):
	name = models.CharField(max_length=20, unique=True)							# 用户名 唯一
	pw = models.CharField(max_length=50)										# 密码 MD5加密
	email = models.EmailField()													# 电子邮箱 用于激活用户
	isActivated = models.BooleanField()											# 用户是否激活
	activateCode = models.CharField(max_length=6)								# 激活码
	date_joined = models.DateTimeField(auto_now_add=True, editable=True)		# 注册时间
	last_joined = models.DateTimeField(auto_now=True, editable=True)			# 最后登录时间
	isDeleted = models.BooleanField(default=False)

	def __str__(self):
		return self.name

# 用户详情表
class UserDetail(models.Model):
	userDefault = models.OneToOneField(UserDefault, on_delete=models.CASCADE)	# 一对一

	gender = models.CharField(max_length=2, default='男')						# 性别
	weight = models.FloatField(default=0)										# 体重(单位kg)
	birthday = models.DateTimeField(default=defaultTime)								# 生日 用于计算年龄
	age = models.IntegerField(default=0)										# 年龄
	birthplace = models.CharField(max_length=100, default='未填写')				# 出生地
	liveplace = models.CharField(max_length=100, default='未填写')				# 暂住地

	def __str__(self):
		return self.userDefault.name

# 注：上述情况下，用 UserDefault 拿 UserDetail 时，使用 UserDefault.userdetail (注意全小写)
# 				  用 UserDetail 拿 UserDefault 时，使用 UserDetail.userDefault (即UserDetail中字段的名字)

# 注：一对多情况下，用UserDefault 拿 Event 时，使用 UserDefault.event_set.all()

# 用户事务类型表
class EventType(models.Model):
	userDefault = models.ForeignKey(UserDefault, on_delete=models.CASCADE)		# 多对一

	name = models.CharField(max_length=20)										# 事务类型名
	description = models.CharField(max_length=100, default='未填写描述')		# 事务类型描述
	useTimes = models.PositiveSmallIntegerField (default=0)						# 该事务类型的被使用次数
	emergencyLevel = models.PositiveSmallIntegerField(							# 该事务类型的紧急性 [0,99]
		default = 20,
		validators = [ MinValueValidator(0), MaxValueValidator(99) ]
		)
	ctime = models.DateTimeField(auto_now_add=True, editable=True)				# 事务类型创建时间
	last_used = models.DateTimeField(auto_now=True, editable=True)				# 事务类型最后使用时间

	def __str__(self):
		return self.name

# 用户事件表
class Event(models.Model):
	userDefault = models.ForeignKey(UserDefault, on_delete=models.CASCADE)		# 多对一

	title = models.CharField(max_length=20, default='未填写标题')				# 事务标题
	description = models.TextField(default='未填写描述')						# 事务描述
	eventType = models.ForeignKey(EventType, on_delete=models.CASCADE)			# 事务类型
	ctime = models.DateTimeField(auto_now_add=True, editable=True)				# 事务创建时间

	userLevel = models.PositiveSmallIntegerField(								# 用户描述的事件紧急性 [0,3]
		default = 0,
		validators = [ MinValueValidator(0), MaxValueValidator(3) ],
		help_text = '用户描述的事件紧急性<br>取值[0,3]'
		)
	userStartTime = models.DateTimeField(default=defaultTime)							# 用户决定的开始时间(一般指最晚开始时间)
	userEndTime = models.DateTimeField(default=defaultTime)								# 用户决定的结束时间(最晚结束时间)
	length = models.PositiveIntegerField(default=0, help_text='单位分钟')		# 用户决定的事件总需耗时(单位分钟)
	sysStartTime = models.DateTimeField(default=defaultTime)							# 系统计算得出的开始时间
	sysEndTime = models.DateTimeField(default=defaultTime)								# 系统计算得出的结束时间
	sysLevel = models.PositiveSmallIntegerField(								# 系统根据该事件信息
		default = 0,															# 及用户日常习惯计算得到的紧急性 [0,99]
		validators = [ MinValueValidator(0), MaxValueValidator(99) ],
		help_text = '系统根据该事件信息及用户日常习惯计算得到的紧急性<br>取值[0,99]'
		)
	state = models.PositiveSmallIntegerField(									# 该事务的状态
		default = 0,															# 0:等待被安排 1:已安排 2:已取消 3:已完成
		validators = [ MinValueValidator(0), MaxValueValidator(3) ],
		help_text = '该事务的状态<br>0:等待被安排 1:已安排 2:已取消 3:已完成'
		)

	def __str__(self):
		return self.title

# 操作记录表
class OperationLog(models.Model):
	userDefault = models.ForeignKey(UserDefault, on_delete=models.CASCADE)		# 多对一

	content = models.TextField(null=True)										# 操作
	ip = models.GenericIPAddressField(default='127.0.0.1')						# ip
	ctime = models.DateTimeField(auto_now_add=True, editable=True)				# 记录时间
	location = models.CharField(max_length=100, default='未知区域')				# 登录地址

	def __str__(self):
		return self.userDefault.name + self.content

class IpAddress(models.Model):
	ip = models.GenericIPAddressField()
	location = models.CharField(max_length=100)

	def __str__(self):
		return self.ip