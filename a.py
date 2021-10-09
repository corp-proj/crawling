import json

with open('b.json','r', encoding='utf-8') as f:
    da = json.load(f)

d = open('a.txt','w',encoding = 'utf-8')
for i in range(10):
    d.writelines(da[i]['text'])
    d.write('\n')

