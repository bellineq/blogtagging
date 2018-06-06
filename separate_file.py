import json

with open('data/alltravel.json') as json_data:
    data = json.load(json_data)

with open('data/alltravel1.json', 'w') as outfile_1:
    json.dump(data[0: int(len(data)/2)], outfile_1)

with open('data/alltravel2.json', 'w') as outfile_2:
    json.dump(data[int(len(data)/2)::], outfile_2)