import json

subdata = []

with open('data/food1.json') as json_data:
    data = json.load(json_data)
    subdata.append(data[0:3])
    subdata.append(data[4:6])

with open('data/test/GaoJessica/food.json', 'w+') as outfile_1:
    json.dump(subdata, outfile_1)