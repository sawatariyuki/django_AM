from ..models import OperationLog

# 保存用户操作记录
def saveLogs(userDefault, content, request):
	if request.META.__contains__('HTTP_X_FORWARDED_FOR'):
		ip = request.META['HTTP_X_FORWARDED_FOR']
	else:
		ip = request.META['REMOTE_ADDR']
	log = OperationLog.objects.create(userDefault=userDefault, content=content, ip=ip)