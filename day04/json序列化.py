import json


data = {
    'name':'alex',
    'age':22,
    'id':{10:12}
}

f = open('temp.txt','w')
f.write(json.dumps(data,indent=4, sort_keys=True, ensure_ascii=False))
f.close()

