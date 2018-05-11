from user.models import *
from django.utils import timezone
from datetime import timedelta
import random
import math

class EventData(object):
	def __init__(self, pk, length, endTime, emergency):
		self.pk = pk
		self.length = length
		self.endTime = endTime
		self.emergency = emergency
		self.SysStartTime = endTime
		self.SysEndTime = endTime

	def __str__(self):
		return '%s Len: %s, End: %s, emergency: %s | S: %s, E: %s' % (
			self.pk, 
			self.length, self.endTime, self.emergency, 
			self.SysStartTime, self.SysEndTime)


def setEventFinish(userDefault):
	# 将过期的事务的设定为已完成
	event_to_finish = Event.objects.filter(userDefault=userDefault).filter(state__in=[0,1,2])	# 获取该用户下 等待安排 已安排 和 已取消 的事务
	now = timezone.now()
	for each in event_to_finish:
		if each.sysStartTime < now:
			each.state = 3
			each.save()


def arrangeEvent(userDefault):
	# 更新用户事务类型中的紧要程度
	eventType = userDefault.eventtype_set.all()
	totalCount = sum([each.useTimes for each in eventType])

	for each in eventType:
		each.emergencyLevel = each.useTimes/totalCount*99
		each.save()

	setEventFinish(userDefault)

	# 计算待安排事务的紧要性
	event_waiting = Event.objects.filter(userDefault=userDefault).filter(state=0)	# 获取该用户下待安排的事务
	
	for each in event_waiting:
		spareTime = (each.userEndTime-each.userStartTime).seconds/60
		rate = each.length/spareTime if each.length<=spareTime and spareTime!=0 else 1 # 事务时长/(结束时间-开始时间)
		# [0, 1]
		# print('spareTime: '+str(rate))

		WEIGHT = [-4.95, -1.65, 1.65, 4.95]
		rate = (rate+0.001) * WEIGHT[each.userLevel]	# [-37.5375, 37.5375]
		# print('USER_WEIGHT'+str(rate))
		
		rate = rate * (each.eventType.emergencyLevel+1)/100
		print('type:'+str(rate)+'\n')

		# sigmoid
		rate = 1/(1+math.e**(-rate))
		print('sigmoid:'+str(rate)+'\n')
		each.sysLevel = int(rate*99)
		each.save()
		

	# 安排事务...(用户最晚时间、系统紧要性)
	data_waiting = list()
	for each in event_waiting:
		data_waiting.append( EventData(each.pk, each.length, each.userEndTime, each.sysLevel) )

	data_waiting.sort(key=lambda e:(e.endTime, e.emergency), reverse=True)
	if len(data_waiting)<=0:
		return 0

	currentTime = data_waiting[0].endTime
	for each in data_waiting:
		currentTime = each.endTime if each.endTime<currentTime else currentTime
		each.SysEndTime, each.SysStartTime = currentTime, currentTime-timedelta(minutes=each.length)
		currentTime = each.SysStartTime

	for each in data_waiting:	# 存储结果
		event = Event.objects.get(pk=each.pk)
		event.sysStartTime, event.sysEndTime = each.SysStartTime, each.SysEndTime
		event.state = 1	# 修改标记位
		event.save()

	return 	len(data_waiting)