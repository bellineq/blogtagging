import json
with open('parsedData/movie3.json', 'r') as f: data = json.load(f)
with open('../userData/user23/movie_23.json','w') as f: json.dump(data[:35],f)
with open('parsedData/movie3.json', 'w') as f: json.dump(data[35:], f)

