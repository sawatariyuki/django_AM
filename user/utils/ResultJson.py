

def getResultJson(code=0, msg="", data=""):
	"""
	code: 0 成功；1 失败	int
	msg: 简要消息			String
	data: 数据对象			String
	"""
	jsonStr = '{"code":' + str(code) + ',"msg":"' + msg + '","data":' + data + ',}'
	return jsonStr