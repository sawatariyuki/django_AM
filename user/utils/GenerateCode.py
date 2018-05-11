import random
from django.utils import timezone
from user.models import UserDefault
from .EncodeStr import StrToMD5

# generate a user-diff dynamic code
def GenerateDynamicCode(name):
	activateCode = UserDefault.objects.get(name=name).activateCode
	strTime = timezone.now().strftime('%Y%m%d%H%M')	# 年 月 日 时 分
	return StrToMD5(activateCode + strTime)

# generate a six-length code using [A-Z][0-9]
def getCode():
	codeRange = [chr(i) for i in range(65,91)] + [chr(i) for i in range(48,58)]
	code = ''.join(random.choice(codeRange) for _ in range(6))
	return code