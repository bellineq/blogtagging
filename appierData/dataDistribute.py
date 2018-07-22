import json
with open('parsedData/beauty4.json', 'r') as f: data = json.load(f)
print(len(data))

with open('../userData/user25/beauty_25.json','r') as f: udata = json.load(f)
for d in data[:35]: udata.append(d)
with open('../userData/user25/beauty_25.json','w') as f: udata = json.dump(udata,f)
with open('parsedData/beauty3.json', 'w') as f: json.dump(data[35:], f)
