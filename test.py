from datetime import datetime

paragraphs = ["value1","value2","value3","value4","value5","value6","value7","value8","value9",]

for p in range(len(paragraphs)):
	print('good')
	print(str(p))


for p in paragraphs[0:50]:
	print('over')
	print(str(p))


for p in paragraphs[0:4]:
	print('below')
	print(str(p))