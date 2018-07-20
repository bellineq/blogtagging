import json
with open('parsedData/tech3.json', 'r') as f: data = json.load(f)
print(len(data))

with open('../userData/user13/tech_13.json','r') as f: udata = json.load(f)
for d in data[:15]: udata.append(d)
with open('../userData/user13/tech_13.json','w') as f: udata = json.dump(udata,f)

with open('../userData/user20/tech_20.json','r') as f: udata = json.load(f)
for d in data[15:35]: udata.append(d)
with open('../userData/user20/tech_20.json','w') as f: udata = json.dump(udata,f)

with open('parsedData/tech3.json', 'w') as f: json.dump(data[35:], f)
