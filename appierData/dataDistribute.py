import json
with open('parsedData/movie2.json', 'r') as f: data = json.load(f)
#with open('movie_8.json', 'w') as f: json.dump(data[:35], f)
#with open('movie_9.json', 'w') as f: json.dump(data[35:105], f)
#with open('movie_10.json', 'w') as f: json.dump(data[105:140], f)
#with open('movie_13.json', 'w') as f: json.dump(data[140:160], f)
#with open('movie_14.json', 'w') as f: json.dump(data[160:195], f)

with open('movie_15.json', 'w') as f: json.dump(data[:20], f)
with open('movie_17.json', 'w') as f: json.dump(data[20:90], f)
with open('movie_18.json', 'w') as f: json.dump(data[90:125], f)
with open('movie_19.json', 'w') as f: json.dump(data[125:160], f)
with open('movie_20.json', 'w') as f: json.dump(data[160:180], f)

with open('parsedData/movie2.json', 'w') as f: json.dump(data[180:], f)

