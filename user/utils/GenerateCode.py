import random

# generate a six-length code using [A-Z][0-9]
def getCode():
	codeRange = [chr(i) for i in range(65,91)] + [chr(i) for i in range(48,58)]
	code = ''.join(random.choice(codeRange) for _ in range(6))
	return code