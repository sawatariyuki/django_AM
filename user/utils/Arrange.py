from user.models import *
from django.utils import timezone as datetime

import random


def arrangeEvent(userDefault):
	# 更新用户事务类型中的紧要程度
	eventType = userDefault.eventtype_set.all()






	# 计算...
	event_waiting = Event.objects.filter(userDefault=userDefault).filter(state=0)	# 获取该用户下待安排的事务

	spareTime = dict()
	for event in event_waiting:
		print('userStartTime: %s' % event.userStartTime)
		print('ctime: %s' % event.ctime)
		print( (event.userStartTime-event.ctime).total_seconds() )
		
		spareTime[event.pk] = int((event.userEndTime-event.userStartTime).total_seconds()//60)-event.length

	print(eventType)
	print(event_waiting)
	print(spareTime)