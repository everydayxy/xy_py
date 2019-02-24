import json

f = open('temp.txt','r')

data = json.loads(f.read())

print(data)
print(data['age'])

data['id']['名牌'] = 30303030

f = open('temp.txt','w')

f.write(json.dumps(data,indent=4,sort_keys=True,ensure_ascii=False))




