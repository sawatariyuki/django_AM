import hashlib

def StrToMD5(str):
	"""
	将字符串用MD5加密

	str: 要被加密的字符串
	"""
	hl = hashlib.md5()
	hl.update(str.encode(encoding='utf-8'))

	return hl.hexdigest()

if __name__ == '__main__':
	strCode = 'pppppppp'
	print( strToMD5(strCode) )