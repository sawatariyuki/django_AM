from ..models import OperationLog
import urllib.request as r
import json

# 保存用户操作记录
def saveLogs(userDefault, content, request):
	if request.META.__contains__('HTTP_X_FORWARDED_FOR'):
		ip = request.META['HTTP_X_FORWARDED_FOR']
	else:
		ip = request.META['REMOTE_ADDR']

	if IpAddress.objects.filter(ip=ip).exists():
		ipAddress = IpAddress.objects.get(ip=ip)
		locStr = ipAddress.location
	else:
		try:
			ret = getlocationByIp(ip)
			location = json.loads( ret )
			locStr = location['country']+'-'+location['province']+'-'+location['city']
		except:
			locStr = '未知区域'

		if locStr != '未知区域':
			ipAddress = IpAddress(ip=ip, location=locStr)
			ipAddress.save()

	log = OperationLog.objects.create(userDefault=userDefault, content=content, ip=ip, location=locStr)



def getlocationByIp(ip):
	url = 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=%s' % ip
	req = r.Request(url)
	resp = r.urlopen(req)
	result = resp.read().decode('utf-8')
	return result
